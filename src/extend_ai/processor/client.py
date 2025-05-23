# This file was auto-generated by Fern from our API Definition.

import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from ..types.processor_type import ProcessorType
from .raw_client import AsyncRawProcessorClient, RawProcessorClient
from .types.processor_create_request_config import ProcessorCreateRequestConfig
from .types.processor_create_response import ProcessorCreateResponse
from .types.processor_update_request_config import ProcessorUpdateRequestConfig
from .types.processor_update_response import ProcessorUpdateResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ProcessorClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawProcessorClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawProcessorClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawProcessorClient
        """
        return self._raw_client

    def create(
        self,
        *,
        name: str,
        type: ProcessorType,
        clone_processor_id: typing.Optional[str] = OMIT,
        config: typing.Optional[ProcessorCreateRequestConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ProcessorCreateResponse:
        """
        Create a new processor in Extend, optionally cloning from an existing processor

        Parameters
        ----------
        name : str
            The name of the new processor

        type : ProcessorType

        clone_processor_id : typing.Optional[str]
            The ID of an existing processor to clone. One of `cloneProcessorId` or `config` must be provided.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        config : typing.Optional[ProcessorCreateRequestConfig]
            The configuration for the processor. The type of configuration must match the processor type. One of `cloneProcessorId` or `config` must be provided.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ProcessorCreateResponse
            Successfully created processor

        Examples
        --------
        from extend_ai import Extend
        client = Extend(token="YOUR_TOKEN", )
        client.processor.create(name='My Processor Name', type="EXTRACT", )
        """
        _response = self._raw_client.create(
            name=name, type=type, clone_processor_id=clone_processor_id, config=config, request_options=request_options
        )
        return _response.data

    def update(
        self,
        id: str,
        *,
        name: typing.Optional[str] = OMIT,
        config: typing.Optional[ProcessorUpdateRequestConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ProcessorUpdateResponse:
        """
        Update an existing processor in Extend

        Parameters
        ----------
        id : str
            The ID of the processor to update.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        name : typing.Optional[str]
            The new name for the processor

        config : typing.Optional[ProcessorUpdateRequestConfig]
            The new configuration for the processor. The type of configuration must match the processor type:
            * For classification processors, use `ClassificationConfig`
            * For extraction processors, use `ExtractionConfig`
            * For splitter processors, use `SplitterConfig`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ProcessorUpdateResponse
            Successfully updated processor

        Examples
        --------
        from extend_ai import Extend
        client = Extend(token="YOUR_TOKEN", )
        client.processor.update(id='processor_id_here', )
        """
        _response = self._raw_client.update(id, name=name, config=config, request_options=request_options)
        return _response.data


class AsyncProcessorClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawProcessorClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawProcessorClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawProcessorClient
        """
        return self._raw_client

    async def create(
        self,
        *,
        name: str,
        type: ProcessorType,
        clone_processor_id: typing.Optional[str] = OMIT,
        config: typing.Optional[ProcessorCreateRequestConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ProcessorCreateResponse:
        """
        Create a new processor in Extend, optionally cloning from an existing processor

        Parameters
        ----------
        name : str
            The name of the new processor

        type : ProcessorType

        clone_processor_id : typing.Optional[str]
            The ID of an existing processor to clone. One of `cloneProcessorId` or `config` must be provided.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        config : typing.Optional[ProcessorCreateRequestConfig]
            The configuration for the processor. The type of configuration must match the processor type. One of `cloneProcessorId` or `config` must be provided.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ProcessorCreateResponse
            Successfully created processor

        Examples
        --------
        from extend_ai import AsyncExtend
        import asyncio
        client = AsyncExtend(token="YOUR_TOKEN", )
        async def main() -> None:
            await client.processor.create(name='My Processor Name', type="EXTRACT", )
        asyncio.run(main())
        """
        _response = await self._raw_client.create(
            name=name, type=type, clone_processor_id=clone_processor_id, config=config, request_options=request_options
        )
        return _response.data

    async def update(
        self,
        id: str,
        *,
        name: typing.Optional[str] = OMIT,
        config: typing.Optional[ProcessorUpdateRequestConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ProcessorUpdateResponse:
        """
        Update an existing processor in Extend

        Parameters
        ----------
        id : str
            The ID of the processor to update.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        name : typing.Optional[str]
            The new name for the processor

        config : typing.Optional[ProcessorUpdateRequestConfig]
            The new configuration for the processor. The type of configuration must match the processor type:
            * For classification processors, use `ClassificationConfig`
            * For extraction processors, use `ExtractionConfig`
            * For splitter processors, use `SplitterConfig`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ProcessorUpdateResponse
            Successfully updated processor

        Examples
        --------
        from extend_ai import AsyncExtend
        import asyncio
        client = AsyncExtend(token="YOUR_TOKEN", )
        async def main() -> None:
            await client.processor.update(id='processor_id_here', )
        asyncio.run(main())
        """
        _response = await self._raw_client.update(id, name=name, config=config, request_options=request_options)
        return _response.data
