"""Tests for pydantic-to-Extend JSON Schema conversion."""

import datetime as dt
import enum
from typing import Dict, List, Optional, Union

import pydantic
import pytest
from typing_extensions import Literal

from extend_ai.wrapper.schema import (
    ExtendCurrency,
    ExtendDate,
    ExtendSignature,
    SchemaConversionError,
    pydantic_to_extend_schema,
)

CURRENCY_SCHEMA = {
    "type": "object",
    "extend:type": "currency",
    "properties": {
        "amount": {"type": ["number", "null"]},
        "iso_4217_currency_code": {"type": ["string", "null"]},
    },
    "required": ["amount", "iso_4217_currency_code"],
    "additionalProperties": False,
}

SIGNATURE_SCHEMA = {
    "type": "object",
    "extend:type": "signature",
    "properties": {
        "printed_name": {"type": ["string", "null"]},
        "signature_date": {"type": ["string", "null"], "extend:type": "date"},
        "is_signed": {"type": ["boolean", "null"]},
        "title_or_role": {"type": ["string", "null"]},
    },
    "required": ["printed_name", "signature_date", "is_signed", "title_or_role"],
    "additionalProperties": False,
}


class TestBasicSchemaCreation:
    def test_generates_valid_json_schema_from_model(self):
        class Schema(pydantic.BaseModel):
            name: Optional[str] = None

        assert pydantic_to_extend_schema(Schema) == {
            "type": "object",
            "properties": {"name": {"type": ["string", "null"]}},
            "required": ["name"],
            "additionalProperties": False,
        }

    def test_sets_additional_properties_false_at_root(self):
        class Schema(pydantic.BaseModel):
            name: Optional[str] = None

        assert pydantic_to_extend_schema(Schema)["additionalProperties"] is False

    def test_adds_all_properties_to_required(self):
        class Schema(pydantic.BaseModel):
            field1: Optional[str] = None
            field2: Optional[float] = None
            field3: Optional[bool] = None

        assert pydantic_to_extend_schema(Schema)["required"] == ["field1", "field2", "field3"]

    def test_rejects_non_model_schema(self):
        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(dict)  # type: ignore[arg-type]


class TestPrimitiveTypes:
    def test_converts_nullable_string(self):
        class Schema(pydantic.BaseModel):
            field: Optional[str] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["field"] == {"type": ["string", "null"]}

    def test_converts_nullable_number(self):
        class Schema(pydantic.BaseModel):
            field: Optional[float] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["field"] == {"type": ["number", "null"]}

    def test_converts_nullable_integer(self):
        class Schema(pydantic.BaseModel):
            field: Optional[int] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["field"] == {"type": ["integer", "null"]}

    def test_converts_nullable_boolean(self):
        class Schema(pydantic.BaseModel):
            field: Optional[bool] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["field"] == {"type": ["boolean", "null"]}

    def test_non_optional_primitives_are_forced_nullable(self):
        class Schema(pydantic.BaseModel):
            name: str
            count: int

        properties = pydantic_to_extend_schema(Schema)["properties"]
        assert properties["name"] == {"type": ["string", "null"]}
        assert properties["count"] == {"type": ["integer", "null"]}

    def test_includes_descriptions(self):
        class Schema(pydantic.BaseModel):
            name: Optional[str] = pydantic.Field(None, description="The customer name")
            age: Optional[float] = pydantic.Field(None, description="Customer age in years")

        properties = pydantic_to_extend_schema(Schema)["properties"]
        assert properties["name"] == {"type": ["string", "null"], "description": "The customer name"}
        assert properties["age"] == {"type": ["number", "null"], "description": "Customer age in years"}


