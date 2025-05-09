# Reference
<details><summary><code>client.<a href="src/extendconfig/client.py">run_workflow</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run a Workflow with files. A Workflow is a sequence of steps that process files and data in a specific order to achieve a desired outcome. A WorkflowRun will be created for each file processed. A WorkflowRun represents a single execution of a workflow against a file.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.run_workflow(
    workflow_id="workflow_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**workflow_id:** `str` 

The ID of the workflow to run. The ID will start with "workflow". This ID can be found viewing the workflow on the Extend platform.

Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**files:** `typing.Optional[typing.Sequence[File4]]` — An array of files to process through the workflow. Either the `files` array or `rawTexts` array must be provided. Supported file types can be found [here](/developers/guides/supported-file-types).
    
</dd>
</dl>

<dl>
<dd>

**raw_texts:** `typing.Optional[typing.Sequence[str]]` — An array of raw strings. Can be used in place of files when passing raw data. The raw data will be converted to `.txt` files and run through the workflow. If the data follows a specific format, it is recommended to use the files parameter instead. Either `files` or `rawTexts` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[str]` 

An optional version of the workflow that files will be run through. This number can be found when viewing the workflow on the Extend platform. When a version number is not supplied, the most recent published version of the workflow will be used. If no published versions exist, the draft version will be used. To run the `"draft"` version of a workflow, use `"draft"` as the version.

Examples:
- `"3"` - Run version 3 of the workflow
- `"draft"` - Run the draft version of the workflow
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[int]` — An optional value used to determine the relative order of WorkflowRuns when rate limiting is in effect. Lower values will be prioritized before higher values.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[JsonObject]` — A optional metadata object that can be assigned to a specific WorkflowRun to help identify it. It will be returned in the response and webhooks. You can place any arbitrary `key : value` pairs in this object.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="src/extendconfig/client.py">run_processor</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run processors (extraction, classification, splitting, etc.) on a given document.

In general, the recommended way to integrate with Extend in production is via workflows, using the [Run Workflow](/developers/api-reference/workflow-endpoints/run-workflow) endpoint. This is due to several factors:
* file parsing/pre-processing will automatically be reused across multiple processors, which will give you simplicity and cost savings given that many use cases will require multiple processors to be run on the same document.
* workflows provide dedicated human in the loop document review, when needed.
* workflows allow you to model and manage your pipeline with a single endpoint and corresponding UI for modeling and monitoring.

However, there are a number of legitimate use cases and systems where it might be easier to model the pipeline via code and run processors directly. This endpoint is provided for this purpose.

Similar to workflow runs, processor runs are asynchronous and will return a status of `PROCESSING` until the run is complete. You can [configure webhooks](/developers/webhooks/configuration) to receive notifications when a processor run is complete or failed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.run_processor(
    processor_id="processor_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**processor_id:** `ProcessorId` 
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[str]` 

An optional version of the processor to use. When not supplied, the most recent published version of the processor will be used. Special values include:
- `"latest"` for the most recent published version. If there are no published versions, the draft version will be used.
- `"draft"` for the draft version.
- Specific version numbers corresponding to versions your team has published, e.g. `"1.0"`, `"2.2"`, etc.
    
</dd>
</dl>

<dl>
<dd>

**file:** `typing.Optional[File3Processor]` — The file to be processed. One of `file` or `rawText` must be provided. Supported file types can be found [here](/developers/guides/supported-file-types).
    
</dd>
</dl>

<dl>
<dd>

**raw_text:** `typing.Optional[str]` — A raw string to be processed. Can be used in place of file when passing raw text data streams. One of `file` or `rawText` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[int]` — An optional value used to determine the relative order of ProcessorRuns when rate limiting is in effect. Lower values will be prioritized before higher values.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[JsonObject]` — An optional object that can be passed in to identify the run of the document processor. It will be returned back to you in the response and webhooks.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[RunProcessorRequestConfig]` — The configuration for the processor run. If this is provided, this config will be used. If not provided, the config for the specific version you provide will be used. The type of configuration must match the processor type.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="src/extendconfig/client.py">parse</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Parse files to get cleaned, chunked target content (e.g. markdown).

The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

Unlike processor and workflow runs, parsing is a synchronous endpoint and returns the parsed content in the response. Expected latency depends primarily on file size. This makes it suitable for workflows where you need immediate access to document content without waiting for asynchronous processing.

For more details, see the [Parse File guide](/developers/guides/parse).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend, ParseConfig, ParseRequestFile

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.parse(
    file=ParseRequestFile(),
    config=ParseConfig(),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file:** `ParseRequestFile` — A file object containing either a URL or a fileId.
    
</dd>
</dl>

<dl>
<dd>

**config:** `ParseConfig` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## WorkflowRun
<details><summary><code>client.workflow_run.<a href="src/extendconfig/workflow_run/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List runs of a Workflow. Workflows are sequences of steps that process files and data in a specific order to achieve a desired outcome. A WorkflowRun represents a single execution of a workflow against a file.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.workflow_run.list(
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**status:** `typing.Optional[WorkflowStatus]` 

Filters workflow runs by their status. If not provided, no filter is applied.

 The status of a workflow run:
 * `"PENDING"` - The workflow run has not started yet
 * `"PROCESSING"` - The workflow run is in progress
 * `"NEEDS_REVIEW"` - The workflow run requires manual review
 * `"REJECTED"` - The workflow run was rejected during manual review
 * `"PROCESSED"` - The workflow run completed successfully
 * `"FAILED"` - The workflow run encountered an error
    
</dd>
</dl>

<dl>
<dd>

**workflow_id:** `typing.Optional[str]` 

Filters workflow runs by the workflow ID. If not provided, runs for all workflows are returned. The ID will start with "workflow". This ID can be found when viewing a workflow on the Extend platform.

Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters workflow runs by the name of the file. Only returns workflow runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortByEnum]` — Sorts the workflow runs by the given field.
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDirEnum]` — Sorts the workflow runs in ascending or descending order. Ascending order means the earliest workflow run is returned first.
    
</dd>
</dl>

<dl>
<dd>

**next_page_token:** `typing.Optional[NextPageToken]` 
    
</dd>
</dl>

<dl>
<dd>

**max_page_size:** `typing.Optional[MaxPageSize]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.workflow_run.<a href="src/extendconfig/workflow_run/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Once a workflow has been run, you can check the status and output of a specific WorkflowRun.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.workflow_run.get(
    workflow_run_id="workflow_run_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**workflow_run_id:** `str` 

