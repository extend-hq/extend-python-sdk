"""
Extended WorkflowRuns client with polling utilities.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.workflow_runs.create_and_poll(
        file={"url": "https://example.com/document.pdf"},
        workflow={"id": "workflow_abc123"},
    )

    if result.workflow_run.status == "PROCESSED":
        print(result.workflow_run.step_runs)
"""

from typing import Optional

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ...workflow_runs.client import AsyncWorkflowRunsClient, WorkflowRunsClient
from ...workflow_runs.types.workflow_runs_retrieve_response import WorkflowRunsRetrieveResponse
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["WorkflowRunsWrapper", "AsyncWorkflowRunsWrapper", "PollingTimeoutError"]

# Default maximum wait time for workflow runs (2 hours).
# Workflow runs can take significantly longer than other run types.
DEFAULT_WORKFLOW_MAX_WAIT_MS = 2 * 60 * 60 * 1000


def _is_terminal_status(status: str) -> bool:
    """
    Check if a WorkflowRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.

    Non-terminal states: PENDING, PROCESSING, CANCELLING
    Terminal states: PROCESSED, FAILED, CANCELLED, NEEDS_REVIEW, REJECTED
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class WorkflowRunsWrapper(WorkflowRunsClient):
    """
    Extended WorkflowRuns client with create_and_poll method.

    Inherits all methods from WorkflowRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: dict,
        workflow: dict,
        outputs: Optional[list] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> WorkflowRunsRetrieveResponse:
        """
        Creates a workflow run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED, NEEDS_REVIEW, REJECTED

        Note: Workflow runs can take significantly longer than other run types.
        The default max_wait_ms is 2 hours. Consider increasing this for complex
        workflows.

        Args:
            file: The file to process.
            workflow: Reference to the workflow to run.
            outputs: Optional list of output configurations.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior. Default max_wait_ms is
                           2 hours for workflow runs.

        Returns:
            The final workflow run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            result = client.workflow_runs.create_and_poll(
                file={"url": "https://example.com/doc.pdf"},
                workflow={"id": "workflow_abc123"}
            )

            match result.workflow_run.status:
                case "PROCESSED":
                    print("Success:", result.workflow_run.step_runs)
                case "NEEDS_REVIEW":
                    print("Needs review:", result.workflow_run.dashboard_url)
                case "FAILED":
                    print("Failed:", result.workflow_run.failure_message)
        """
        # Create the workflow run
        create_response = self.create(
            file=file,
            workflow=workflow,
            outputs=outputs,
            priority=priority,
            metadata=metadata,
        )
        run_id = create_response.workflow_run.id

        # Use default workflow timeout if not specified
        if polling_options is None:
            polling_options = PollingOptions(max_wait_ms=DEFAULT_WORKFLOW_MAX_WAIT_MS)
        elif polling_options.max_wait_ms == 300_000:  # Default value
            polling_options.max_wait_ms = DEFAULT_WORKFLOW_MAX_WAIT_MS

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.workflow_run.status),
            options=polling_options,
        )


class AsyncWorkflowRunsWrapper(AsyncWorkflowRunsClient):
    """
    Extended AsyncWorkflowRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: dict,
        workflow: dict,
        outputs: Optional[list] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> WorkflowRunsRetrieveResponse:
        """
        Creates a workflow run and polls until it reaches a terminal state (async version).
        """
        # Create the workflow run
        create_response = await self.create(
            file=file,
            workflow=workflow,
            outputs=outputs,
            priority=priority,
            metadata=metadata,
        )
        run_id = create_response.workflow_run.id

        # Use default workflow timeout if not specified
        if polling_options is None:
            polling_options = PollingOptions(max_wait_ms=DEFAULT_WORKFLOW_MAX_WAIT_MS)
        elif polling_options.max_wait_ms == 300_000:  # Default value
            polling_options.max_wait_ms = DEFAULT_WORKFLOW_MAX_WAIT_MS

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.workflow_run.status),
            options=polling_options,
        )
