# This file was auto-generated by Fern from our API Definition.

import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from .raw_client import AsyncRawBatchProcessorRunClient, RawBatchProcessorRunClient
from .types.batch_processor_run_get_response import BatchProcessorRunGetResponse


class BatchProcessorRunClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawBatchProcessorRunClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawBatchProcessorRunClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawBatchProcessorRunClient
        """
        return self._raw_client

    def get(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> BatchProcessorRunGetResponse:
        """
        Retrieve details about a batch processor run, including evaluation runs

        Parameters
        ----------
        id : str
            The unique identifier of the batch processor run to retrieve. The ID will always start with "bpr_".

            Example: `"bpr_Xj8mK2pL9nR4vT7qY5wZ"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BatchProcessorRunGetResponse
            Successfully retrieved batch processor run

        Examples
        --------
        from extend_ai import Extend
        client = Extend(token="YOUR_TOKEN", )
        client.batch_processor_run.get(id='batch_processor_run_id_here', )
        """
        _response = self._raw_client.get(id, request_options=request_options)
        return _response.data


class AsyncBatchProcessorRunClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawBatchProcessorRunClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawBatchProcessorRunClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawBatchProcessorRunClient
        """
        return self._raw_client

    async def get(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BatchProcessorRunGetResponse:
        """
        Retrieve details about a batch processor run, including evaluation runs

        Parameters
        ----------
        id : str
            The unique identifier of the batch processor run to retrieve. The ID will always start with "bpr_".

            Example: `"bpr_Xj8mK2pL9nR4vT7qY5wZ"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BatchProcessorRunGetResponse
            Successfully retrieved batch processor run

        Examples
        --------
        from extend_ai import AsyncExtend
        import asyncio
        client = AsyncExtend(token="YOUR_TOKEN", )
        async def main() -> None:
            await client.batch_processor_run.get(id='batch_processor_run_id_here', )
        asyncio.run(main())
        """
        _response = await self._raw_client.get(id, request_options=request_options)
        return _response.data
