"""
Extended Extractors client with typed (pydantic) schema support.

`config["schema"]` may be a pydantic model class; it is converted to Extend's
JSON Schema format before the request is sent.

Example:
    from typing import Optional
    from pydantic import BaseModel, Field
    from extend_ai import Extend

    class Invoice(BaseModel):
        invoice_number: Optional[str] = Field(None, description="The invoice number")

    client = Extend(token="...")
    extractor = client.extractors.create(
        name="Invoice Extractor",
        config={"schema": Invoice},
    )
"""

import typing

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.request_options import RequestOptions
from ...extractors.client import AsyncExtractorsClient as GeneratedAsyncExtractorsClient
from ...extractors.client import ExtractorsClient as GeneratedExtractorsClient
from ...extractors.requests.extractors_create_request_generate import ExtractorsCreateRequestGenerateParams
from ...requests.extract_config_json import ExtractConfigJsonParams
from ...types.extractor import Extractor
from ..schema import TypedExtractConfigParams, convert_typed_config, get_schema_model

__all__ = ["ExtractorsClient", "AsyncExtractorsClient"]

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)

_ConfigParam = typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams]]


def convert_config_arg(config: typing.Any) -> typing.Any:
    """Convert a pydantic model schema in a config argument, passing other values through."""
    if get_schema_model(config) is not None:
        return convert_typed_config(config)
    return config


class ExtractorsClient(GeneratedExtractorsClient):
    """
    Extended Extractors client that accepts a pydantic model class as
    `config["schema"]` in create() and update().
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create(
        self,
        *,
        name: str,
        clone_extractor_id: typing.Optional[str] = OMIT,
        config: _ConfigParam = OMIT,
        generate: typing.Optional[ExtractorsCreateRequestGenerateParams] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Extractor:
        return super().create(
            name=name,
            clone_extractor_id=clone_extractor_id,
            config=convert_config_arg(config),
            generate=generate,
            request_options=request_options,
        )

    def update(
        self,
        id: str,
        *,
        extend_workspace_id: typing.Optional[str] = None,
        name: typing.Optional[str] = OMIT,
        config: _ConfigParam = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Extractor:
        return super().update(
            id,
            extend_workspace_id=extend_workspace_id,
            name=name,
            config=convert_config_arg(config),
            request_options=request_options,
        )


class AsyncExtractorsClient(GeneratedAsyncExtractorsClient):
    """
    Extended AsyncExtractors client that accepts a pydantic model class as
    `config["schema"]` in create() and update().
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create(
        self,
        *,
        name: str,
        clone_extractor_id: typing.Optional[str] = OMIT,
        config: _ConfigParam = OMIT,
        generate: typing.Optional[ExtractorsCreateRequestGenerateParams] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Extractor:
        return await super().create(
            name=name,
            clone_extractor_id=clone_extractor_id,
            config=convert_config_arg(config),
            generate=generate,
            request_options=request_options,
        )

    async def update(
        self,
        id: str,
        *,
        extend_workspace_id: typing.Optional[str] = None,
        name: typing.Optional[str] = OMIT,
        config: _ConfigParam = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Extractor:
        return await super().update(
            id,
            extend_workspace_id=extend_workspace_id,
            name=name,
            config=convert_config_arg(config),
            request_options=request_options,
        )