class TestEnumTypes:
    def test_converts_literal_with_null_added(self):
        class Schema(pydantic.BaseModel):
            status: Optional[Literal["active", "inactive"]] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["status"] == {"enum": ["active", "inactive", None]}

    def test_converts_string_enum_with_null_added(self):
        class Status(str, enum.Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        class Schema(pydantic.BaseModel):
            status: Optional[Status] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["status"] == {"enum": ["active", "inactive", None]}

    def test_preserves_description_on_enums(self):
        class Schema(pydantic.BaseModel):
            status: Optional[Literal["active", "inactive"]] = pydantic.Field(None, description="Account status")

        assert pydantic_to_extend_schema(Schema)["properties"]["status"] == {
            "enum": ["active", "inactive", None],
            "description": "Account status",
        }

    def test_does_not_duplicate_null_in_literal(self):
        class Schema(pydantic.BaseModel):
            status: Optional[Literal["active", "inactive", None]] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["status"] == {"enum": ["active", "inactive", None]}

    def test_converts_single_string_literal(self):
        class Schema(pydantic.BaseModel):
            type: Optional[Literal["invoice"]] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["type"] == {"enum": ["invoice", None]}

    def test_rejects_non_string_literals(self):
        class Schema(pydantic.BaseModel):
            value: Optional[Literal[42]] = None

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)

    def test_rejects_non_string_enums(self):
        class Number(enum.Enum):
            ONE = 1
            TWO = 2

        class Schema(pydantic.BaseModel):
            value: Optional[Number] = None

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)


class TestArrayTypes:
    def test_converts_array_of_objects(self):
        class Item(pydantic.BaseModel):
            name: Optional[str] = None
            price: Optional[float] = None

        class Schema(pydantic.BaseModel):
            items: List[Item] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["items"] == {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": ["string", "null"]},
                    "price": {"type": ["number", "null"]},
                },
                "required": ["name", "price"],
                "additionalProperties": False,
            },
        }

    def test_converts_array_of_strings_non_nullable_items(self):
        class Schema(pydantic.BaseModel):
            tags: List[str] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["tags"] == {
            "type": "array",
            "items": {"type": "string"},
        }

    def test_converts_array_of_numbers(self):
        class Schema(pydantic.BaseModel):
            values: List[float] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["values"] == {
            "type": "array",
            "items": {"type": "number"},
        }

    def test_converts_array_of_integers(self):
        class Schema(pydantic.BaseModel):
            counts: List[int] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["counts"] == {
            "type": "array",
            "items": {"type": "integer"},
        }

    def test_converts_array_of_booleans(self):
        class Schema(pydantic.BaseModel):
            flags: List[bool] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["flags"] == {
            "type": "array",
            "items": {"type": "boolean"},
        }

    def test_converts_optional_array(self):
        class Schema(pydantic.BaseModel):
            tags: Optional[List[str]] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["tags"] == {
            "type": "array",
            "items": {"type": "string"},
        }

    def test_includes_description_on_arrays(self):
        class Schema(pydantic.BaseModel):
            items: List[str] = pydantic.Field(default_factory=list, description="List of items")

        assert pydantic_to_extend_schema(Schema)["properties"]["items"] == {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of items",
        }


class TestNestedObjects:
    def test_converts_nested_objects(self):
        class Address(pydantic.BaseModel):
            street: Optional[str] = None
            city: Optional[str] = None
            zip: Optional[str] = None

        class Schema(pydantic.BaseModel):
            address: Optional[Address] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["address"] == {
            "type": "object",
            "properties": {
                "street": {"type": ["string", "null"]},
                "city": {"type": ["string", "null"]},
                "zip": {"type": ["string", "null"]},
            },
            "required": ["street", "city", "zip"],
            "additionalProperties": False,
        }

    def test_handles_deeply_nested_objects(self):
        class Level3(pydantic.BaseModel):
            value: Optional[str] = None

        class Level2(pydantic.BaseModel):
            level3: Optional[Level3] = None

        class Level1(pydantic.BaseModel):
            level2: Optional[Level2] = None

        class Schema(pydantic.BaseModel):
            level1: Optional[Level1] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["level1"] == {
            "type": "object",
            "properties": {
                "level2": {
                    "type": "object",
                    "properties": {
                        "level3": {
                            "type": "object",
                            "properties": {"value": {"type": ["string", "null"]}},
                            "required": ["value"],
                            "additionalProperties": False,
                        },
                    },
                    "required": ["level3"],
                    "additionalProperties": False,
                },
            },
            "required": ["level2"],
            "additionalProperties": False,
        }

    def test_preserves_description_on_nested_objects(self):
        class Address(pydantic.BaseModel):
            street: Optional[str] = None

        class Schema(pydantic.BaseModel):
            address: Optional[Address] = pydantic.Field(None, description="Mailing address")

        assert pydantic_to_extend_schema(Schema)["properties"]["address"]["description"] == "Mailing address"