The ID of the WorkflowRun that was outputted after a Workflow was run through the API. The ID will start with "workflow_run". This ID can be found when creating a WorkflowRun via API, or when viewing the "history" tab of a workflow on the Extend platform.

Example: `"workflow_run_8k9m-xyzAB_Pqrst-Nvw4"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.workflow_run.<a href="src/extendconfig/workflow_run/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

You can update the name and metadata of an in progress WorkflowRun at any time using this endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.workflow_run.update(
    workflow_run_id="workflow_run_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**workflow_run_id:** `str` 

The ID of the WorkflowRun. This ID will start with "workflow_run". This ID can be found in the API response when creating a Workflow Run, or in the "history" tab of a workflow on the Extend platform.

Example: `"workflow_run_8k9m-xyzAB_Pqrst-Nvw4"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — An optional name that can be assigned to a specific WorkflowRun
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[JsonObject]` 

A metadata object that can be assigned to a specific WorkflowRun. If metadata already exists on this WorkflowRun, the newly incoming metadata will be merged with the existing metadata, with the incoming metadata taking field precedence.

You can include any arbitrary `key : value` pairs in this object.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## BatchWorkflowRun
<details><summary><code>client.batch_workflow_run.<a href="src/extendconfig/batch_workflow_run/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to efficiently initiate large batches of workflow runs in a single request (up to 1,000 in a single request, but you can queue up multiple batches in rapid succession). It accepts an array of inputs, each containing a file and metadata pair. The primary use case for this endpoint is for doing large bulk runs of >1000 files at a time that can process over the course of a few hours without needing to manage rate limits that would likely occur using the primary run endpoint.

Unlike the single [Run Workflow](/developers/api-reference/workflow-endpoints/run-workflow) endpoint which returns the details of the created workflow runs immediately, this batch endpoint returns a `batchId`.

Our recommended usage pattern is to integrate with [Webhooks](/developers/webhooks/configuration) for consuming results, using the `metadata` and `batchId` to match up results to the original inputs in your downstream systems. However, you can integrate in a polling mechanism by using a combination of the [List Workflow Runs](/developers/workflow-endpoints/list-workflow-runs) endpoint to fetch all runs via a batch, and then [Get Workflow Run](/developers/workflow-endpoints/get-workflow-run) to fetch the full outputs each run.

**Processing and Monitoring:**
Upon successful submission, the endpoint returns a `batchId`. The individual workflow runs are then queued for processing.

- **Monitoring:** Track the progress and consume results of individual runs using [Webhooks](/developers/webhooks/configuration). Subscribe to events like `workflow_run.completed`, `workflow_run.failed`, etc. The webhook payload for these events will include the corresponding `batchId` and the `metadata` you provided for each input.
- **Fetching Results:** You can also use the [List Workflow Runs](/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint and filter using the `batchId` query param.

**Error Responses**

Common errors include:

**400 Bad Request**: Invalid request body (e.g., missing required fields, array size limits exceeded, issues with `fileUrl` or `fileId`). The response body will contain an `error` message detailing the specific validation issues. Can also indicate issues accessing a provided `fileUrl`.

**401 Unauthorized**: Missing or invalid API token.

**403 Forbidden**: The API token does not have permission to access the specified workflow.

**404 Not Found**: The specified `workflowId` or `version` does not exist.

**429 Too Many Requests**: The request was rate limited. Please try again later.

**500 Internal Server Error**: An unexpected error occurred on the server.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend
from extendconfig.batch_workflow_run import (
    BatchWorkflowRunCreateRequestInputsItem,
)

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.batch_workflow_run.create(
    workflow_id="workflow_id_here",
    inputs=[BatchWorkflowRunCreateRequestInputsItem()],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**workflow_id:** `str` 

The ID of the workflow to run. This ID will start with "workflow_". This ID can be found viewing the workflow on the Extend platform.

Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**inputs:** `typing.Sequence[BatchWorkflowRunCreateRequestInputsItem]` — An array of input objects to be processed by the workflow. Each object represents a single workflow run to be created. The array must contain at least 1 input and at most 1000 inputs.
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[str]` — An optional version of the workflow to use. This can be a specific version number (e.g., `"1"`, `"2"`) found on the Extend platform, or `"draft"` to use the current unpublished draft version. When a version is not supplied, the latest deployed version of the workflow will be used. If no deployed version exists, the draft version will be used.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ProcessorRun
<details><summary><code>client.processor_run.<a href="src/extendconfig/processor_run/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a specific processor run, including its status, outputs, and any edits made during review.

