# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, update_forward_refs
from ...core.serialization import FieldMetadata
from ...core.unchecked_base_model import UncheckedBaseModel
from ...types.workflow_run import WorkflowRun


class WorkflowRunUpdateResponse(UncheckedBaseModel):
    success: bool
    workflow_run: typing_extensions.Annotated[WorkflowRun, FieldMetadata(alias="workflowRun")]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from ...types.extraction_field import ExtractionField  # noqa: E402, F401, I001

update_forward_refs(WorkflowRunUpdateResponse)
