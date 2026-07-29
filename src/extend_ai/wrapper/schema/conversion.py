"""
Converts pydantic models to Extend's JSON Schema format.

Note: The API performs comprehensive validation and transformation of schemas.
This module focuses on structural conversion; complex validation (nesting
limits, property counts, property key format) is handled server-side.
"""

import datetime as dt
import enum
import types
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from .custom_types import get_extend_type

__all__ = ["SchemaConversionError", "pydantic_to_extend_schema"]

_NoneType = type(None)


class SchemaConversionError(Exception):
    """Raised when a pydantic model cannot be converted to Extend JSON Schema."""

    def __init__(self, message: str, path: typing.Optional[typing.List[str]] = None):
        self.path: typing.List[str] = list(path or [])
        if self.path:
            message = f"{message} at path: {'.'.join(self.path)}"
        super().__init__(message)


def _iter_model_fields(
    model: typing.Type[pydantic.BaseModel],
) -> typing.Iterator[typing.Tuple[str, typing.Any, typing.Optional[str]]]:
    """
    Yield (field_name, annotation, description) for each field of a pydantic
    model, working under both pydantic v1 and v2.
    """
    # Raw class annotations (via get_type_hints) preserve Optional wrappers,
    # which pydantic v1's `outer_type_` strips.
    try:
        hints = typing_extensions.get_type_hints(model, include_extras=True)
    except Exception:
        hints = {}

    if IS_PYDANTIC_V2:
        for name, field in model.model_fields.items():  # type: ignore[attr-defined]
            yield name, hints.get(name, field.annotation), field.description
    else:
        for name, field in model.__fields__.items():  # type: ignore[attr-defined]
            description = getattr(field.field_info, "description", None)  # type: ignore[attr-defined]
            yield name, hints.get(name, field.outer_type_), description  # type: ignore[attr-defined]


def _is_union_origin(origin: typing.Any) -> bool:
    if origin is typing.Union:
        return True
    union_type = getattr(types, "UnionType", None)  # X | Y syntax on Python 3.10+
    return union_type is not None and origin is union_type


def _unwrap_annotation(annotation: typing.Any, path: typing.List[str]) -> typing.Any:
    """
    Strip Annotated metadata and Optional/None-unions from an annotation,
    returning the inner type. Unions of multiple non-None types are rejected.
    """
    while True:
        origin = typing_extensions.get_origin(annotation)
        if origin is typing_extensions.Annotated:
            annotation = typing_extensions.get_args(annotation)[0]
        elif _is_union_origin(origin):
            non_none = [arg for arg in typing_extensions.get_args(annotation) if arg is not _NoneType]
            if len(non_none) != 1:
                raise SchemaConversionError(
                    "Union types are not supported (only Optional[...] is allowed)", path
                )
            annotation = non_none[0]
        else:
            return annotation


def _with_description(schema: typing.Dict[str, typing.Any], description: typing.Optional[str]) -> typing.Dict[str, typing.Any]:
    if description:
        schema["description"] = description
    return schema


def _date_schema() -> typing.Dict[str, typing.Any]:
    return {"type": ["string", "null"], "extend:type": "date"}


def _currency_schema() -> typing.Dict[str, typing.Any]:
    return {
        "type": "object",
        "extend:type": "currency",
        "properties": {
            "amount": {"type": ["number", "null"]},
            "iso_4217_currency_code": {"type": ["string", "null"]},
        },
        "required": ["amount", "iso_4217_currency_code"],
        "additionalProperties": False,
    }