A common use case for this endpoint is to poll for the status and final output of an async processor run when using the [Run Processor](/developers/api-reference/processor-endpoints/run-processor) endpoint. For instance, if you do not want to not configure webhooks to receive the output via completion/failure events.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor_run.get(
    id="processor_run_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The unique identifier for this processor run. The ID will start with "dpr_". This can be fetched from the API response when running a processor, or from the Extend UI in the "history" tab of a processor.

Example: `"dpr_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Processor
<details><summary><code>client.processor.<a href="src/extendconfig/processor/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new processor in Extend, optionally cloning from an existing processor
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor.create(
    name="My Processor Name",
    type="EXTRACT",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the new processor
    
</dd>
</dl>

<dl>
<dd>

**type:** `ProcessorType` 
    
</dd>
</dl>

<dl>
<dd>

**clone_processor_id:** `typing.Optional[str]` 

The ID of an existing processor to clone. The ID will start with "dp_". One of `cloneProcessorId` or `config` must be provided.

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorCreateRequestConfig]` — The configuration for the processor. The type of configuration must match the processor type. One of `cloneProcessorId` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**json_schema_enabled:** `typing.Optional[bool]` — Whether to enable JSON schema for the processor. Defaults to false.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.processor.<a href="src/extendconfig/processor/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing processor in Extend
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor.update(
    id="processor_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The ID of the processor to update. The ID will start with "dp_".

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name for the processor
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorUpdateRequestConfig]` 

The new configuration for the processor. The type of configuration must match the processor type:
* For classification processors, use `ClassificationConfig`
* For extraction processors, use `ExtractionConfig`
* For splitter processors, use `SplitterConfig`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ProcessorVersion
<details><summary><code>client.processor_version.<a href="src/extendconfig/processor_version/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific version of a processor in Extend
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor_version.get(
    processor_id="processor_id_here",
    processor_version_id="processor_version_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**processor_id:** `str` 

The ID of the processor. The ID will start with "dp_".

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**processor_version_id:** `str` 

The ID of the specific processor version to retrieve. The ID will start with "dpv_".

Example: `"dpv_QYk6jgHA_8CsO8rVWhyNC"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.processor_version.<a href="src/extendconfig/processor_version/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to fetch all versions of a given processor, including the current `draft` version.

Versions are typically returned in descending order of creation (newest first), but this should be confirmed in the actual implementation.
The `draft` version is the latest unpublished version of the processor, which can be published to create a new version. It might not have any changes from the last published version.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor_version.list(
    id="processor_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The ID of the processor to retrieve versions for. The ID will start with "dp_".

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.processor_version.<a href="src/extendconfig/processor_version/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to publish a new version of an existing processor. Publishing a new version creates a snapshot of the processor's current configuration and makes it available for use in workflows.

Publishing a new version does not automatically update existing workflows using this processor. You may need to manually update workflows to use the new version if desired.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.processor_version.create(
    id="processor_id_here",
    release_type="major",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The ID of the processor to publish a new version for. The ID will start with "dp_".

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**release_type:** `ProcessorVersionCreateRequestReleaseType` — The type of release for this version. The two options are "major" and "minor", which will increment the version number accordingly.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — A description of the changes in this version. This helps track the evolution of the processor over time.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorVersionCreateRequestConfig]` — The configuration for this version of the processor. The type of configuration must match the processor type.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## File
<details><summary><code>client.file.<a href="src/extendconfig/file/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List files in your account. Files represent documents that have been uploaded to Extend. This endpoint returns a paginated response. You can use the `nextPageToken` to fetch subsequent results.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.file.list(
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name_contains:** `typing.Optional[str]` 

Filters files to only include those that contain the given string in the name.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDirEnum]` — Sorts the files in ascending or descending order. Ascending order means the earliest file is returned first.
    
</dd>
</dl>

<dl>
<dd>

**next_page_token:** `typing.Optional[NextPageToken]` 
    
</dd>
</dl>

<dl>
<dd>

**max_page_size:** `typing.Optional[MaxPageSize]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.file.<a href="src/extendconfig/file/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch a file by its ID to obtain additional details and the raw file content.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.file.get(
    id="file_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

Extend's ID for the file. It will always start with `"file_"`. This ID is returned when creating a new File, or the value on the `fileId` field in a WorkflowRun.

Example: `"file_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**raw_text:** `typing.Optional[bool]` — If set to true, the raw text content of the file will be included in the response. This is useful for indexing text-based files like PDFs, Word Documents, etc.
    
</dd>
</dl>

<dl>
<dd>

**markdown:** `typing.Optional[bool]` 

If set to true, the markdown content of the file will be included in the response. This is useful for indexing very clean content into RAG pipelines for files like PDFs, Word Documents, etc.

Only available for files with a type of PDF, IMG, or .doc/.docx files that were auto-converted to PDFs.
    
</dd>
</dl>

<dl>
<dd>

**html:** `typing.Optional[bool]` 

If set to true, the html content of the file will be included in the response. This is useful for indexing html content into RAG pipelines.

Only available for files with a type of DOCX.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.file.<a href="src/extendconfig/file/client.py">upload</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upload and create a new file in Extend.

This endpoint accepts file contents and registers them as a File in Extend, which can be used for [running workflows](/developers/api-reference/workflow-endpoints/run-workflow), [creating evaluation sets](/developers/api-reference/evaluation-set-endpoints/bulk-create-evaluation-set-items), [parsing](/developers/api-reference/parse-endpoints/parse-file), etc.

If an uploaded file is detected as a Word or PowerPoint document, it will be automatically converted to a PDF.

Supported file types can be found [here](/developers/guides/supported-file-types).

This endpoint requires multipart form encoding. Most HTTP clients will handle this encoding automatically (see the examples).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.file.upload()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## FileEndpoints
<details><summary><code>client.file_endpoints.<a href="src/extendconfig/file_endpoints/client.py">create_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new file in Extend for use in an evaluation set. This endpoint is deprecated, use /files/upload instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.file_endpoints.create_file(
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the file
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` — A pre signed URL for the file
    
</dd>
</dl>

<dl>
<dd>

**raw_text:** `typing.Optional[str]` — The raw text content of the file
    
</dd>
</dl>

<dl>
<dd>

**media_type:** `typing.Optional[str]` — The media type of the file (e.g. application/pdf)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EvaluationSet
<details><summary><code>client.evaluation_set.<a href="src/extendconfig/evaluation_set/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Evaluation sets are collections of files and expected outputs that are used to evaluate the performance of a given processor in Extend. This endpoint will create a new evaluation set in Extend, which items can be added to using the [Create Evaluation Set Item](/developers/api-reference/evaluation-set-endpoints/create-evaluation-set-item) endpoint.

Note: it is not necessary to create an evaluation set via API. You can also create an evaluation set via the Extend dashboard and take the ID from there.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.evaluation_set.create(
    name="My Evaluation Set",
    description="My Evaluation Set Description",
    processor_id="processor_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` 

The name of the evaluation set.

Example: `"Invoice Processing Test Set"`
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 

A description of what this evaluation set is used for.

Example: `"Q4 2023 vendor invoices"`
    
</dd>
</dl>

<dl>
<dd>

**processor_id:** `str` 

The ID of the processor to create an evaluation set for. The ID will start with "dp_". Evaluation sets can in theory be run against any processor, but it is required to associate the evaluation set with a primary processor.

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EvaluationSetItem
<details><summary><code>client.evaluation_set_item.<a href="src/extendconfig/evaluation_set_item/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Evaluation set items are the individual files and expected outputs that are used to evaluate the performance of a given processor in Extend. This endpoint will create a new evaluation set item in Extend, which will be used during an evaluation run.

Best Practices for Outputs in Evaluation Sets:
- **Configure First, Output Later**
  - Always create and finalize your processor configuration before creating evaluation sets
  - Field IDs in outputs must match those defined in your processor configuration
- **Type Consistency**
  - Ensure output types exactly match your processor configuration
  - For example, if a field is configured as "currency", don't submit a simple number value
- **Field IDs**
  - Use the exact field IDs from your processor configuration
  - Create your own semantic IDs instead in the configs for each field/type instead of using the generated ones
- **Value**
  - Remember that all results are inside the value key of a result object, except the values within nested structures.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend, ProvidedJsonOutput

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.evaluation_set_item.create(
    evaluation_set_id="evaluation_set_id_here",
    file_id="file_id_here",
    expected_output=ProvidedJsonOutput(
        value={"key": "value"},
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**evaluation_set_id:** `str` 

The ID of the evaluation set to add the item to. The ID will start with "ev_".

Example: `"ev_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**file_id:** `str` 

Extend's internal ID for the file. It will always start with "file_".

Example: `"file_xK9mLPqRtN3vS8wF5hB2cQ"`
    
</dd>
</dl>

<dl>
<dd>

**expected_output:** `ProvidedProcessorOutput` — The expected output that will be used to evaluate the processor's performance.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.evaluation_set_item.<a href="src/extendconfig/evaluation_set_item/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

If you need to change the expected output for a given evaluation set item, you can use this endpoint to update the item. This can be useful if you need to correct an error in the expected output or if the output of the processor has changed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend, ProvidedJsonOutput

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.evaluation_set_item.update(
    id="evaluation_set_item_id_here",
    expected_output=ProvidedJsonOutput(
        value={"key": "value"},
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The ID of the evaluation set item to update. The ID will start with "evi_".

Example: `"evi_kR9mNP12Qw4yTv8BdR3H"`
    
</dd>
</dl>

<dl>
<dd>

**expected_output:** `ProvidedProcessorOutput` — The expected output of the processor when run against the file
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.evaluation_set_item.<a href="src/extendconfig/evaluation_set_item/client.py">create_batch</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

If you have a large number of files that you need to add to an evaluation set, you can use this endpoint to create multiple evaluation set items at once. This can be useful if you have a large dataset that you need to evaluate the performance of a processor against.

Note: you still need to create each File first using the file API.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend, ProvidedJsonOutput
from extendconfig.evaluation_set_item import (
    EvaluationSetItemCreateBatchRequestItemsItem,
)

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.evaluation_set_item.create_batch(
    evaluation_set_id="evaluation_set_id_here",
    items=[
        EvaluationSetItemCreateBatchRequestItemsItem(
            file_id="file_id_here",
            expected_output=ProvidedJsonOutput(
                value={"key": "value"},
            ),
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**evaluation_set_id:** `str` 

The ID of the evaluation set to add the items to. The ID will start with "ev_".

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.Sequence[EvaluationSetItemCreateBatchRequestItemsItem]` — An array of objects representing the evaluation set items to create
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## WorkflowRunOutput
<details><summary><code>client.workflow_run_output.<a href="src/extendconfig/workflow_run_output/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this endpoint to submit corrected outputs for a WorkflowRun for future processor evaluation and tuning in Extend.

If you are using our Human-in-the-loop workflow review, then we already will be collecting your operator submitted corrections. However, if you are receiving data via the API without human review, there could be incorrect outputs that you would like to correct for future usage in evaluation and tuning within the Extend platform. This endpoint allows you to submit corrected outputs for a WorkflowRun, by providing the correct output for a given output ID.

The output ID, would be found in a given entry within the outputs arrays of a Workflow Run payload. The ID would look something like `dpr_gwkZZNRrPgkjcq0y-***`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend, ProvidedJsonOutput

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.workflow_run_output.update(
    workflow_run_id="workflow_run_id_here",
    output_id="output_id_here",
    reviewed_output=ProvidedJsonOutput(
        value={"key": "value"},
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**workflow_run_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**output_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**reviewed_output:** `ProvidedProcessorOutput` 

The corrected output of the processor when run against the file.

This should conform to the output type schema of the given processor.

If this is an extraction result, you can include all fields, or just the ones that were corrected, our system will handle merges/dedupes. However, if you do include a field, we assume the value included in the final reviewed value.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## BatchProcessorRun
<details><summary><code>client.batch_processor_run.<a href="src/extendconfig/batch_processor_run/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a batch processor run, including evaluation runs
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.batch_processor_run.get(
    id="batch_processor_run_id_here",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 

The unique identifier of the batch processor run to retrieve. The ID will always start with "bpr_".

Example: `"bpr_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Workflow
<details><summary><code>client.workflow.<a href="src/extendconfig/workflow/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new workflow in Extend. Workflows are sequences of steps that process files and data in a specific order to achieve a desired outcome.

This endpoint will create a new workflow in Extend, which can then be configured and deployed. Typically, workflows are created from our UI, however this endpoint can be used to create workflows programmatically. Configuration of the flow still needs to be done in the dashboard.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from extendconfig import Extend

client = Extend(
    extend_api_version="YOUR_EXTEND_API_VERSION",
    token="YOUR_TOKEN",
)
client.workflow.create(
    name="Invoice Processing",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the workflow
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