class TestExtendDate:
    def test_converts_to_extend_type_date(self):
        class Schema(pydantic.BaseModel):
            invoice_date: ExtendDate = None

        assert pydantic_to_extend_schema(Schema)["properties"]["invoice_date"] == {
            "type": ["string", "null"],
            "extend:type": "date",
        }

    def test_plain_date_annotation_converts_to_extend_type_date(self):
        class Schema(pydantic.BaseModel):
            invoice_date: Optional[dt.date] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["invoice_date"] == {
            "type": ["string", "null"],
            "extend:type": "date",
        }

    def test_preserves_description(self):
        class Schema(pydantic.BaseModel):
            invoice_date: ExtendDate = pydantic.Field(None, description="The invoice date")

        assert pydantic_to_extend_schema(Schema)["properties"]["invoice_date"] == {
            "type": ["string", "null"],
            "extend:type": "date",
            "description": "The invoice date",
        }

    def test_works_in_arrays_with_non_nullable_format(self):
        class Schema(pydantic.BaseModel):
            dates: List[dt.date] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["dates"] == {
            "type": "array",
            "items": {"type": "string", "extend:type": "date"},
        }

    def test_rejects_datetime(self):
        class Schema(pydantic.BaseModel):
            timestamp: Optional[dt.datetime] = None

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)


class TestExtendCurrency:
    def test_converts_to_extend_type_currency(self):
        class Schema(pydantic.BaseModel):
            total: Optional[ExtendCurrency] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["total"] == CURRENCY_SCHEMA

    def test_preserves_description(self):
        class Schema(pydantic.BaseModel):
            total: Optional[ExtendCurrency] = pydantic.Field(None, description="Total invoice amount")

        expected = dict(CURRENCY_SCHEMA, description="Total invoice amount")
        assert pydantic_to_extend_schema(Schema)["properties"]["total"] == expected

    def test_works_in_arrays(self):
        class Schema(pydantic.BaseModel):
            amounts: List[ExtendCurrency] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["amounts"] == {
            "type": "array",
            "items": CURRENCY_SCHEMA,
        }


class TestExtendSignature:
    def test_converts_to_extend_type_signature(self):
        class Schema(pydantic.BaseModel):
            customer_signature: Optional[ExtendSignature] = None

        assert pydantic_to_extend_schema(Schema)["properties"]["customer_signature"] == SIGNATURE_SCHEMA

    def test_preserves_description(self):
        class Schema(pydantic.BaseModel):
            signature: Optional[ExtendSignature] = pydantic.Field(None, description="Customer signature")

        assert pydantic_to_extend_schema(Schema)["properties"]["signature"]["description"] == "Customer signature"

    def test_works_in_arrays(self):
        class Schema(pydantic.BaseModel):
            signatures: List[ExtendSignature] = []

        assert pydantic_to_extend_schema(Schema)["properties"]["signatures"] == {
            "type": "array",
            "items": SIGNATURE_SCHEMA,
        }


