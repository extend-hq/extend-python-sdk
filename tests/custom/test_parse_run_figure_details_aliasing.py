"""
Regression test for figure block detail serialization.

Figure block details are modeled separately from the block itself, but the
unchecked construction path previously inferred the details type from an
ambiguous union. If the payload used the block's `"figure"` type marker, the
details could be misclassified and leak snake_case keys during
`model_dump(by_alias=True)`.
"""

from extend_ai.core.unchecked_base_model import construct_type
from extend_ai.types.figure_details import FigureDetails
from extend_ai.types.parse_run import ParseRun

PARSE_RUN_WITH_FIGURE_BLOCK_JSON = {
    "object": "parse_run",
    "id": "pr_test123",
    "file": {
        "object": "file",
        "id": "file_1",
        "name": "document.pdf",
        "type": "PDF",
        "metadata": {},
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z",
    },
    "status": "PROCESSED",
    "config": {
        "target": "spatial",
        "engine": "parse_performance",
    },
    "output": {
        "chunks": [
            {
                "object": "chunk",
                "type": "body",
                "content": "Figure chunk",
                "metadata": {"pageNumber": 1},
                "blocks": [
                    {
                        "object": "block",
                        "id": "block_1",
                        "type": "figure",
                        "content": "Figure 1",
                        "details": {
                            "type": "figure",
                            "image_url": "https://example.com/image.png",
                            "figure_type": "chart",
                        },
                        "metadata": {"pageNumber": 1},
                        "polygon": [],
                        "boundingBox": {"top": 0, "left": 0, "width": 1, "height": 1},
                    }
                ],
            }
        ]
    },
}


def test_figure_block_details_dump_uses_aliases() -> None:
    parse_run = construct_type(type_=ParseRun, object_=PARSE_RUN_WITH_FIGURE_BLOCK_JSON)

    chunk = parse_run.output.chunks[0]
    details = chunk.blocks[0].details

    assert isinstance(details, FigureDetails)

    dumped_details = chunk.model_dump(by_alias=True)["blocks"][0]["details"]

    assert dumped_details["type"] == "figure_details"
    assert dumped_details["imageUrl"] == "https://example.com/image.png"
    assert getattr(dumped_details["figureType"], "value", dumped_details["figureType"]) == "chart"
    assert "image_url" not in dumped_details
    assert "figure_type" not in dumped_details
    assert "rowCount" not in dumped_details
    assert "columnCount" not in dumped_details
