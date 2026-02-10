"""
Extended EditRuns client with polling utilities.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.edit_runs.create_and_poll(
        file={"id": "file_xxx"},
        config={"schema": {...}},
    )

    if result.status == "PROCESSED":
        print(result.output)
"""

from typing import Any, Dict, Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...edit_runs.client import AsyncEditRunsClient as GeneratedAsyncEditRunsClient
from ...edit_runs.client import EditRunsClient as GeneratedEditRunsClient
from ...edit_runs.requests.edit_runs_create_request_file import EditRunsCreateRequestFileParams
from ...requests.edit_config import EditConfigParams
from ...types.edit_run import EditRun
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["EditRunsClient", "AsyncEditRunsClient", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if an EditRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.

    Terminal states: PROCESSED, FAILED
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class EditRunsClient(GeneratedEditRunsClient):
    """
    Extended EditRuns client with create_and_poll method.

    Inherits all methods from EditRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: EditRunsCreateRequestFileParams,
        config: Optional[EditConfigParams] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> EditRun:
        """
        Creates an edit run and polls until it reaches a terminal state.

        Terminal states: PROCESSED, FAILED

        Args:
            file: The file to edit (must be a fillable PDF form).
            config: Edit configuration specifying the edits to make.
            polling_options: Options for polling behavior.

        Returns:
            The final edit run when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.edit_runs.create_and_poll(
                file={"id": "file_xxx"},
                config={"schema": {...}}
            )

            if result.status == "PROCESSED":
                print(result.output)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if config is not None:
            kwargs["config"] = config

        # Create the edit run
        create_response = self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
            options=polling_options,
        )


class AsyncEditRunsClient(GeneratedAsyncEditRunsClient):
    """
    Extended AsyncEditRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: EditRunsCreateRequestFileParams,
        config: Optional[EditConfigParams] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> EditRun:
        """
        Creates an edit run and polls until it reaches a terminal state (async version).
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if config is not None:
            kwargs["config"] = config

        # Create the edit run
        create_response = await self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
            options=polling_options,
        )
