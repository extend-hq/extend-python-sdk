"""
Extended Extend client with webhook utilities and polling methods.

This file is protected by .fernignore and will not be overwritten during regeneration.

Example:
    from extend_ai import Extend

    client = Extend(token="your-api-key")

    # Use create_and_poll for convenient polling
    extract_result = client.extract_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        extractor={"id": "extractor_123"},
    )

    classify_result = client.classify_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        classifier={"id": "classifier_123"},
    )

    workflow_result = client.workflow_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        workflow={"id": "workflow_123"},
    )

    # Verify webhooks
    event = client.webhooks.verify_and_parse(body, headers, secret)
"""

import os
import typing

import httpx
from ..batch_processor_run.client import AsyncBatchProcessorRunClient, BatchProcessorRunClient
from ..classifier_versions.client import AsyncClassifierVersionsClient, ClassifierVersionsClient
from ..classifiers.client import AsyncClassifiersClient, ClassifiersClient
from ..client import AsyncExtend as GeneratedAsyncExtend
from ..client import Extend as GeneratedExtend

# Import all client types for proper type annotations
from ..core.request_options import RequestOptions
from ..environment import ExtendEnvironment
from ..evaluation_set_items.client import AsyncEvaluationSetItemsClient, EvaluationSetItemsClient
from ..evaluation_set_runs.client import AsyncEvaluationSetRunsClient, EvaluationSetRunsClient
from ..evaluation_sets.client import AsyncEvaluationSetsClient, EvaluationSetsClient
from ..files.client import AsyncFilesClient, FilesClient
from ..processor.client import AsyncProcessorClient, ProcessorClient
from ..processor_run.client import AsyncProcessorRunClient, ProcessorRunClient
from ..processor_version.client import AsyncProcessorVersionClient, ProcessorVersionClient
from ..requests.extract_config_json import ExtractConfigJsonParams
from ..requests.extract_request_extractor import ExtractRequestExtractorParams
from ..requests.extract_request_file import ExtractRequestFileParams
from ..requests.multi_file_run_package import MultiFileRunPackageParams
from ..splitter_versions.client import AsyncSplitterVersionsClient, SplitterVersionsClient
from ..splitters.client import AsyncSplittersClient, SplittersClient
from ..types.extract_run import ExtractRun
from ..types.run_metadata import RunMetadata
from ..workflows.client import AsyncWorkflowsClient, WorkflowsClient
from .resources import (
    AsyncClassifyRunsClient,
    AsyncEditRunsClient,
    AsyncExtractorsClient,
    AsyncExtractorVersionsClient,
    AsyncExtractRunsClient,
    AsyncParseRunsClient,
    AsyncSplitRunsClient,
    AsyncWorkflowRunsClient,
    ClassifyRunsClient,
    EditRunsClient,
    ExtractorsClient,
    ExtractorVersionsClient,
    ExtractRunsClient,
    ParseRunsClient,
    SplitRunsClient,
    WorkflowRunsClient,
)
from .schema import (
    TypedExtractConfigParams,
    TypedExtractorParams,
    TypedExtractRun,
    convert_typed_config,
    convert_typed_extractor,
    get_extractor_schema_model,
    get_schema_model,
    parse_extract_run,
)
from .schema.typed_run import ModelT
from .webhooks import Webhooks

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


def _convert_extract_request(
    extractor: typing.Any, config: typing.Any
) -> typing.Tuple[typing.Any, typing.Any, typing.Optional[type]]:
    """
    Convert a pydantic model schema in an extract request's `config` or
    `extractor["override_config"]` to Extend JSON Schema. Returns the
    (possibly converted) extractor and config, and the schema model if one
    was supplied.
    """
    schema_model: typing.Optional[type] = None

    model = get_schema_model(config)
    if model is not None:
        schema_model = model
        config = convert_typed_config(config)

    model = get_extractor_schema_model(extractor)
    if model is not None:
        schema_model = model
        extractor = convert_typed_extractor(extractor)

    return extractor, config, schema_model


