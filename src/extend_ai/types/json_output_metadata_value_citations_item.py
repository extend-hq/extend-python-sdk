# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.serialization import FieldMetadata
from ..core.unchecked_base_model import UncheckedBaseModel
from .json_output_metadata_value_citations_item_polygon_item import JsonOutputMetadataValueCitationsItemPolygonItem


class JsonOutputMetadataValueCitationsItem(UncheckedBaseModel):
    page: typing.Optional[float] = pydantic.Field(default=None)
    """
    Page number where the citation was found
    """

    reference_text: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="referenceText")] = (
        pydantic.Field(default=None)
    )
    """
    The text that was referenced
    """

    polygon: typing.Optional[typing.List[JsonOutputMetadataValueCitationsItemPolygonItem]] = pydantic.Field(
        default=None
    )
    """
    Array of points defining the polygon around the referenced text
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
