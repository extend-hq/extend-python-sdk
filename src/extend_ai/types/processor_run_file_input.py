# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.serialization import FieldMetadata
from ..core.unchecked_base_model import UncheckedBaseModel


class ProcessorRunFileInput(UncheckedBaseModel):
    """
    Input file for running a single processor.
    """

    file_name: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="fileName")] = pydantic.Field(
        default=None
    )
    """
    The name of the file to be processed. If not provided, the file name will be inferred from the URL. It is highly recommended to include this parameter for legibility.
    """

    file_url: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="fileUrl")] = pydantic.Field(
        default=None
    )
    """
    A URL where the file can be downloaded from. If you use presigned URLs, we recommend an expiration time of 5-15 minutes. One of a `fileUrl` or `fileId` must be provided.
    """

    file_id: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="fileId")] = pydantic.Field(
        default=None
    )
    """
    Extend's internal ID for the file. It will always start with `file_`. One of a `fileUrl` or `fileId` must be provided. You can view a file ID from the Extend UI, for instance from running a parser or from a previous file creation. If you provide a `fileId`, any parsed data will be reused.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
