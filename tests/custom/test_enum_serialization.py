"""
Regression test for Pydantic serialization warnings on enum fields.

When `skip_validation` is enabled, the SDK uses `construct_type` to build
response models without Pydantic validation. Before the fix, enum-typed
fields were left as raw strings, causing PydanticSerializationUnexpectedValue
warnings on `model_dump_json()`.
"""

import warnings

from extend_ai.core.unchecked_base_model import construct_type
from extend_ai.types.workflow_run import WorkflowRun
from extend_ai.types.parser_run import ParserRun


WORKFLOW_RUN_JSON = {
    "object": "workflow_run",
    "id": "workflow_run_test123",
    "workflow": {"id": "wf_1", "name": "Test"},
    "workflowVersion": {"id": "wfv_1", "version": 1},
    "dashboardUrl": "https://dashboard.extend.ai/test",
    "status": "PROCESSED",
    "metadata": {},
    "batchId": None,
    "files": [
        {
            "object": "file",
            "id": "file_1",
            "name": "invoice.pdf",
            "type": "PDF",
            "metadata": {},
            "createdAt": "2025-01-01T00:00:00Z",
            "updatedAt": "2025-01-01T00:00:00Z",
        }
    ],
    "reviewed": False,
    "stepRuns": [],
}

PARSER_RUN_JSON = {
    "object": "parser_run",
    "id": "parser_run_test123",
    "fileId": "file_1",
    "chunks": [],
    "status": "PROCESSED",
}


def _enum_serialization_warnings(caught: list) -> list:
    return [
        w for w in caught
        if "Expected `enum`" in str(w.message)
    ]


def test_workflow_run_model_dump_json_no_warnings() -> None:
    workflow_run = construct_type(type_=WorkflowRun, object_=WORKFLOW_RUN_JSON)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        workflow_run.model_dump_json()

    bad = _enum_serialization_warnings(caught)
    assert bad == [], (
        f"Expected no enum serialization warnings, got: "
        f"{[str(w.message) for w in bad]}"
    )


def test_parser_run_model_dump_json_no_warnings() -> None:
    parser_run = construct_type(type_=ParserRun, object_=PARSER_RUN_JSON)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        parser_run.model_dump_json()

    bad = _enum_serialization_warnings(caught)
    assert bad == [], (
        f"Expected no enum serialization warnings, got: "
        f"{[str(w.message) for w in bad]}"
    )
