# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .step_run_step_type import StepRunStepType


class StepRunStep(UncheckedBaseModel):
    object: str = pydantic.Field()
    """
    The type of response. In this case, it will always be `"workflow_step"`.
    """

    id: str = pydantic.Field()
    """
    The ID of the workflow step.
    
    Example: `"step_xKm9pNv3qWsY_jL2tR5Dh"`
    """

    name: str = pydantic.Field()
    """
    The name of the workflow step.
    
    Example: `"Validate Invoice Total"`
    """

    type: StepRunStepType = pydantic.Field()
    """
    The type of workflow step:
    * `"EXTERNAL_DATA_VALIDATION"` - Validates data against an external source
    * `"RULE_VALIDATION"` - Validates data against defined rules
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
