"""
Extended ExtractorVersions client with typed (pydantic) schema support.

`config["schema"]` may be a pydantic model class; it is converted to Extend's
JSON Schema format before the request is sent.
"""

import typing

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.request_options import RequestOptions
from ...extractor_versions.client import AsyncExtractorVersionsClient as GeneratedAsyncExtractorVersionsClient
from ...extractor_versions.client import ExtractorVersionsClient as GeneratedExtractorVersionsClient
from ...requests.extract_config_json import ExtractConfigJsonParams
from ...types.extractor_version import ExtractorVersion
from ...types.release_type import ReleaseType
from ...types.version_description import VersionDescription
from ..schema import TypedExtractConfigParams
from .extractors import convert_config_arg

__all__ = ["ExtractorVersionsClient", "AsyncExtractorVersionsClient"]

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)

_ConfigParam = typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams]]


class ExtractorVersionsClient(GeneratedExtractorVersionsClient):
    """
    Extended ExtractorVersions client that accepts a pydantic model class as
    `config["schema"]` in create().
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create(
        self,
        extractor_id: str,
        *,
        release_type: ReleaseType,
        extend_workspace_id: typing.Optional[str] = None,
        description: typing.Optional[VersionDescription] = OMIT,
        config: _ConfigParam = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractorVersion:
        return super().create(
            extractor_id,
            release_type=release_type,
            extend_workspace_id=extend_workspace_id,
            description=description,
            config=convert_config_arg(config),
            request_options=request_options,
        )


class AsyncExtractorVersionsClient(GeneratedAsyncExtractorVersionsClient):
    """
    Extended AsyncExtractorVersions client that accepts a pydantic model class
    as `config["schema"]` in create().
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create(
        self,
        extractor_id: str,
        *,
        release_type: ReleaseType,
        extend_workspace_id: typing.Optional[str] = None,
        description: typing.Optional[VersionDescription] = OMIT,
        config: _ConfigParam = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractorVersion:
        return await super().create(
            extractor_id,
            release_type=release_type,
            extend_workspace_id=extend_workspace_id,
            description=description,
            config=convert_config_arg(config),
            request_options=request_options,
        )
