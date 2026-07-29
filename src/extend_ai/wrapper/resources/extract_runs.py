"""
Extended ExtractRuns client with polling utilities and typed schemas.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.extract_runs.create_and_poll(
        file={"id": "file_xxx"},
        extractor={"id": "extractor_abc123"},
    )

    if result.status == "PROCESSED":
        print(result.output)

    # Or pass a pydantic model as the schema for typed output
    from typing import Optional
    from pydantic import BaseModel

    class Invoice(BaseModel):
        invoice_number: Optional[str] = None

    result = client.extract_runs.create_and_poll(
        file={"id": "file_xxx"},
        config={"schema": Invoice},
    )
    if result.output is not None:
        print(result.output.value.invoice_number)  # typed!
"""

import typing

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.request_options import RequestOptions
from ...extract_runs.client import AsyncExtractRunsClient as GeneratedAsyncExtractRunsClient
from ...extract_runs.client import ExtractRunsClient as GeneratedExtractRunsClient
from ...extract_runs.requests.extract_runs_create_request_extractor import ExtractRunsCreateRequestExtractorParams
from ...extract_runs.requests.extract_runs_create_request_file import ExtractRunsCreateRequestFileParams
from ...requests.extract_config_json import ExtractConfigJsonParams
from ...requests.multi_file_run_package import MultiFileRunPackageParams
from ...types.extract_run import ExtractRun
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority

# Re-export for convenience
from ..polling import PollingOptions, PollingTimeoutError, poll_until_done, poll_until_done_async
from ..schema import (
    TypedExtractConfigParams,
    TypedExtractorParams,
    TypedExtractRun,
    convert_typed_config,
    convert_typed_extractor,
    get_extractor_schema_model,
    get_schema_model,
    parse_extract_run,
)
from ..schema.typed_run import ModelT

__all__ = ["ExtractRunsClient", "AsyncExtractRunsClient", "PollingTimeoutError"]

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


def _convert_create_args(extractor: typing.Any, config: typing.Any) -> typing.Tuple[typing.Any, typing.Any]:
    """Convert a pydantic model schema in create() arguments, passing other values through."""
    if get_schema_model(config) is not None:
        config = convert_typed_config(config)
    if get_extractor_schema_model(extractor) is not None:
        extractor = convert_typed_extractor(extractor)
    return extractor, config


