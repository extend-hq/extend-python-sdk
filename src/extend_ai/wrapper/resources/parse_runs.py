"""
Extended ParseRuns client with polling utilities.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.parse_runs.create_and_poll(
        file={"url": "https://example.com/document.pdf"},
    )

    if result.parse_run.status == "PROCESSED":
        print(result.parse_run.output)
"""

from typing import Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...parse_runs.client import AsyncParseRunsClient, ParseRunsClient
from ...parse_runs.types.parse_runs_retrieve_response import ParseRunsRetrieveResponse
from ...types.parse_config import ParseConfig
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["ParseRunsWrapper", "AsyncParseRunsWrapper", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if a ParseRunStatusEnum is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.

    Terminal states: PROCESSED, FAILED
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class ParseRunsWrapper(ParseRunsClient):
    """
    Extended ParseRuns client with create_and_poll method.

    Inherits all methods from ParseRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: dict,
        config: Optional[ParseConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ParseRunsRetrieveResponse:
        """
        Creates a parse run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED

        Args:
            file: The file to parse.
            config: Parse configuration options.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final parse run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.parse_runs.create_and_poll(
                file={"url": "https://example.com/doc.pdf"},
                config={
                    "block_options": {
                        "text": {"enabled": True},
                        "tables": {"enabled": True},
                    },
                },
            )

            if result.parse_run.status == "PROCESSED":
                print(result.parse_run.output)
        """
        # Create the parse run
        create_response = self.create(
            file=file,
            config=config,
            priority=priority,
            metadata=metadata,
        )
        run_id = create_response.parse_run.id

        # Poll until terminal state
        # Note: parse_runs.retrieve takes an optional request object as the second parameter
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.parse_run.status),
            options=polling_options,
        )


class AsyncParseRunsWrapper(AsyncParseRunsClient):
    """
    Extended AsyncParseRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: dict,
        config: Optional[ParseConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ParseRunsRetrieveResponse:
        """
        Creates a parse run and polls until it reaches a terminal state (async version).
        """
        # Create the parse run
        create_response = await self.create(
            file=file,
            config=config,
            priority=priority,
            metadata=metadata,
        )
        run_id = create_response.parse_run.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.parse_run.status),
            options=polling_options,
        )