class Extend(GeneratedExtend):
    """
    The Extend API client with webhook utilities and polling methods.

    This client extends the generated Extend client with:
    - `create_and_poll()` methods on run resources for convenient polling
    - `webhooks` property for webhook signature verification

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ExtendEnvironment
        The environment to use for requests from the client.
        Defaults to ExtendEnvironment.PRODUCTION

    token : typing.Optional[typing.Union[str, typing.Callable[[], str]]]
        Your Extend API token. Defaults to the EXTEND_API_KEY environment variable.

    headers : typing.Optional[typing.Dict[str, str]]
        Additional headers to send with every request.

    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests.
        Default: 300 seconds.

    follow_redirects : typing.Optional[bool]
        Whether the client follows redirects.

    httpx_client : typing.Optional[httpx.Client]
        Custom httpx client to use for making requests.

    extend_api_version : typing.Optional[str]
        API version to use.

    Examples
    --------
    from extend_ai import Extend

    client = Extend(token="YOUR_TOKEN")

    # Create and poll for extract run
    result = client.extract_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        extractor={"id": "extractor_123"}
    )

    # Verify webhook signature
    event = client.webhooks.verify_and_parse(body, headers, secret)
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ExtendEnvironment = ExtendEnvironment.PRODUCTION,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
        extend_api_version: typing.Optional[str] = None,
    ):
        # Fall back to the environment like the generated client and the other
        # SDKs; the generated __init__ raises a descriptive ApiError if the
        # token is still missing.
        if token is None:
            token = os.getenv("EXTEND_API_KEY")
        super().__init__(
            base_url=base_url,
            environment=environment,
            token=token,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
            extend_api_version=extend_api_version,
        )

        # Webhook utilities
        self._webhooks = Webhooks()

        # Client instances (lazy initialization)
        self._extract_runs_client: typing.Optional[ExtractRunsClient] = None
        self._classify_runs_client: typing.Optional[ClassifyRunsClient] = None
        self._split_runs_client: typing.Optional[SplitRunsClient] = None
        self._workflow_runs_client: typing.Optional[WorkflowRunsClient] = None
        self._edit_runs_client: typing.Optional[EditRunsClient] = None
        self._parse_runs_client: typing.Optional[ParseRunsClient] = None
        self._extractors_client: typing.Optional[ExtractorsClient] = None
        self._extractor_versions_client: typing.Optional[ExtractorVersionsClient] = None

    @property
    def webhooks(self) -> Webhooks:
        """Webhook utilities for signature verification and event parsing."""
        return self._webhooks

    @typing.overload
    def extract(
        self,
        *,
        config: TypedExtractConfigParams[ModelT],
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    def extract(
        self,
        *,
        extractor: TypedExtractorParams[ModelT],
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    def extract(
        self,
        *,
        extractor: typing.Optional[ExtractRequestExtractorParams] = OMIT,
        config: typing.Optional[ExtractConfigJsonParams] = OMIT,
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractRun: ...

    def extract(
        self,
        *,
        extractor: typing.Optional[
            typing.Union[ExtractRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = OMIT,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = OMIT,
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Union[ExtractRun, TypedExtractRun[ModelT]]:
        """
        Extract structured data from a file synchronously, waiting for the result.

        In addition to the generated `extract()` behavior, `config["schema"]`
        (or `extractor["override_config"]["schema"]`) may be a pydantic model
        class. The model is converted to Extend's JSON Schema format for the
        request, and the extraction output is validated into instances of the
        model, returned as a TypedExtractRun.

        Example:
            from typing import Optional
            from pydantic import BaseModel

            class Invoice(BaseModel):
                invoice_number: Optional[str] = None

            result = client.extract(
                file={"url": "https://example.com/invoice.pdf"},
                config={"schema": Invoice},
            )
            if result.output is not None:
                print(result.output.value.invoice_number)  # typed!
        """
        converted_extractor, converted_config, schema_model = _convert_extract_request(extractor, config)
        result = super().extract(
            extractor=converted_extractor,
            config=converted_config,
            file=file,
            package=package,
            metadata=metadata,
            request_options=request_options,
        )
        if schema_model is not None:
            return parse_extract_run(result, typing.cast(typing.Type[ModelT], schema_model))
        return result

    # Run resources with create_and_poll support
    @property
    def extract_runs(self) -> ExtractRunsClient:
        """ExtractRuns client with create_and_poll method."""
        if self._extract_runs_client is None:
            self._extract_runs_client = ExtractRunsClient(client_wrapper=self._client_wrapper)
        return self._extract_runs_client

    @property
    def classify_runs(self) -> ClassifyRunsClient:
        """ClassifyRuns client with create_and_poll method."""
        if self._classify_runs_client is None:
            self._classify_runs_client = ClassifyRunsClient(client_wrapper=self._client_wrapper)
        return self._classify_runs_client

    @property
    def split_runs(self) -> SplitRunsClient:
        """SplitRuns client with create_and_poll method."""
        if self._split_runs_client is None:
            self._split_runs_client = SplitRunsClient(client_wrapper=self._client_wrapper)
        return self._split_runs_client

    @property
    def workflow_runs(self) -> WorkflowRunsClient:
        """WorkflowRuns client with create_and_poll method."""
        if self._workflow_runs_client is None:
            self._workflow_runs_client = WorkflowRunsClient(client_wrapper=self._client_wrapper)
        return self._workflow_runs_client

    @property
    def edit_runs(self) -> EditRunsClient:
        """EditRuns client with create_and_poll method."""
        if self._edit_runs_client is None:
            self._edit_runs_client = EditRunsClient(client_wrapper=self._client_wrapper)
        return self._edit_runs_client

    @property
    def parse_runs(self) -> ParseRunsClient:
        """ParseRuns client with create_and_poll method."""
        if self._parse_runs_client is None:
            self._parse_runs_client = ParseRunsClient(client_wrapper=self._client_wrapper)
        return self._parse_runs_client

    # Type-annotated properties for IDE support (delegate to parent)
    @property
    def files(self) -> FilesClient:
        """Files client."""
        return super().files  # type: ignore[return-value]

    @property
    def extractors(self) -> ExtractorsClient:
        """Extractors client with typed (pydantic) schema support."""
        if self._extractors_client is None:
            self._extractors_client = ExtractorsClient(client_wrapper=self._client_wrapper)
        return self._extractors_client

    @property
    def extractor_versions(self) -> ExtractorVersionsClient:
        """Extractor versions client with typed (pydantic) schema support."""
        if self._extractor_versions_client is None:
            self._extractor_versions_client = ExtractorVersionsClient(client_wrapper=self._client_wrapper)
        return self._extractor_versions_client

    @property
    def classifiers(self) -> ClassifiersClient:
        """Classifiers client."""
        return super().classifiers  # type: ignore[return-value]

    @property
    def classifier_versions(self) -> ClassifierVersionsClient:
        """Classifier versions client."""
        return super().classifier_versions  # type: ignore[return-value]

    @property
    def splitters(self) -> SplittersClient:
        """Splitters client."""
        return super().splitters  # type: ignore[return-value]

    @property
    def splitter_versions(self) -> SplitterVersionsClient:
        """Splitter versions client."""
        return super().splitter_versions  # type: ignore[return-value]

    @property
    def workflows(self) -> WorkflowsClient:
        """Workflows client."""
        return super().workflows  # type: ignore[return-value]

    @property
    def evaluation_sets(self) -> EvaluationSetsClient:
        """Evaluation sets client."""
        return super().evaluation_sets  # type: ignore[return-value]

    @property
    def evaluation_set_items(self) -> EvaluationSetItemsClient:
        """Evaluation set items client."""
        return super().evaluation_set_items  # type: ignore[return-value]

    @property
    def evaluation_set_runs(self) -> EvaluationSetRunsClient:
        """Evaluation set runs client."""
        return super().evaluation_set_runs  # type: ignore[return-value]

    @property
    def processor(self) -> ProcessorClient:
        """Processor client (legacy)."""
        return super().processor  # type: ignore[return-value]

    @property
    def processor_run(self) -> ProcessorRunClient:
        """Processor run client (legacy)."""
        return super().processor_run  # type: ignore[return-value]

    @property
    def processor_version(self) -> ProcessorVersionClient:
        """Processor version client (legacy)."""
        return super().processor_version  # type: ignore[return-value]

    @property
    def batch_processor_run(self) -> BatchProcessorRunClient:
        """Batch processor run client."""
        return super().batch_processor_run  # type: ignore[return-value]


class AsyncExtend(GeneratedAsyncExtend):
    """
    The async Extend API client with webhook utilities and polling methods.

    This client extends the generated AsyncExtend client with:
    - `create_and_poll()` methods on run resources for convenient polling
    - `webhooks` property for webhook signature verification

    Examples
    --------
    import asyncio
    from extend_ai import AsyncExtend

    client = AsyncExtend(token="YOUR_TOKEN")

    async def main():
        result = await client.extract_runs.create_and_poll(
            file={"url": "https://example.com/doc.pdf"},
            extractor={"id": "extractor_123"}
        )

    asyncio.run(main())
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ExtendEnvironment = ExtendEnvironment.PRODUCTION,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        extend_api_version: typing.Optional[str] = None,
    ):
        # Fall back to the environment like the generated client and the other
        # SDKs; the generated __init__ raises a descriptive ApiError if the
        # token is still missing.
        if token is None:
            token = os.getenv("EXTEND_API_KEY")
        super().__init__(
            base_url=base_url,
            environment=environment,
            token=token,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
            extend_api_version=extend_api_version,
        )

        # Webhook utilities
        self._webhooks = Webhooks()

        # Client instances (lazy initialization)
        self._extract_runs_client: typing.Optional[AsyncExtractRunsClient] = None
        self._classify_runs_client: typing.Optional[AsyncClassifyRunsClient] = None
        self._split_runs_client: typing.Optional[AsyncSplitRunsClient] = None
        self._workflow_runs_client: typing.Optional[AsyncWorkflowRunsClient] = None
        self._edit_runs_client: typing.Optional[AsyncEditRunsClient] = None
        self._parse_runs_client: typing.Optional[AsyncParseRunsClient] = None
        self._extractors_client: typing.Optional[AsyncExtractorsClient] = None
        self._extractor_versions_client: typing.Optional[AsyncExtractorVersionsClient] = None

    @property
    def webhooks(self) -> Webhooks:
        """Webhook utilities for signature verification and event parsing."""
        return self._webhooks

    @typing.overload
    async def extract(
        self,
        *,
        config: TypedExtractConfigParams[ModelT],
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    async def extract(
        self,
        *,
        extractor: TypedExtractorParams[ModelT],
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    async def extract(
        self,
        *,
        extractor: typing.Optional[ExtractRequestExtractorParams] = OMIT,
        config: typing.Optional[ExtractConfigJsonParams] = OMIT,
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractRun: ...

    async def extract(
        self,
        *,
        extractor: typing.Optional[
            typing.Union[ExtractRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = OMIT,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = OMIT,
        file: typing.Optional[ExtractRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Union[ExtractRun, TypedExtractRun[ModelT]]:
        """
        Extract structured data from a file synchronously, waiting for the result (async version).

        `config["schema"]` (or `extractor["override_config"]["schema"]`) may be
        a pydantic model class, in which case the extraction output is validated
        into instances of the model and returned as a TypedExtractRun.
        """
        converted_extractor, converted_config, schema_model = _convert_extract_request(extractor, config)
        result = await super().extract(
            extractor=converted_extractor,
            config=converted_config,
            file=file,
            package=package,
            metadata=metadata,
            request_options=request_options,
        )
        if schema_model is not None:
            return parse_extract_run(result, typing.cast(typing.Type[ModelT], schema_model))
        return result

    # Run resources with create_and_poll support
    @property
    def extract_runs(self) -> AsyncExtractRunsClient:
        """ExtractRuns client with create_and_poll method."""
        if self._extract_runs_client is None:
            self._extract_runs_client = AsyncExtractRunsClient(client_wrapper=self._client_wrapper)
        return self._extract_runs_client

    @property
    def classify_runs(self) -> AsyncClassifyRunsClient:
        """ClassifyRuns client with create_and_poll method."""
        if self._classify_runs_client is None:
            self._classify_runs_client = AsyncClassifyRunsClient(client_wrapper=self._client_wrapper)
        return self._classify_runs_client

    @property
    def split_runs(self) -> AsyncSplitRunsClient:
        """SplitRuns client with create_and_poll method."""
        if self._split_runs_client is None:
            self._split_runs_client = AsyncSplitRunsClient(client_wrapper=self._client_wrapper)
        return self._split_runs_client

    @property
    def workflow_runs(self) -> AsyncWorkflowRunsClient:
        """WorkflowRuns client with create_and_poll method."""
        if self._workflow_runs_client is None:
            self._workflow_runs_client = AsyncWorkflowRunsClient(client_wrapper=self._client_wrapper)
        return self._workflow_runs_client

    @property
    def edit_runs(self) -> AsyncEditRunsClient:
        """EditRuns client with create_and_poll method."""
        if self._edit_runs_client is None:
            self._edit_runs_client = AsyncEditRunsClient(client_wrapper=self._client_wrapper)
        return self._edit_runs_client

    @property
    def parse_runs(self) -> AsyncParseRunsClient:
        """ParseRuns client with create_and_poll method."""
        if self._parse_runs_client is None:
            self._parse_runs_client = AsyncParseRunsClient(client_wrapper=self._client_wrapper)
        return self._parse_runs_client

    # Type-annotated properties for IDE support (delegate to parent)
    @property
    def files(self) -> AsyncFilesClient:
        """Files client."""
        return super().files  # type: ignore[return-value]

    @property
    def extractors(self) -> AsyncExtractorsClient:
        """Extractors client with typed (pydantic) schema support."""
        if self._extractors_client is None:
            self._extractors_client = AsyncExtractorsClient(client_wrapper=self._client_wrapper)
        return self._extractors_client

    @property
    def extractor_versions(self) -> AsyncExtractorVersionsClient:
        """Extractor versions client with typed (pydantic) schema support."""
        if self._extractor_versions_client is None:
            self._extractor_versions_client = AsyncExtractorVersionsClient(client_wrapper=self._client_wrapper)
        return self._extractor_versions_client

    @property
    def classifiers(self) -> AsyncClassifiersClient:
        """Classifiers client."""
        return super().classifiers  # type: ignore[return-value]

    @property
    def classifier_versions(self) -> AsyncClassifierVersionsClient:
        """Classifier versions client."""
        return super().classifier_versions  # type: ignore[return-value]

    @property
    def splitters(self) -> AsyncSplittersClient:
        """Splitters client."""
        return super().splitters  # type: ignore[return-value]

    @property
    def splitter_versions(self) -> AsyncSplitterVersionsClient:
        """Splitter versions client."""
        return super().splitter_versions  # type: ignore[return-value]

    @property
    def workflows(self) -> AsyncWorkflowsClient:
        """Workflows client."""
        return super().workflows  # type: ignore[return-value]

    @property
    def evaluation_sets(self) -> AsyncEvaluationSetsClient:
        """Evaluation sets client."""
        return super().evaluation_sets  # type: ignore[return-value]

    @property
    def evaluation_set_items(self) -> AsyncEvaluationSetItemsClient:
        """Evaluation set items client."""
        return super().evaluation_set_items  # type: ignore[return-value]

    @property
    def evaluation_set_runs(self) -> AsyncEvaluationSetRunsClient:
        """Evaluation set runs client."""
        return super().evaluation_set_runs  # type: ignore[return-value]

    @property
    def processor(self) -> AsyncProcessorClient:
        """Processor client (legacy)."""
        return super().processor  # type: ignore[return-value]

    @property
    def processor_run(self) -> AsyncProcessorRunClient:
        """Processor run client (legacy)."""
        return super().processor_run  # type: ignore[return-value]

    @property
    def processor_version(self) -> AsyncProcessorVersionClient:
        """Processor version client (legacy)."""
        return super().processor_version  # type: ignore[return-value]

    @property
    def batch_processor_run(self) -> AsyncBatchProcessorRunClient:
        """Batch processor run client."""
        return super().batch_processor_run  # type: ignore[return-value]
