# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from ...core.serialization import FieldMetadata
from ...core.unchecked_base_model import UncheckedBaseModel
from ...types.evaluation_set_item import EvaluationSetItem


class EvaluationSetItemCreateResponse(UncheckedBaseModel):
    success: bool
    evaluation_set_item: typing_extensions.Annotated[EvaluationSetItem, FieldMetadata(alias="evaluationSetItem")]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