class TestSchemaConversionError:
    def test_includes_path_in_error_message(self):
        error = SchemaConversionError("Unsupported type", ["items", "nested", "field"])

        assert str(error) == "Unsupported type at path: items.nested.field"
        assert error.path == ["items", "nested", "field"]

    def test_works_without_path(self):
        error = SchemaConversionError("General error")

        assert str(error) == "General error"
        assert error.path == []

    def test_conversion_errors_carry_field_path(self):
        class Inner(pydantic.BaseModel):
            mapping: Dict[str, str] = {}

        class Schema(pydantic.BaseModel):
            inner: Optional[Inner] = None

        with pytest.raises(SchemaConversionError) as exc_info:
            pydantic_to_extend_schema(Schema)
        assert exc_info.value.path == ["inner", "mapping"]


class TestUnsupportedTypes:
    def test_rejects_dict_fields(self):
        class Schema(pydantic.BaseModel):
            mapping: Dict[str, str] = {}

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)

    def test_rejects_non_optional_unions(self):
        class Schema(pydantic.BaseModel):
            value: Union[str, int] = ""

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)

    def test_rejects_array_of_enums(self):
        class Schema(pydantic.BaseModel):
            statuses: List[Literal["a", "b"]] = []

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)

    def test_rejects_array_of_string_enums(self):
        class Status(str, enum.Enum):
            A = "a"

        class Schema(pydantic.BaseModel):
            statuses: List[Status] = []

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)

    def test_rejects_nested_arrays(self):
        class Schema(pydantic.BaseModel):
            matrix: List[List[str]] = []

        with pytest.raises(SchemaConversionError):
            pydantic_to_extend_schema(Schema)


class TestComplexSchemas:
    def test_converts_realistic_invoice_schema(self):
        class Vendor(pydantic.BaseModel):
            name: Optional[str] = pydantic.Field(None, description="Vendor company name")
            address: Optional[str] = pydantic.Field(None, description="Vendor address")

        class LineItem(pydantic.BaseModel):
            description: Optional[str] = None
            quantity: Optional[float] = None
            unit_price: Optional[ExtendCurrency] = None
            line_total: Optional[ExtendCurrency] = None

        class Invoice(pydantic.BaseModel):
            invoice_number: Optional[str] = pydantic.Field(None, description="The invoice number")
            invoice_date: ExtendDate = pydantic.Field(None, description="The invoice date")
            due_date: ExtendDate = pydantic.Field(None, description="Payment due date")
            vendor: Optional[Vendor] = pydantic.Field(None, description="Vendor information")
            total_amount: Optional[ExtendCurrency] = pydantic.Field(None, description="Total invoice amount")
            line_items: List[LineItem] = pydantic.Field(default_factory=list, description="Invoice line items")
            status: Optional[Literal["draft", "sent", "paid", "overdue"]] = pydantic.Field(
                None, description="Invoice status"
            )

        json_schema = pydantic_to_extend_schema(Invoice)

        assert json_schema["type"] == "object"
        assert "invoice_number" in json_schema["required"]
        assert "invoice_date" in json_schema["required"]
        assert "line_items" in json_schema["required"]

        assert json_schema["properties"]["invoice_date"]["extend:type"] == "date"
        assert json_schema["properties"]["total_amount"]["extend:type"] == "currency"
        assert json_schema["properties"]["line_items"]["items"]["properties"]["unit_price"]["extend:type"] == "currency"
        assert json_schema["properties"]["status"]["enum"] == ["draft", "sent", "paid", "overdue", None]

    def test_converts_contract_schema_with_signatures(self):
        class Term(pydantic.BaseModel):
            section: Optional[str] = None
            content: Optional[str] = None

        class Contract(pydantic.BaseModel):
            contract_id: Optional[str] = None
            effective_date: ExtendDate = None
            party_a_signature: Optional[ExtendSignature] = pydantic.Field(None, description="Party A signature")
            party_b_signature: Optional[ExtendSignature] = pydantic.Field(None, description="Party B signature")
            terms: List[Term] = []

        json_schema = pydantic_to_extend_schema(Contract)

        assert json_schema["properties"]["party_a_signature"]["extend:type"] == "signature"
        assert json_schema["properties"]["party_b_signature"]["extend:type"] == "signature"
