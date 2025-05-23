# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.serialization import FieldMetadata
from ..core.unchecked_base_model import UncheckedBaseModel


class ExtractMetricsFieldMetrics(UncheckedBaseModel):
    """
    Record mapping field names to their respective metrics.
    """

    mean_confidence: typing_extensions.Annotated[typing.Optional[float], FieldMetadata(alias="meanConfidence")] = (
        pydantic.Field(default=None)
    )
    """
    The mean confidence score for this field across all documents.
    """

    recall_perc: typing_extensions.Annotated[typing.Optional[float], FieldMetadata(alias="recallPerc")] = (
        pydantic.Field(default=None)
    )
    """
    The recall percentage for this field, representing how many of the expected values were correctly extracted.
    """

    precision_perc: typing_extensions.Annotated[typing.Optional[float], FieldMetadata(alias="precisionPerc")] = (
        pydantic.Field(default=None)
    )
    """
    The precision percentage for this field, representing how many of the extracted values were correct.
    """

    field_metrics: typing_extensions.Annotated[
        typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]], FieldMetadata(alias="fieldMetrics")
    ] = pydantic.Field(default=None)
    """
    For nested object fields, this contains metrics for the child fields. Has the same structure as the parent fieldMetrics.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
