"""
Extended WorkflowRuns client with polling utilities.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    # Create and poll until completion
    result = client.workflow_runs.create_and_poll(
        file={"id": "file_xxx"},
        workflow={"id": "workflow_abc123"},
    )

    if result.status == "PROCESSED":
        print(result.step_runs)
"""

from typing import Any, Dict, Optional, Sequence

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...requests.workflow_reference import WorkflowReferenceParams
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ...types.run_secrets import RunSecrets
from ...types.workflow_run import WorkflowRun
from ...workflow_runs.client import AsyncWorkflowRunsClient, WorkflowRunsClient
from ...workflow_runs.requests.workflow_runs_create_request_file import WorkflowRunsCreateRequestFileParams
from ...workflow_runs.requests.workflow_runs_create_request_outputs_item import WorkflowRunsCreateRequestOutputsItemParams
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["WorkflowRunsWrapper", "AsyncWorkflowRunsWrapper", "PollingTimeoutError"]


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
        workflow: WorkflowReferenceParams,
        file: WorkflowRunsCreateRequestFileParams,
        outputs: Optional[Sequence[WorkflowRunsCreateRequestOutputsItemParams]] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        secrets: Optional[RunSecrets] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> WorkflowRun:
        """
        Creates a workflow run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED, NEEDS_REVIEW, REJECTED

        Args:
            workflow: Reference to the workflow to run.
            file: The file to process.
            outputs: Optional list of output configurations.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            secrets: Secret values for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final workflow run when processing is complete.

        Raises:
            PollingTimeoutError: If max_wait_ms is set and exceeded.

        Example:
            result = client.workflow_runs.create_and_poll(
                file={"id": "file_xxx"},
                workflow={"id": "workflow_abc123"}
            )

            match result.status:
                case "PROCESSED":
                    print("Success:", result.step_runs)
                case "NEEDS_REVIEW":
                    print("Needs review:", result.dashboard_url)
                case "FAILED":
                    print("Failed:", result.failure_message)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"workflow": workflow, "file": file}
        if outputs is not None:
            kwargs["outputs"] = outputs
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata
        if secrets is not None:
            kwargs["secrets"] = secrets

        # Create the workflow run
        create_response = self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
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
        workflow: WorkflowReferenceParams,
        file: WorkflowRunsCreateRequestFileParams,
        outputs: Optional[Sequence[WorkflowRunsCreateRequestOutputsItemParams]] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        secrets: Optional[RunSecrets] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> WorkflowRun:
        """
        Creates a workflow run and polls until it reaches a terminal state (async version).
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"workflow": workflow, "file": file}
        if outputs is not None:
            kwargs["outputs"] = outputs
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata
        if secrets is not None:
            kwargs["secrets"] = secrets

        # Create the workflow run
        create_response = await self.create(**kwargs)
        run_id = create_response.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.status),
            options=polling_options,
        )
