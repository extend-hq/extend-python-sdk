# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2, update_forward_refs
from ..core.serialization import FieldMetadata
from ..core.unchecked_base_model import UncheckedBaseModel
from .file import File
from .json_object import JsonObject
from .processor_run import ProcessorRun
from .step_run import StepRun
from .workflow import Workflow
from .workflow_status import WorkflowStatus


class WorkflowRun(UncheckedBaseModel):
    object: str = pydantic.Field()
    """
    The type of response. In this case, it will always be `"workflow_run"`.
    """

    id: str = pydantic.Field()
    """
    The ID of the workflow run.
    
    Example: `"workflow_run_xKm9pNv3qWsY_jL2tR5Dh"`
    """

    name: str = pydantic.Field()
    """
    The name of the workflow run.
    
    Example: `"myFirstFile.pdf"`
    """

    url: str = pydantic.Field()
    """
    A URL to view this workflow run in the Extend UI.
    
    Example: `"https://dashboard.extend.ai/workflows/workflow_Bk9mNp2qWs5_xL8vR4tYh?workflowRunId=workflow_run_Zj3nMx7ZPd9f4c2WQ_kAg"`
    """

    status: WorkflowStatus
    metadata: JsonObject = pydantic.Field()
    """
    The metadata that was passed in when running the Workflow.
    """

    batch_id: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="batchId")] = pydantic.Field(
        default=None
    )
    """
    The batch ID of the WorkflowRun. If this WorkflowRun was created as part of a batch of files, all runs in that batch will have the same batch ID.
    
    Example: `"batch_7Ws31-F5"`
    """

    files: typing.List[File]
    failure_reason: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="failureReason")] = (
        pydantic.Field(default=None)
    )
    """
    The reason why the workflow run failed. Will only be included if the workflow run status is "FAILED".
    """

    failure_message: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="failureMessage")] = (
        pydantic.Field(default=None)
    )
    """
    A more detailed message about the failure. Will only be included if the workflow run status is "FAILED".
    """

    initial_run_at: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="initialRunAt")] = pydantic.Field()
    """
    The time (in UTC) at which the workflow run was created. Will follow the RFC 3339 format.
    
    Example: `"2025-04-28T17:01:39.285Z"`
    """

    reviewed_by: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="reviewedBy")] = pydantic.Field(
        default=None
    )
    """
    The email address of the person who reviewed the workflow run. Will not be included if the workflow run has not been reviewed.
    
    Example: `"jane.doe@example.com"`
    """

    reviewed: bool = pydantic.Field()
    """
    Whether the workflow run has been reviewed.
    """

    rejection_note: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="rejectionNote")] = (
        pydantic.Field(default=None)
    )
    """
    A note that is added if a workflow run is rejected.
    
    Example: `"Invalid invoice format"`
    """

    reviewed_at: typing_extensions.Annotated[typing.Optional[dt.datetime], FieldMetadata(alias="reviewedAt")] = (
        pydantic.Field(default=None)
    )
    """
    The time (in UTC) at which the workflow run was reviewed. Will follow the RFC 3339 format. Will not be included if the workflow run has not been reviewed.
    
    Example: `"2024-03-21T16:45:00Z"`
    """

    start_time: typing_extensions.Annotated[typing.Optional[dt.datetime], FieldMetadata(alias="startTime")] = (
        pydantic.Field(default=None)
    )
    """
    The time (in UTC) at which the workflow run started executing. This will always be after the `initialRunAt` time. Will follow the RFC 3339 format. Will not be included if the workflow run has not started executing.
    
    Example: `"2024-03-21T15:30:00Z"`
    """

    end_time: typing_extensions.Annotated[typing.Optional[dt.datetime], FieldMetadata(alias="endTime")] = (
        pydantic.Field(default=None)
    )
    """
    The time (in UTC) that the workflow finished executing. Will follow the RFC 3339 format. Will not be included if the workflow run has not finished executing.
    
    Example: `"2024-03-21T15:35:00Z"`
    """

    outputs: typing.List[ProcessorRun]
    step_runs: typing_extensions.Annotated[typing.List[StepRun], FieldMetadata(alias="stepRuns")] = pydantic.Field()
    """
    An array of WorkflowStepRun objects. Each WorkflowStepRun represents a single run of a WorkflowStep and contains details about the step and the run's output.
    
    Note: This field currently supports External Data Validation and Rule Validation step types. Document processor run outputs are included in the outputs field.
    """

    workflow: Workflow

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .extraction_field import ExtractionField  # noqa: E402, F401, I001

update_forward_refs(WorkflowRun)
