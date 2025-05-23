# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.serialization import FieldMetadata
from ..core.unchecked_base_model import UncheckedBaseModel
from .provided_processor_output import ProvidedProcessorOutput


class EvaluationSetItem(UncheckedBaseModel):
    """
    The EvaluationSetItem object represents an item in an evaluation set in Extend. Items are the individual files and expected outputs that are used to evaluate the performance of a given processor in Extend.
    """

    object: str = pydantic.Field()
    """
    The type of response. In this case, it will always be `"evaluation_set_item"`.
    """

    id: str = pydantic.Field()
    """
    The ID of the evaluation set item.
    
    Example: `"evi_kR9mNP12Qw4yTv8BdR3H"`
    """

    evaluation_set_id: typing_extensions.Annotated[str, FieldMetadata(alias="evaluationSetId")] = pydantic.Field()
    """
    The ID of the evaluation set that this item belongs to.
    
    Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    """

    file_id: typing_extensions.Annotated[str, FieldMetadata(alias="fileId")] = pydantic.Field()
    """
    Extend's internal ID for the file. It will always start with "file_".
    
    Example: `"file_xK9mLPqRtN3vS8wF5hB2cQ"`
    """

    expected_output: typing_extensions.Annotated[ProvidedProcessorOutput, FieldMetadata(alias="expectedOutput")] = (
        pydantic.Field()
    )
    """
    The expected output that will be used to evaluate the processor's performance. This will confirm to the output type schema of the processor.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
