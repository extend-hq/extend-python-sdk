"""Regression: Chunk.blocks uses ForwardRef('Block'); construct_type must resolve it so nested models serialize with aliases."""

from extend_ai.core.unchecked_base_model import construct_type
from extend_ai.types.block import Block
from extend_ai.types.chunk import Chunk
from extend_ai.types.figure_details import FigureDetails


def test_chunk_blocks_resolve_forward_ref_and_figure_details_dump_by_alias() -> None:
    chunk_raw = {
        "object": "chunk",
        "type": "page",
        "content": "x",
        "metadata": {"pageRange": {"start": 1, "end": 1}},
        "blocks": [
            {
                "object": "block",
                "id": "b1",
                "type": "figure",
                "content": "",
                "details": {
                    "type": "figure_details",
                    "image_url": "https://example.com/fig.png",
                    "figure_type": "image",
                },
                "metadata": {"page": {"number": 1}},
                "polygon": [],
                "boundingBox": {"x": 0, "y": 0, "width": 1, "height": 1},
            }
        ],
    }
    chunk = construct_type(type_=Chunk, object_=chunk_raw, host=Chunk)
    assert isinstance(chunk.blocks[0], Block)
    assert isinstance(chunk.blocks[0].details, FigureDetails)

    dumped = chunk.model_dump(by_alias=True)
    details = dumped["blocks"][0]["details"]
    assert isinstance(details, dict)
    assert "imageUrl" in details
    assert "figureType" in details
    assert "image_url" not in details
