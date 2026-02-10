"""
Regression test: FieldMetadata aliases must work on Python 3.10+ even when
the TypedDict has circular TYPE_CHECKING-only imports that cause
get_type_hints() to raise NameError.

This reproduces the bug where EditJsonParams fields like extend_edit_bbox
were sent with underscore keys instead of their colon aliases
(extend_edit:bbox) because the NameError fallback returned unresolvable
ForwardRef strings.
"""

from extend_ai.core.serialization import convert_and_respect_annotation_metadata
from extend_ai.requests.edit_json import EditJsonParams
from extend_ai.requests.edit_config import EditConfigParams
from extend_ai.requests.edit_bounding_box import EditBoundingBoxParams
from extend_ai.types import EditJsonExtendEditFieldType


def test_convert_and_respect_annotation_metadata_with_circular_typeddict_aliases() -> None:
    data: EditConfigParams = {
        "schema": {
            "type": "object",
            "properties": {
                "test_field": EditJsonParams(
                    type=["string", "null"],
                    description="A test field",
                    extend_edit_field_type=EditJsonExtendEditFieldType.TEXT,
                    extend_edit_bbox=EditBoundingBoxParams(left=1.0, top=2.0, right=3.0, bottom=4.0),
                    extend_edit_page_index=0,
                    extend_edit_value="hello",
                ),
            },
        },
    }

    converted = convert_and_respect_annotation_metadata(
        object_=data, annotation=EditConfigParams, direction="write"
    )

    schema = converted["schema"]
    props = schema["properties"]
    field = props["test_field"]

    # Verify colon-separated aliases are used (not underscore Python attribute names)
    assert "extend_edit:field_type" in field, f"Expected 'extend_edit:field_type' but got keys: {list(field.keys())}"
    assert "extend_edit:bbox" in field, f"Expected 'extend_edit:bbox' but got keys: {list(field.keys())}"
    assert "extend_edit:page_index" in field, f"Expected 'extend_edit:page_index' but got keys: {list(field.keys())}"
    assert "extend_edit:value" in field, f"Expected 'extend_edit:value' but got keys: {list(field.keys())}"

    # Verify underscore names are NOT present
    assert "extend_edit_field_type" not in field, "Underscore key 'extend_edit_field_type' should not be present"
    assert "extend_edit_bbox" not in field, "Underscore key 'extend_edit_bbox' should not be present"
    assert "extend_edit_page_index" not in field, "Underscore key 'extend_edit_page_index' should not be present"
    assert "extend_edit_value" not in field, "Underscore key 'extend_edit_value' should not be present"

    # Verify values are correct
    assert field["extend_edit:field_type"] == "text"
    assert field["extend_edit:bbox"] == {"left": 1.0, "top": 2.0, "right": 3.0, "bottom": 4.0}
    assert field["extend_edit:page_index"] == 0
    assert field["extend_edit:value"] == "hello"

    # Also verify non-aliased fields pass through
    assert field["type"] == ["string", "null"]
    assert field["description"] == "A test field"
