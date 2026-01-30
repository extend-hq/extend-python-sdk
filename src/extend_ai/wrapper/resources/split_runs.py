"""
Extended SplitRuns client with polling utilities.

Example:
    from extend_ai import Extend, FileFromId

    client = Extend(token="...")

    # Create and poll until completion
    result = client.split_runs.create_and_poll(
        file=FileFromId(id="file_xxx"),
        splitter=SplitRunsCreateRequestSplitter(id="splitter_abc123"),
    )

    if result.split_run.status == "PROCESSED":
        print(result.split_run.output)
"""

from typing import Any, Dict, Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...split_runs.client import AsyncSplitRunsClient, SplitRunsClient
from ...split_runs.types.split_runs_create_request_file import SplitRunsCreateRequestFile
from ...split_runs.types.split_runs_create_request_splitter import SplitRunsCreateRequestSplitter
from ...split_runs.types.split_runs_retrieve_response import SplitRunsRetrieveResponse
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ...types.split_config import SplitConfig
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["SplitRunsWrapper", "AsyncSplitRunsWrapper", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if a ProcessorRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class SplitRunsWrapper(SplitRunsClient):
    """
    Extended SplitRuns client with create_and_poll method.

    Inherits all methods from SplitRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: SplitRunsCreateRequestFile,
        splitter: Optional[SplitRunsCreateRequestSplitter] = None,
        config: Optional[SplitConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> SplitRunsRetrieveResponse:
        """
        Creates a split run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED

        Args:
            file: The file to split.
            splitter: Reference to an existing splitter.
            config: Inline split configuration.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final split run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            from extend_ai import FileFromId
            from extend_ai.split_runs.types import SplitRunsCreateRequestSplitter

            result = client.split_runs.create_and_poll(
                file=FileFromId(id="file_xxx"),
                splitter=SplitRunsCreateRequestSplitter(id="splitter_abc123")
            )

            if result.split_run.status == "PROCESSED":
                print(result.split_run.output)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if splitter is not None:
            kwargs["splitter"] = splitter
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the split run
        create_response = self.create(**kwargs)
        run_id = create_response.split_run.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.split_run.status),
            options=polling_options,
        )


class AsyncSplitRunsWrapper(AsyncSplitRunsClient):
    """
    Extended AsyncSplitRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: SplitRunsCreateRequestFile,
        splitter: Optional[SplitRunsCreateRequestSplitter] = None,
        config: Optional[SplitConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> SplitRunsRetrieveResponse:
        """
        Creates a split run and polls until it reaches a terminal state (async version).
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if splitter is not None:
            kwargs["splitter"] = splitter
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the split run
        create_response = await self.create(**kwargs)
        run_id = create_response.split_run.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.split_run.status),
            options=polling_options,
        )
