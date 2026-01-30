"""
Extended ClassifyRuns client with polling utilities.

Example:
    from extend_ai import Extend, FileFromId

    client = Extend(token="...")

    # Create and poll until completion
    result = client.classify_runs.create_and_poll(
        file=FileFromId(id="file_xxx"),
        classifier=ClassifyRunsCreateRequestClassifier(id="classifier_abc123"),
    )

    if result.classify_run.status == "PROCESSED":
        print(result.classify_run.output)
"""

from typing import Any, Dict, Optional

from ...classify_runs.client import AsyncClassifyRunsClient, ClassifyRunsClient
from ...classify_runs.types.classify_runs_create_request_classifier import ClassifyRunsCreateRequestClassifier
from ...classify_runs.types.classify_runs_create_request_file import ClassifyRunsCreateRequestFile
from ...classify_runs.types.classify_runs_retrieve_response import ClassifyRunsRetrieveResponse
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...types.classify_config import ClassifyConfig
from ...types.run_metadata import RunMetadata
from ...types.run_priority import RunPriority
from ..polling import PollingOptions, poll_until_done, poll_until_done_async

# Re-export for convenience
from ..polling import PollingTimeoutError

__all__ = ["ClassifyRunsWrapper", "AsyncClassifyRunsWrapper", "PollingTimeoutError"]


def _is_terminal_status(status: str) -> bool:
    """
    Check if a ProcessorRunStatus is terminal (no longer processing).
    We check for non-terminal states rather than terminal states so that
    if new terminal states are added, polling will still complete.
    """
    return status not in ("PROCESSING", "PENDING", "CANCELLING")


class ClassifyRunsWrapper(ClassifyRunsClient):
    """
    Extended ClassifyRuns client with create_and_poll method.

    Inherits all methods from ClassifyRunsClient and adds create_and_poll
    for convenient polling until completion.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_and_poll(
        self,
        *,
        file: ClassifyRunsCreateRequestFile,
        classifier: Optional[ClassifyRunsCreateRequestClassifier] = None,
        config: Optional[ClassifyConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ClassifyRunsRetrieveResponse:
        """
        Creates a classify run and polls until it reaches a terminal state.

        This is a convenience method that combines create() and polling via
        retrieve() with exponential backoff and jitter.

        Terminal states: PROCESSED, FAILED, CANCELLED

        Args:
            file: The file to classify.
            classifier: Reference to an existing classifier.
            config: Inline classify configuration.
            priority: Priority of the run.
            metadata: Additional metadata for the run.
            polling_options: Options for polling behavior.

        Returns:
            The final classify run response when processing is complete.

        Raises:
            PollingTimeoutError: If the run doesn't complete within max_wait_ms.

        Example:
            from extend_ai import FileFromId
            from extend_ai.classify_runs.types import ClassifyRunsCreateRequestClassifier

            result = client.classify_runs.create_and_poll(
                file=FileFromId(id="file_xxx"),
                classifier=ClassifyRunsCreateRequestClassifier(id="classifier_abc123")
            )

            if result.classify_run.status == "PROCESSED":
                print(result.classify_run.output)
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if classifier is not None:
            kwargs["classifier"] = classifier
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the classify run
        create_response = self.create(**kwargs)
        run_id = create_response.classify_run.id

        # Poll until terminal state
        return poll_until_done(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.classify_run.status),
            options=polling_options,
        )


class AsyncClassifyRunsWrapper(AsyncClassifyRunsClient):
    """
    Extended AsyncClassifyRuns client with create_and_poll method.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def create_and_poll(
        self,
        *,
        file: ClassifyRunsCreateRequestFile,
        classifier: Optional[ClassifyRunsCreateRequestClassifier] = None,
        config: Optional[ClassifyConfig] = None,
        priority: Optional[RunPriority] = None,
        metadata: Optional[RunMetadata] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> ClassifyRunsRetrieveResponse:
        """
        Creates a classify run and polls until it reaches a terminal state (async version).
        """
        # Build kwargs, only including non-None values to avoid passing null
        kwargs: Dict[str, Any] = {"file": file}
        if classifier is not None:
            kwargs["classifier"] = classifier
        if config is not None:
            kwargs["config"] = config
        if priority is not None:
            kwargs["priority"] = priority
        if metadata is not None:
            kwargs["metadata"] = metadata

        # Create the classify run
        create_response = await self.create(**kwargs)
        run_id = create_response.classify_run.id

        # Poll until terminal state
        return await poll_until_done_async(
            retrieve=lambda: self.retrieve(run_id),
            is_terminal=lambda response: _is_terminal_status(response.classify_run.status),
            options=polling_options,
        )
