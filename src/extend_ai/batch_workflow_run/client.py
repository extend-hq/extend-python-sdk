# This file was auto-generated by Fern from our API Definition.

import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from .raw_client import AsyncRawBatchWorkflowRunClient, RawBatchWorkflowRunClient
from .types.batch_workflow_run_create_request_inputs_item import BatchWorkflowRunCreateRequestInputsItem
from .types.batch_workflow_run_create_response import BatchWorkflowRunCreateResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BatchWorkflowRunClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawBatchWorkflowRunClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawBatchWorkflowRunClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawBatchWorkflowRunClient
        """
        return self._raw_client

    def create(
        self,
        *,
        workflow_id: str,
        inputs: typing.Sequence[BatchWorkflowRunCreateRequestInputsItem],
        version: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BatchWorkflowRunCreateResponse:
        """
        This endpoint allows you to efficiently initiate large batches of workflow runs in a single request (up to 1,000 in a single request, but you can queue up multiple batches in rapid succession). It accepts an array of inputs, each containing a file and metadata pair. The primary use case for this endpoint is for doing large bulk runs of >1000 files at a time that can process over the course of a few hours without needing to manage rate limits that would likely occur using the primary run endpoint.

        Unlike the single [Run Workflow](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/run-workflow) endpoint which returns the details of the created workflow runs immediately, this batch endpoint returns a `batchId`.

        Our recommended usage pattern is to integrate with [Webhooks](https://docs.extend.ai/2025-04-21/developers/webhooks/configuration) for consuming results, using the `metadata` and `batchId` to match up results to the original inputs in your downstream systems. However, you can integrate in a polling mechanism by using a combination of the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint to fetch all runs via a batch, and then [Get Workflow Run](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/get-workflow-run) to fetch the full outputs each run.

        **Processing and Monitoring:**
        Upon successful submission, the endpoint returns a `batchId`. The individual workflow runs are then queued for processing.

        - **Monitoring:** Track the progress and consume results of individual runs using [Webhooks](https://docs.extend.ai/2025-04-21/developers/webhooks/configuration). Subscribe to events like `workflow_run.completed`, `workflow_run.failed`, etc. The webhook payload for these events will include the corresponding `batchId` and the `metadata` you provided for each input.
        - **Fetching Results:** You can also use the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint and filter using the `batchId` query param.

        Parameters
        ----------
        workflow_id : str
            The ID of the workflow to run. This ID will start with "workflow_". This ID can be found viewing the workflow on the Extend platform.

            Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`

        inputs : typing.Sequence[BatchWorkflowRunCreateRequestInputsItem]
            An array of input objects to be processed by the workflow. Each object represents a single workflow run to be created. The array must contain at least 1 input and at most 1000 inputs.

        version : typing.Optional[str]
            An optional version of the workflow to use. This can be a specific version number (e.g., `"1"`, `"2"`) found on the Extend platform, or `"draft"` to use the current unpublished draft version. When a version is not supplied, the latest deployed version of the workflow will be used. If no deployed version exists, the draft version will be used.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BatchWorkflowRunCreateResponse
            Successfully queued batch workflow run

        Examples
        --------
        from extend_ai import Extend
        from extend_ai.batch_workflow_run import BatchWorkflowRunCreateRequestInputsItem
        client = Extend(token="YOUR_TOKEN", )
        client.batch_workflow_run.create(workflow_id='workflow_id_here', inputs=[BatchWorkflowRunCreateRequestInputsItem()], )
        """
        _response = self._raw_client.create(
            workflow_id=workflow_id, inputs=inputs, version=version, request_options=request_options
        )
        return _response.data


class AsyncBatchWorkflowRunClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawBatchWorkflowRunClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawBatchWorkflowRunClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawBatchWorkflowRunClient
        """
        return self._raw_client

    async def create(
        self,
        *,
        workflow_id: str,
        inputs: typing.Sequence[BatchWorkflowRunCreateRequestInputsItem],
        version: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BatchWorkflowRunCreateResponse:
        """
        This endpoint allows you to efficiently initiate large batches of workflow runs in a single request (up to 1,000 in a single request, but you can queue up multiple batches in rapid succession). It accepts an array of inputs, each containing a file and metadata pair. The primary use case for this endpoint is for doing large bulk runs of >1000 files at a time that can process over the course of a few hours without needing to manage rate limits that would likely occur using the primary run endpoint.

        Unlike the single [Run Workflow](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/run-workflow) endpoint which returns the details of the created workflow runs immediately, this batch endpoint returns a `batchId`.

        Our recommended usage pattern is to integrate with [Webhooks](https://docs.extend.ai/2025-04-21/developers/webhooks/configuration) for consuming results, using the `metadata` and `batchId` to match up results to the original inputs in your downstream systems. However, you can integrate in a polling mechanism by using a combination of the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint to fetch all runs via a batch, and then [Get Workflow Run](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/get-workflow-run) to fetch the full outputs each run.

        **Processing and Monitoring:**
        Upon successful submission, the endpoint returns a `batchId`. The individual workflow runs are then queued for processing.

        - **Monitoring:** Track the progress and consume results of individual runs using [Webhooks](https://docs.extend.ai/2025-04-21/developers/webhooks/configuration). Subscribe to events like `workflow_run.completed`, `workflow_run.failed`, etc. The webhook payload for these events will include the corresponding `batchId` and the `metadata` you provided for each input.
        - **Fetching Results:** You can also use the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint and filter using the `batchId` query param.

        Parameters
        ----------
        workflow_id : str
            The ID of the workflow to run. This ID will start with "workflow_". This ID can be found viewing the workflow on the Extend platform.

            Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`

        inputs : typing.Sequence[BatchWorkflowRunCreateRequestInputsItem]
            An array of input objects to be processed by the workflow. Each object represents a single workflow run to be created. The array must contain at least 1 input and at most 1000 inputs.

        version : typing.Optional[str]
            An optional version of the workflow to use. This can be a specific version number (e.g., `"1"`, `"2"`) found on the Extend platform, or `"draft"` to use the current unpublished draft version. When a version is not supplied, the latest deployed version of the workflow will be used. If no deployed version exists, the draft version will be used.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BatchWorkflowRunCreateResponse
            Successfully queued batch workflow run

        Examples
        --------
        from extend_ai import AsyncExtend
        from extend_ai.batch_workflow_run import BatchWorkflowRunCreateRequestInputsItem
        import asyncio
        client = AsyncExtend(token="YOUR_TOKEN", )
        async def main() -> None:
            await client.batch_workflow_run.create(workflow_id='workflow_id_here', inputs=[BatchWorkflowRunCreateRequestInputsItem()], )
        asyncio.run(main())
        """
        _response = await self._raw_client.create(
            workflow_id=workflow_id, inputs=inputs, version=version, request_options=request_options
        )
        return _response.data
