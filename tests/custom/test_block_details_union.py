"""
Regression tests for BlockDetails union resolution.

Customer report (Devesh Meena): When calling parse_runs.retrieve() and doing
chunk.model_dump(by_alias=True), the Block.details for figure blocks came back
as a raw dict with snake_case keys (image_url) instead of camelCase (imageUrl).

Root cause: _convert_undiscriminated_union_type tried parse_obj_as() for each
union member in order without checking Literal discriminants first. Since
FigureDetails has all-optional fields, it vacuously matched ANY dict —
including empty {} details from text/heading blocks and cases where
parse_obj_as would fall through to construct_type (yielding snake_case __dict__).

Fix: when any member of the union carries a Literal-typed discriminant field
(like `type: Literal["figure_details"]`), require a strict match (key present
AND value matches) before attempting parse_obj_as or construct_type. This
ensures:
  1. Figure blocks are resolved to FigureDetails (not TableDetails, etc.)
  2. Text/heading blocks with {} details are resolved to the Dict[str, Any]
     fallback (EmptyBlockDetails) — not incorrectly to FigureDetails.
  3. model_dump(by_alias=True) produces camelCase keys for figure details.
"""

import pytest

from extend_ai.core.unchecked_base_model import construct_type
from extend_ai.types.block import Block
from extend_ai.types.block_details import BlockDetails
from extend_ai.types.figure_details import FigureDetails
from extend_ai.types.table_cell_details import TableCellDetails
from extend_ai.types.table_details import TableDetails


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_block(block_type: str, details: dict) -> Block:
    return construct_type(
        type_=Block,
        object_={
            "object": "block",
            "id": "block_abc123",
            "type": block_type,
            "content": "",
            "details": details,
            "metadata": {"pageNumber": 1},
            "polygon": [],
            "boundingBox": {"x": 0, "y": 0, "width": 100, "height": 100},
        },
    )


# ---------------------------------------------------------------------------
# Unit tests on _convert_undiscriminated_union_type via BlockDetails
# ---------------------------------------------------------------------------


class TestBlockDetailsUnionResolution:
    def test_figure_details_resolved_correctly(self):
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        result = _convert_undiscriminated_union_type(
            BlockDetails,
            {"type": "figure_details", "imageUrl": "https://example.com/img.png", "figureType": "chart"},
        )
        assert isinstance(result, FigureDetails)
        assert result.image_url == "https://example.com/img.png"

    def test_table_details_resolved_correctly(self):
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        result = _convert_undiscriminated_union_type(
            BlockDetails,
            {"type": "table_details", "rowCount": 3, "columnCount": 4},
        )
        assert isinstance(result, TableDetails)
        assert result.row_count == 3
        assert result.column_count == 4

    def test_table_cell_details_resolved_correctly(self):
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        result = _convert_undiscriminated_union_type(
            BlockDetails,
            {"type": "table_cell_details", "rowIndex": 0, "columnIndex": 2},
        )
        assert isinstance(result, TableCellDetails)
        assert result.row_index == 0
        assert result.column_index == 2

    def test_empty_dict_returns_empty_dict_not_figure_details(self):
        """Regression: text/heading blocks have {} details and must not be typed as FigureDetails."""
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        result = _convert_undiscriminated_union_type(BlockDetails, {})
        assert isinstance(result, dict)
        assert result == {}

    def test_unknown_type_returns_raw_dict(self):
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        raw = {"type": "some_future_details", "extraField": "value"}
        result = _convert_undiscriminated_union_type(BlockDetails, raw)
        assert isinstance(result, dict)

    def test_figure_details_without_optional_fields(self):
        from extend_ai.core.unchecked_base_model import _convert_undiscriminated_union_type

        result = _convert_undiscriminated_union_type(
            BlockDetails,
            {"type": "figure_details"},
        )
        assert isinstance(result, FigureDetails)
        assert result.image_url is None
        assert result.figure_type is None


# ---------------------------------------------------------------------------
# End-to-end tests through Block + model_dump
# ---------------------------------------------------------------------------


class TestFigureBlockModelDump:
    """
    Regression for customer report: model_dump(by_alias=True) on a Block
    containing a figure-type details should produce camelCase keys.
    """

    def test_figure_block_details_is_figure_details_instance(self):
        block = make_block(
            "figure",
            {"type": "figure_details", "imageUrl": "https://example.com/img.png", "figureType": "chart"},
        )
        assert isinstance(block.details, FigureDetails)

    def test_figure_block_model_dump_by_alias_has_camel_case_keys(self):
        block = make_block(
            "figure",
            {"type": "figure_details", "imageUrl": "https://example.com/img.png", "figureType": "chart"},
        )
        dumped = block.model_dump(by_alias=True)
        details = dumped["details"]

        # Keys must be camelCase (by_alias=True)
        assert "imageUrl" in details, f"Expected 'imageUrl' but got keys: {list(details.keys())}"
        assert "figureType" in details, f"Expected 'figureType' but got keys: {list(details.keys())}"
        assert "image_url" not in details
        assert "figure_type" not in details

    def test_figure_block_model_dump_values(self):
        block = make_block(
            "figure",
            {"type": "figure_details", "imageUrl": "https://example.com/img.png", "figureType": "chart"},
        )
        dumped = block.model_dump(by_alias=True)
        details = dumped["details"]

        assert details["type"] == "figure_details"
        assert details["imageUrl"] == "https://example.com/img.png"
        # figureType is a StrEnum (subclass of str) so equality with plain string holds
        assert details["figureType"] == "chart"

    def test_text_block_details_is_empty_dict(self):
        """Regression: text block {} details must not be typed as FigureDetails."""
        block = make_block("text", {})
        assert isinstance(block.details, dict)
        assert block.details == {}

    def test_text_block_model_dump_details_is_empty_dict(self):
        block = make_block("text", {})
        dumped = block.model_dump(by_alias=True)
        assert dumped["details"] == {}

    def test_table_block_details_is_table_details_instance(self):
        block = make_block(
            "table",
            {"type": "table_details", "rowCount": 5, "columnCount": 3},
        )
        assert isinstance(block.details, TableDetails)
        assert block.details.row_count == 5
        assert block.details.column_count == 3

    def test_table_block_model_dump_by_alias(self):
        block = make_block(
            "table",
            {"type": "table_details", "rowCount": 5, "columnCount": 3},
        )
        dumped = block.model_dump(by_alias=True)
        details = dumped["details"]
        assert "rowCount" in details
        assert "columnCount" in details
        assert details["rowCount"] == 5

    def test_figure_without_figure_type(self):
        """Optional figureType should be None when absent."""
        block = make_block(
            "figure",
            {"type": "figure_details", "imageUrl": "https://example.com/img.png"},
        )
        assert isinstance(block.details, FigureDetails)
        dumped = block.model_dump(by_alias=True)
        assert dumped["details"]["imageUrl"] == "https://example.com/img.png"
        assert dumped["details"].get("figureType") is None
