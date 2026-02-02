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

    if result.edit_run.status == "PROCESSED":
        print(result.edit_run.output)
"""

from typing import Any, Dict, Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...edit_runs.client import AsyncEditRunsClient, EditRunsClient
from ...edit_runs.requests.edit_runs_create_request_config import EditRunsCreateRequestConfigParams
from ...edit_runs.requests.edit_runs_create_request_file import EditRunsCreateRequestFileParams
from ...edit_runs.types.edit_runs_retrieve_response import EditRunsRetrieveResponse
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["EditRunsWrapper", "AsyncEditRunsWrapper", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if an EditRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.

    Terminal states: PROCESSED, FAILED
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class EditRunsWrapper(EditRunsClient):
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
        config: Optional[EditRunsCreateRequestConfigParams] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> EditRunsRetrieveResponse:
        """
        Creates an edit run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED

        Args:
            file: The file to edit (must be a fillable PDF form).
            config: Edit configuration specifying the edits to make.
            polling_options: Options for polling behavior.

        Returns:
            The final edit run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.edit_runs.create_and_poll(
                file={"id": "file_xxx"},
                config={"schema": {...}}
            )

            if result.edit_run.status == "PROCESSED":
                print(result.edit_run.output)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if config is not None:
            kwargs["config"] = config

        # Create the edit run
        create_response = self.create(**kwargs)
        run_id = create_response.edit_run.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.edit_run.status),
            options=polling_options,
        )


class AsyncEditRunsWrapper(AsyncEditRunsClient):
    """
    Extended AsyncEditRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: EditRunsCreateRequestFileParams,
        config: Optional[EditRunsCreateRequestConfigParams] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> EditRunsRetrieveResponse:
        """
        Creates an edit run and polls until it reaches a terminal state (async version).
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if config is not None:
            kwargs["config"] = config

        # Create the edit run
        create_response = await self.create(**kwargs)
        run_id = create_response.edit_run.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.edit_run.status),
            options=polling_options,
        )