def _signature_schema() -> typing.Dict[str, typing.Any]:
    return {
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


def _enum_values(annotation: typing.Any, path: typing.List[str]) -> typing.List[typing.Optional[str]]:
    """Extract string enum values from a Literal[...] or string Enum class."""
    if typing_extensions.get_origin(annotation) is typing_extensions.Literal:
        raw_values: typing.List[typing.Any] = [v for v in typing_extensions.get_args(annotation) if v is not None]
    else:  # enum.Enum subclass
        raw_values = [member.value for member in annotation]

    values: typing.List[typing.Optional[str]] = []
    for value in raw_values:
        if not isinstance(value, str):
            raise SchemaConversionError(
                f"Enums must only contain strings, got {type(value).__name__}: {value!r}", path
            )
        values.append(value)
    values.append(None)
    return values


def _is_enum_annotation(annotation: typing.Any) -> bool:
    if typing_extensions.get_origin(annotation) is typing_extensions.Literal:
        return True
    return isinstance(annotation, type) and issubclass(annotation, enum.Enum)


def pydantic_to_extend_schema(model: typing.Type[pydantic.BaseModel]) -> typing.Dict[str, typing.Any]:
    """
    Convert a pydantic model class to Extend's JSON Schema format.

    All primitive fields become nullable (per Extend's schema requirements),
    every property is listed as required, and `Optional[...]` wrappers are
    unwrapped. Field descriptions come from ``Field(description=...)``.

    Args:
        model: A ``pydantic.BaseModel`` subclass describing the data to extract.

    Returns:
        The Extend JSON Schema as a plain dict.

    Raises:
        SchemaConversionError: If the model uses unsupported types.
    """
    if not (isinstance(model, type) and issubclass(model, pydantic.BaseModel)):
        raise SchemaConversionError(f"Schema must be a pydantic BaseModel subclass, got {model!r}")
    return _convert_object(model, [])


def _convert_object(model: typing.Type[pydantic.BaseModel], path: typing.List[str]) -> typing.Dict[str, typing.Any]:
    properties: typing.Dict[str, typing.Any] = {}
    required: typing.List[str] = []

    for name, annotation, description in _iter_model_fields(model):
        properties[name] = _convert_annotation(annotation, description, path + [name])
        required.append(name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def _convert_annotation(
    annotation: typing.Any, description: typing.Optional[str], path: typing.List[str]
) -> typing.Dict[str, typing.Any]:
    inner = _unwrap_annotation(annotation, path)

    if typing_extensions.get_origin(inner) is list or inner is list:
        args = typing_extensions.get_args(inner)
        if not args:
            raise SchemaConversionError("Arrays must declare an item type (use List[...])", path)
        return _with_description({"type": "array", "items": _convert_array_item(args[0], path)}, description)

    if _is_enum_annotation(inner):
        return _with_description({"enum": _enum_values(inner, path)}, description)

    if isinstance(inner, type):
        if issubclass(inner, pydantic.BaseModel):
            extend_type = get_extend_type(inner)
            if extend_type == "currency":
                return _with_description(_currency_schema(), description)
            if extend_type == "signature":
                return _with_description(_signature_schema(), description)
            return _with_description(_convert_object(inner, path), description)
        if issubclass(inner, bool):
            return _with_description({"type": ["boolean", "null"]}, description)
        if issubclass(inner, int):
            return _with_description({"type": ["integer", "null"]}, description)
        if issubclass(inner, float):
            return _with_description({"type": ["number", "null"]}, description)
        if issubclass(inner, dt.datetime):
            raise SchemaConversionError(
                "datetime.datetime is not supported; use datetime.date (or ExtendDate) for date fields", path
            )
        if issubclass(inner, dt.date):
            return _with_description(_date_schema(), description)
        if issubclass(inner, str):
            return _with_description({"type": ["string", "null"]}, description)

    raise SchemaConversionError(f"Unsupported type: {inner!r}", path)


def _convert_array_item(annotation: typing.Any, path: typing.List[str]) -> typing.Dict[str, typing.Any]:
    """
    Convert array item types, which have different rules than top-level types:
    items can be objects or primitives, and primitive items are NOT nullable.
    """
    inner = _unwrap_annotation(annotation, path)

    if _is_enum_annotation(inner):
        raise SchemaConversionError(
            "Enums are not supported as array items. "
            "Array items must be objects or primitives (string, number, integer, boolean).",
            path,
        )

    if isinstance(inner, type) and issubclass(inner, pydantic.BaseModel):
        extend_type = get_extend_type(inner)
        if extend_type == "currency":
            return _currency_schema()
        if extend_type == "signature":
            return _signature_schema()
        return _convert_object(inner, path)

    if isinstance(inner, type):
        if issubclass(inner, bool):
            return {"type": "boolean"}
        if issubclass(inner, int):
            return {"type": "integer"}
        if issubclass(inner, float):
            return {"type": "number"}
        if issubclass(inner, dt.datetime):
            raise SchemaConversionError(
                "datetime.datetime is not supported; use datetime.date (or ExtendDate) for date fields", path
            )
        if issubclass(inner, dt.date):
            return {"type": "string", "extend:type": "date"}
        if issubclass(inner, str):
            return {"type": "string"}

    raise SchemaConversionError(
        f"Unsupported array item type: {inner!r}. "
        "Array items must be objects or primitives (string, number, integer, boolean).",
        path,
    )
