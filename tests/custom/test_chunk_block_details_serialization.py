"""Regression tests for Chunk → Block → BlockDetails deserialization.

Two bugs caused ``model_dump(by_alias=True)`` to produce incorrect output for
block details:

1. **ForwardRef on Chunk.blocks** — ``Chunk.blocks`` is annotated as
   ``List["Block"]``.  Under Pydantic v2 + ``from __future__ import annotations``,
   ``model_rebuild`` does not replace the ForwardRef in ``model_fields``.
   ``construct_type`` saw a ForwardRef (not a class) and fell through to
   ``return object_``, leaving every block as a raw dict.

2. **Greedy FigureDetails match** — ``FigureDetails`` has all-optional fields
   (besides ``type`` which has a Literal default).  ``parse_obj_as(FigureDetails, {})``
   always succeeds, so the undiscriminated-union resolver picked FigureDetails
   for *every* dict — including empty ``{}`` details for text/heading blocks.
"""

from extend_ai.core.unchecked_base_model import construct_type
from extend_ai.types.block import Block
from extend_ai.types.block_details import BlockDetails
from extend_ai.types.chunk import Chunk
from extend_ai.types.figure_details import FigureDetails
from extend_ai.types.table_cell_details import TableCellDetails
from extend_ai.types.table_details import TableDetails


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_block_raw(block_type: str, details: dict) -> dict:
    return {
        "object": "block",
        "id": "block_test",
        "type": block_type,
        "content": "",
        "details": details,
        "metadata": {"page": {"number": 1}},
        "polygon": [],
        "boundingBox": {"x": 0, "y": 0, "width": 1, "height": 1},
    }


def _make_chunk_raw(*blocks: dict) -> dict:
    return {
        "object": "chunk",
        "type": "page",
        "content": "x",
        "metadata": {"pageRange": {"start": 1, "end": 1}},
        "blocks": list(blocks),
    }


# ---------------------------------------------------------------------------
# Bug 1: ForwardRef — Chunk.blocks items must be Block instances
# ---------------------------------------------------------------------------


class TestChunkBlocksForwardRefResolution:
    def test_blocks_are_block_instances(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "image"}),
            ),
            host=Chunk,
        )
        assert isinstance(chunk.blocks[0], Block)

    def test_figure_details_through_chunk(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "chart"}),
            ),
            host=Chunk,
        )
        assert isinstance(chunk.blocks[0].details, FigureDetails)

    def test_figure_details_alias_serialization_through_chunk(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "image"}),
            ),
            host=Chunk,
        )
        dumped = chunk.model_dump(by_alias=True)
        details = dumped["blocks"][0]["details"]
        assert "imageUrl" in details
        assert "figureType" in details
        assert "image_url" not in details
        assert "figure_type" not in details


# ---------------------------------------------------------------------------
# Bug 2: Greedy FigureDetails match on undiscriminated union
# ---------------------------------------------------------------------------


class TestBlockDetailsUnionResolution:
    def test_figure_details_resolved_correctly(self) -> None:
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "chart"}),
        )
        assert isinstance(block.details, FigureDetails)
        assert block.details.image_url == "https://x.com/a.png"

    def test_table_details_resolved_correctly(self) -> None:
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("table", {"type": "table_details", "rowCount": 3, "columnCount": 4}),
        )
        assert isinstance(block.details, TableDetails)
        assert block.details.row_count == 3
        assert block.details.column_count == 4

    def test_table_cell_details_resolved_correctly(self) -> None:
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("table_cell", {"type": "table_cell_details", "rowIndex": 0, "columnIndex": 2}),
        )
        assert isinstance(block.details, TableCellDetails)
        assert block.details.row_index == 0
        assert block.details.column_index == 2

    def test_empty_dict_returns_empty_dict_not_figure_details(self) -> None:
        """Text/heading blocks have ``details: {}`` — must NOT become FigureDetails."""
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("text", {}),
        )
        assert isinstance(block.details, dict)
        assert block.details == {}

    def test_empty_dict_model_dump_stays_empty(self) -> None:
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("text", {}),
        )
        dumped = block.model_dump(by_alias=True)
        assert dumped["details"] == {}

    def test_unknown_type_returns_raw_dict(self) -> None:
        raw = {"type": "some_future_details", "extraField": "value"}
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("text", raw),
        )
        assert isinstance(block.details, dict)

    def test_figure_details_without_optional_fields(self) -> None:
        block = construct_type(
            type_=Block,
            object_=_make_block_raw("figure", {"type": "figure_details"}),
        )
        assert isinstance(block.details, FigureDetails)
        assert block.details.image_url is None
        assert block.details.figure_type is None


# ---------------------------------------------------------------------------
# End-to-end: model_dump(by_alias=True) through Chunk
# ---------------------------------------------------------------------------


class TestEndToEndChunkDump:
    def test_figure_block_camel_case_keys(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "chart"}),
            ),
            host=Chunk,
        )
        dumped = chunk.model_dump(by_alias=True)
        details = dumped["blocks"][0]["details"]
        assert details["type"] == "figure_details"
        assert details["imageUrl"] == "https://x.com/a.png"
        assert "image_url" not in details

    def test_text_block_empty_details(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("text", {}),
            ),
            host=Chunk,
        )
        dumped = chunk.model_dump(by_alias=True)
        assert dumped["blocks"][0]["details"] == {}

    def test_table_block_camel_case_keys(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("table", {"type": "table_details", "rowCount": 5, "columnCount": 3}),
            ),
            host=Chunk,
        )
        dumped = chunk.model_dump(by_alias=True)
        details = dumped["blocks"][0]["details"]
        assert "rowCount" in details
        assert "columnCount" in details
        assert details["rowCount"] == 5

    def test_mixed_block_types(self) -> None:
        chunk = construct_type(
            type_=Chunk,
            object_=_make_chunk_raw(
                _make_block_raw("figure", {"type": "figure_details", "imageUrl": "https://x.com/a.png", "figureType": "image"}),
                _make_block_raw("text", {}),
                _make_block_raw("table", {"type": "table_details", "rowCount": 2, "columnCount": 3}),
            ),
            host=Chunk,
        )
        dumped = chunk.model_dump(by_alias=True)

        assert isinstance(chunk.blocks[0].details, FigureDetails)
        assert isinstance(chunk.blocks[1].details, dict)
        assert isinstance(chunk.blocks[2].details, TableDetails)

        assert dumped["blocks"][0]["details"]["imageUrl"] == "https://x.com/a.png"
        assert dumped["blocks"][1]["details"] == {}
        assert dumped["blocks"][2]["details"]["rowCount"] == 2
