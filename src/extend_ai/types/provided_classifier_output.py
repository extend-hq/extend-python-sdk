# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class ProvidedClassifierOutput(UncheckedBaseModel):
    id: str = pydantic.Field()
    """
    The unique identifier for this classification
    """

    type: str = pydantic.Field()
    """
    The type of classification
    """

    confidence: typing.Optional[float] = pydantic.Field(default=None)
    """
    A value between 0 and 1 indicating the model's confidence in the classification, where 1 represents maximum confidence
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
