# This file was auto-generated by Fern from our API Definition.

import typing

import httpx
from .batch_processor_run.client import AsyncBatchProcessorRunClient, BatchProcessorRunClient
from .batch_workflow_run.client import AsyncBatchWorkflowRunClient, BatchWorkflowRunClient
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.request_options import RequestOptions
from .environment import ExtendEnvironment
from .evaluation_set.client import AsyncEvaluationSetClient, EvaluationSetClient
from .evaluation_set_item.client import AsyncEvaluationSetItemClient, EvaluationSetItemClient
from .file.client import AsyncFileClient, FileClient
from .processor.client import AsyncProcessorClient, ProcessorClient
from .processor_run.client import AsyncProcessorRunClient, ProcessorRunClient
from .processor_version.client import AsyncProcessorVersionClient, ProcessorVersionClient
from .raw_client import AsyncRawExtend, RawExtend
from .types.parse_config import ParseConfig
from .types.parse_request_file import ParseRequestFile
from .types.parse_response import ParseResponse
from .workflow.client import AsyncWorkflowClient, WorkflowClient
from .workflow_run.client import AsyncWorkflowRunClient, WorkflowRunClient
from .workflow_run_output.client import AsyncWorkflowRunOutputClient, WorkflowRunOutputClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class Extend:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ExtendEnvironment
        The environment to use for requests from the client. from .environment import ExtendEnvironment

        Defaults to ExtendEnvironment.PRODUCTION



    token : typing.Union[str, typing.Callable[[], str]]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 300 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    extend_api_version : typing.Optional[str]
    Examples
    --------
    from extend_ai import Extend
    client = Extend(token="YOUR_TOKEN", )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ExtendEnvironment = ExtendEnvironment.PRODUCTION,
        token: typing.Union[str, typing.Callable[[], str]],
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
        extend_api_version: typing.Optional[str] = None,
    ):
        _defaulted_timeout = (
            timeout if timeout is not None else 300 if httpx_client is None else httpx_client.timeout.read
        )
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
            extend_api_version=extend_api_version,
        )
        self._raw_client = RawExtend(client_wrapper=self._client_wrapper)
        self.workflow_run = WorkflowRunClient(client_wrapper=self._client_wrapper)
        self.batch_workflow_run = BatchWorkflowRunClient(client_wrapper=self._client_wrapper)
        self.processor_run = ProcessorRunClient(client_wrapper=self._client_wrapper)
        self.processor = ProcessorClient(client_wrapper=self._client_wrapper)
        self.processor_version = ProcessorVersionClient(client_wrapper=self._client_wrapper)
        self.file = FileClient(client_wrapper=self._client_wrapper)
        self.evaluation_set = EvaluationSetClient(client_wrapper=self._client_wrapper)
        self.evaluation_set_item = EvaluationSetItemClient(client_wrapper=self._client_wrapper)
        self.workflow_run_output = WorkflowRunOutputClient(client_wrapper=self._client_wrapper)
        self.batch_processor_run = BatchProcessorRunClient(client_wrapper=self._client_wrapper)
        self.workflow = WorkflowClient(client_wrapper=self._client_wrapper)

    @property
    def with_raw_response(self) -> RawExtend:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawExtend
        """
        return self._raw_client

    def parse(
        self,
        *,
        file: ParseRequestFile,
        config: typing.Optional[ParseConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ParseResponse:
        """
        Parse files to get cleaned, chunked target content (e.g. markdown).

        The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

        Unlike processor and workflow runs, parsing is a synchronous endpoint and returns the parsed content in the response. Expected latency depends primarily on file size. This makes it suitable for workflows where you need immediate access to document content without waiting for asynchronous processing.

        For more details, see the [Parse File guide](https://docs.extend.ai/2025-04-21/developers/guides/parse).

        Parameters
        ----------
        file : ParseRequestFile
            A file object containing either a URL or a fileId.

        config : typing.Optional[ParseConfig]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ParseResponse
            Successfully parsed file

        Examples
        --------
        from extend_ai import Extend
        from extend_ai import ParseRequestFile
        client = Extend(token="YOUR_TOKEN", )
        client.parse(file=ParseRequestFile(), )
        """
        _response = self._raw_client.parse(file=file, config=config, request_options=request_options)
        return _response.data


class AsyncExtend:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ExtendEnvironment
        The environment to use for requests from the client. from .environment import ExtendEnvironment

        Defaults to ExtendEnvironment.PRODUCTION



    token : typing.Union[str, typing.Callable[[], str]]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 300 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    extend_api_version : typing.Optional[str]
    Examples
    --------
    from extend_ai import AsyncExtend
    client = AsyncExtend(token="YOUR_TOKEN", )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ExtendEnvironment = ExtendEnvironment.PRODUCTION,
        token: typing.Union[str, typing.Callable[[], str]],
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        extend_api_version: typing.Optional[str] = None,
    ):
        _defaulted_timeout = (
            timeout if timeout is not None else 300 if httpx_client is None else httpx_client.timeout.read
        )
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
            extend_api_version=extend_api_version,
        )
        self._raw_client = AsyncRawExtend(client_wrapper=self._client_wrapper)
        self.workflow_run = AsyncWorkflowRunClient(client_wrapper=self._client_wrapper)
        self.batch_workflow_run = AsyncBatchWorkflowRunClient(client_wrapper=self._client_wrapper)
        self.processor_run = AsyncProcessorRunClient(client_wrapper=self._client_wrapper)
        self.processor = AsyncProcessorClient(client_wrapper=self._client_wrapper)
        self.processor_version = AsyncProcessorVersionClient(client_wrapper=self._client_wrapper)
        self.file = AsyncFileClient(client_wrapper=self._client_wrapper)
        self.evaluation_set = AsyncEvaluationSetClient(client_wrapper=self._client_wrapper)
        self.evaluation_set_item = AsyncEvaluationSetItemClient(client_wrapper=self._client_wrapper)
        self.workflow_run_output = AsyncWorkflowRunOutputClient(client_wrapper=self._client_wrapper)
        self.batch_processor_run = AsyncBatchProcessorRunClient(client_wrapper=self._client_wrapper)
        self.workflow = AsyncWorkflowClient(client_wrapper=self._client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawExtend:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawExtend
        """
        return self._raw_client

    async def parse(
        self,
        *,
        file: ParseRequestFile,
        config: typing.Optional[ParseConfig] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ParseResponse:
        """
        Parse files to get cleaned, chunked target content (e.g. markdown).

        The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

        Unlike processor and workflow runs, parsing is a synchronous endpoint and returns the parsed content in the response. Expected latency depends primarily on file size. This makes it suitable for workflows where you need immediate access to document content without waiting for asynchronous processing.

        For more details, see the [Parse File guide](https://docs.extend.ai/2025-04-21/developers/guides/parse).

        Parameters
        ----------
        file : ParseRequestFile
            A file object containing either a URL or a fileId.

        config : typing.Optional[ParseConfig]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ParseResponse
            Successfully parsed file

        Examples
        --------
        from extend_ai import AsyncExtend
        from extend_ai import ParseRequestFile
        import asyncio
        client = AsyncExtend(token="YOUR_TOKEN", )
        async def main() -> None:
            await client.parse(file=ParseRequestFile(), )
        asyncio.run(main())
        """
        _response = await self._raw_client.parse(file=file, config=config, request_options=request_options)
        return _response.data


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: ExtendEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
