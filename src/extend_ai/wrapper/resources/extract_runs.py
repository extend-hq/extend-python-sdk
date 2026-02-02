"""
Extended ExtractRuns client with polling utilities.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.extract_runs.create_and_poll(
        file={"id": "file_xxx"},
        extractor={"id": "extractor_abc123"},
    )

    if result.extract_run.status == "PROCESSED":
        print(result.extract_run.output)
"""

from typing import Any, Dict, Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...extract_runs.client import AsyncExtractRunsClient, ExtractRunsClient
from ...extract_runs.requests.extract_runs_create_request_extractor import ExtractRunsCreateRequestExtractorParams
from ...extract_runs.requests.extract_runs_create_request_file import ExtractRunsCreateRequestFileParams
from ...extract_runs.types.extract_runs_retrieve_response import ExtractRunsRetrieveResponse
from ...requests.extract_config_json import ExtractConfigJsonParams
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["ExtractRunsWrapper", "AsyncExtractRunsWrapper", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if a ProcessorRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class ExtractRunsWrapper(ExtractRunsClient):
    """
    Extended ExtractRuns client with create_and_poll method.

    Inherits all methods from ExtractRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: ExtractRunsCreateRequestFileParams,
        extractor: Optional[ExtractRunsCreateRequestExtractorParams] = None,
        config: Optional[ExtractConfigJsonParams] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ExtractRunsRetrieveResponse:
        """
        Creates an extract run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED

        Args:
            file: The file to be extracted from. Files can be provided as a URL,
                  Extend file ID, or raw text.
            extractor: Reference to an existing extractor. One of extractor or
                      config must be provided.
            config: Inline extract configuration. One of extractor or config must
                   be provided.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior (max_wait_ms, initial_delay_ms,
                           max_delay_ms, jitter_fraction).

        Returns:
            The final extract run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.extract_runs.create_and_poll(
                file={"id": "file_xxx"},
                extractor={"id": "extractor_abc123"}
            )

            if result.extract_run.status == "PROCESSED":
                print(result.extract_run.output)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if extractor is not None:
            kwargs["extractor"] = extractor
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the extract run
        create_response = self.create(**kwargs)
        run_id = create_response.extract_run.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.extract_run.status),
            options=polling_options,
        )


class AsyncExtractRunsWrapper(AsyncExtractRunsClient):
    """
    Extended AsyncExtractRuns client with create_and_poll method.

    Inherits all methods from AsyncExtractRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: ExtractRunsCreateRequestFileParams,
        extractor: Optional[ExtractRunsCreateRequestExtractorParams] = None,
        config: Optional[ExtractConfigJsonParams] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ExtractRunsRetrieveResponse:
        """
        Creates an extract run and polls until it reaches a terminal state (async version).

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED

        Args:
            file: The file to be extracted from.
            extractor: Reference to an existing extractor.
            config: Inline extract configuration.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final extract run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if extractor is not None:
            kwargs["extractor"] = extractor
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the extract run
        create_response = await self.create(**kwargs)
        run_id = create_response.extract_run.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.extract_run.status),
            options=polling_options,
        )