def _is_terminal_status(status: str) -> bool:
    """
    Check if a ProcessorRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


def _build_create_kwargs(
    *,
    file: typing.Optional[ExtractRunsCreateRequestFileParams],
    package: typing.Optional[MultiFileRunPackageParams],
    extractor: typing.Any,
    config: typing.Any,
    priority: typing.Optional[RunPriority],
    metadata: typing.Optional[RunMetadata],
) -> typing.Tuple[typing.Dict[str, typing.Any], typing.Optional[type]]:
    """
    Build create() kwargs (omitting None values), converting any pydantic model
    schema to Extend JSON Schema. Returns the kwargs and the schema model, if
    one was supplied.
    """
    schema_model: typing.Optional[type] = None

    if config is not None:
        model = get_schema_model(config)
        if model is not None:
            schema_model = model
            config = convert_typed_config(config)

    if extractor is not None:
        model = get_extractor_schema_model(extractor)
        if model is not None:
            schema_model = model
            extractor = convert_typed_extractor(extractor)

    kwargs: typing.Dict[str, typing.Any] = {}
    if file is not None:
        kwargs["file"] = file
    if package is not None:
        kwargs["package"] = package
    if extractor is not None:
        kwargs["extractor"] = extractor
    if config is not None:
        kwargs["config"] = config
    if priority is not None:
        kwargs["priority"] = priority
    if metadata is not None:
        kwargs["metadata"] = metadata

    return kwargs, schema_model


class ExtractRunsClient(GeneratedExtractRunsClient):
    """
    Extended ExtractRuns client with create_and_poll method.

    Inherits all methods from ExtractRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create(
        self,
        *,
        extractor: typing.Optional[
            typing.Union[ExtractRunsCreateRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = OMIT,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = OMIT,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        priority: typing.Optional[RunPriority] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractRun:
        """
        Create an extract run. See the generated client for full documentation.

        `config["schema"]` (or `extractor["override_config"]["schema"]`) may be a
        pydantic model class; it is converted to Extend's JSON Schema format before
        the request is sent. Note that `create()` returns immediately without
        output — for validated, typed output use `create_and_poll()` or
        `client.extract()` instead.
        """
        converted_extractor, converted_config = _convert_create_args(extractor, config)
        return super().create(
            extractor=converted_extractor,
            config=converted_config,
            file=file,
            package=package,
            priority=priority,
            metadata=metadata,
            request_options=request_options,
        )

    @typing.overload
    def create_and_poll(
        self,
        *,
        config: TypedExtractConfigParams[ModelT],
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    def create_and_poll(
        self,
        *,
        extractor: TypedExtractorParams[ModelT],
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    def create_and_poll(
        self,
        *,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        extractor: typing.Optional[ExtractRunsCreateRequestExtractorParams] = None,
        config: typing.Optional[ExtractConfigJsonParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> ExtractRun: ...

    def create_and_poll(
        self,
        *,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        extractor: typing.Optional[
            typing.Union[ExtractRunsCreateRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = None,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> typing.Union[ExtractRun, TypedExtractRun[ModelT]]:
        """
        Creates an extract run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED

        Args:
            file: The file to be extracted from. Mutually exclusive with
                `package` — provide one or the other.
            package: A package of files for multi-file extraction. Mutually
                exclusive with `file` — provide one or the other.
            extractor: Reference to an existing extractor.
            config: Inline extract configuration. `config["schema"]` may be a
                pydantic model class, in which case the extraction output is
                validated into instances of that model.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final extract run when processing is complete. If a pydantic
            model was supplied as the schema, a TypedExtractRun whose output
            values are instances of the model.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.extract_runs.create_and_poll(
                file={"id": "file_xxx"},
                extractor={"id": "extractor_abc123"}
            )

            if result.status == "PROCESSED":
                print(result.output)
        """
        kwargs, schema_model = _build_create_kwargs(
            file=file, package=package, extractor=extractor, config=config, priority=priority, metadata=metadata
        )

        # Create the extract run
        create_response = self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        result = poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
            options=polling_options,
        )

        if schema_model is not None:
            return parse_extract_run(result, typing.cast(typing.Type[ModelT], schema_model))
        return result


class AsyncExtractRunsClient(GeneratedAsyncExtractRunsClient):
    """
    Extended AsyncExtractRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create(
        self,
        *,
        extractor: typing.Optional[
            typing.Union[ExtractRunsCreateRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = OMIT,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = OMIT,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = OMIT,
        package: typing.Optional[MultiFileRunPackageParams] = OMIT,
        priority: typing.Optional[RunPriority] = OMIT,
        metadata: typing.Optional[RunMetadata] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExtractRun:
        """
        Create an extract run (async version). See the generated client for full
        documentation.

        `config["schema"]` (or `extractor["override_config"]["schema"]`) may be a
        pydantic model class; it is converted to Extend's JSON Schema format before
        the request is sent. Note that `create()` returns immediately without
        output — for validated, typed output use `create_and_poll()` or
        `client.extract()` instead.
        """
        converted_extractor, converted_config = _convert_create_args(extractor, config)
        return await super().create(
            extractor=converted_extractor,
            config=converted_config,
            file=file,
            package=package,
            priority=priority,
            metadata=metadata,
            request_options=request_options,
        )

    @typing.overload
    async def create_and_poll(
        self,
        *,
        config: TypedExtractConfigParams[ModelT],
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    async def create_and_poll(
        self,
        *,
        extractor: TypedExtractorParams[ModelT],
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> TypedExtractRun[ModelT]: ...

    @typing.overload
    async def create_and_poll(
        self,
        *,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        extractor: typing.Optional[ExtractRunsCreateRequestExtractorParams] = None,
        config: typing.Optional[ExtractConfigJsonParams] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> ExtractRun: ...

    async def create_and_poll(
        self,
        *,
        file: typing.Optional[ExtractRunsCreateRequestFileParams] = None,
        package: typing.Optional[MultiFileRunPackageParams] = None,
        extractor: typing.Optional[
            typing.Union[ExtractRunsCreateRequestExtractorParams, TypedExtractorParams[ModelT]]
        ] = None,
        config: typing.Optional[typing.Union[ExtractConfigJsonParams, TypedExtractConfigParams[ModelT]]] = None,
        priority: typing.Optional[RunPriority] = None,
        metadata: typing.Optional[RunMetadata] = None,
        polling_options: typing.Optional[PollingOptions] = None,
    ) -> typing.Union[ExtractRun, TypedExtractRun[ModelT]]:
        """
        Creates an extract run and polls until it reaches a terminal state (async version).

        `file` and `package` are mutually exclusive — provide one or the other.
        `config["schema"]` may be a pydantic model class, in which case the
        extraction output is validated into instances of that model.
        """
        kwargs, schema_model = _build_create_kwargs(
            file=file, package=package, extractor=extractor, config=config, priority=priority, metadata=metadata
        )

        # Create the extract run
        create_response = await self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        result = await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
            options=polling_options,
        )

        if schema_model is not None:
            return parse_extract_run(result, typing.cast(typing.Type[ModelT], schema_model))
        return result
