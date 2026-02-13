# Reference
<details><summary><code>client.<a href="src/extend_ai/client.py">parse</a>(...) -&gt; AsyncHttpResponse[ParserRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Parse files to get cleaned, chunked target content (e.g. markdown).

The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

For more details, see the [Parse File guide](/product/parsing/parse).
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
from extend_ai import Extend, ParseRequestFile

client = Extend(
    token="YOUR_TOKEN",
)
client.parse(
    response_type="json",
    file=ParseRequestFile(),
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

**response_type:** `typing.Optional[ParseRequestResponseType]` 

Controls the format of the response chunks. Defaults to `json` if not specified.
* `json` - Returns parsed outputs in the response body
* `url` - Return a presigned URL to the parsed content in the response body
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ParseConfig]` 
    
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

<details><summary><code>client.<a href="src/extend_ai/client.py">parse_async</a>(...) -&gt; AsyncHttpResponse[ParserRunStatus]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Parse files **asynchronously** to get cleaned, chunked target content (e.g. markdown).

The Parse Async endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

Parse files asynchronously and get a parser run ID that can be used to check status and retrieve results with the [Get Parser Run](https://docs.extend.ai/2025-04-21/developers/api-reference/parse-endpoints/get-parser-run) endpoint.

This is useful for:
* Large files that may take longer to process
* Avoiding timeout issues with synchronous parsing.

For more details, see the [Parse File guide](/product/parsing/parse).
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
from extend_ai import Extend, ParseAsyncRequestFile

client = Extend(
    token="YOUR_TOKEN",
)
client.parse_async(
    file=ParseAsyncRequestFile(),
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

**file:** `ParseAsyncRequestFile` — A file object containing either a URL or a fileId.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ParseConfig]` 
    
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
<details><summary><code>client.file.<a href="src/extend_ai/file/client.py">list</a>(...) -&gt; AsyncHttpResponse[FileListResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.file.list(
    name_contains="nameContains",
    sort_dir="asc",
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
    max_page_size=1,
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

<details><summary><code>client.file.<a href="src/extend_ai/file/client.py">get</a>(...) -&gt; AsyncHttpResponse[FileGetResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.file.get(
    id="file_id_here",
    raw_text=True,
    markdown=True,
    html=True,
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

<details><summary><code>client.file.<a href="src/extend_ai/file/client.py">delete</a>(...) -&gt; AsyncHttpResponse[FileDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a file and all associated data from Extend. This operation is permanent and cannot be undone.

This endpoint can be used if you'd like to manage data retention on your own rather than automated data retention policies. Or make one-off deletions for your downstream customers.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.file.delete(
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

The ID of the file to delete.

Example: `"file_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

<details><summary><code>client.file.<a href="src/extend_ai/file/client.py">upload</a>(...) -&gt; AsyncHttpResponse[FileUploadResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upload and create a new file in Extend.

This endpoint accepts file contents and registers them as a File in Extend, which can be used for [running workflows](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/run-workflow), [creating evaluation set items](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/bulk-create-evaluation-set-items), [parsing](https://docs.extend.ai/2025-04-21/developers/api-reference/parse-endpoints/parse-file), etc.

If an uploaded file is detected as a Word or PowerPoint document, it will be automatically converted to a PDF.

Supported file types can be found [here](/product/general/supported-file-types).

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
from extend_ai import Extend

client = Extend(
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

## ParserRun
<details><summary><code>client.parser_run.<a href="src/extend_ai/parser_run/client.py">get</a>(...) -&gt; AsyncHttpResponse[ParserRunGetResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the status and results of a parser run.

Use this endpoint to get results for a parser run that has already completed, or to check on the status of an asynchronous parser run initiated via the [Parse File Asynchronously](https://docs.extend.ai/2025-04-21/developers/api-reference/parse-endpoints/parse-file-async) endpoint.

If parsing is still in progress, you'll receive a response with just the status. Once complete, you'll receive the full parsed content in the response.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.parser_run.get(
    id="parser_run_id_here",
    response_type="json",
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

The unique identifier for the parser run.

Example: `"parser_run_xK9mLPqRtN3vS8wF5hB2cQ"`
    
</dd>
</dl>

<dl>
<dd>

**response_type:** `typing.Optional[ParserRunGetRequestResponseType]` 

Controls the format of the response chunks. Defaults to `json` if not specified.
* `json` - Returns chunks with inline content
* `url` - Returns chunks with presigned URLs to content instead of inline data
    
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

<details><summary><code>client.parser_run.<a href="src/extend_ai/parser_run/client.py">delete</a>(...) -&gt; AsyncHttpResponse[ParserRunDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a parser run and all associated data from Extend. This operation is permanent and cannot be undone.

This endpoint can be used if you'd like to manage data retention on your own rather than automated data retention policies. Or make one-off deletions for your downstream customers.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.parser_run.delete(
    id="parser_run_id_here",
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

The ID of the parser run to delete.

Example: `"parser_run_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

## Edit
<details><summary><code>client.edit.<a href="src/extend_ai/edit/client.py">create</a>(...) -&gt; AsyncHttpResponse[EditRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit and manipulate PDF documents by detecting and filling form fields.
This is a synchronous endpoint that will wait for the edit operation to complete (up to 5 minutes) before returning results. For longer operations, use the [Edit File Async](/developers/api-reference/edit-endpoints/edit-file-async) endpoint.
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
from extend_ai import Extend
from extend_ai.edit import EditCreateRequestFile

client = Extend(
    token="YOUR_TOKEN",
)
client.edit.create(
    file=EditCreateRequestFile(),
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

**file:** `EditCreateRequestFile` — A file object containing either a URL or a fileId.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[EditCreateRequestConfig]` — Configuration for the edit operation. Field values should be specified using `extend_edit:value` on each field in the schema.
    
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

<details><summary><code>client.edit.<a href="src/extend_ai/edit/client.py">create_async</a>(...) -&gt; AsyncHttpResponse[EditRunStatus]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit and manipulate PDF documents **asynchronously** by filling forms, adding/modifying text fields, and applying structured changes.

The Edit Async endpoint allows you to convert and edit documents asynchronously and get an edit run ID that can be used to check status and retrieve results with the [Get Edit Run](/developers/api-reference/edit-endpoints/get-edit-run) endpoint.

This is useful for:
* Large files that may take longer to process
* Avoiding timeout issues with synchronous editing
* Processing multiple files in parallel
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
from extend_ai import Extend
from extend_ai.edit import EditCreateAsyncRequestFile

client = Extend(
    token="YOUR_TOKEN",
)
client.edit.create_async(
    file=EditCreateAsyncRequestFile(),
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

**file:** `EditCreateAsyncRequestFile` — A file object containing either a URL or a fileId.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[EditCreateAsyncRequestConfig]` — Configuration for the edit operation. Field values should be specified using `extend_edit:value` on each field in the schema.
    
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

<details><summary><code>client.edit.<a href="src/extend_ai/edit/client.py">get</a>(...) -&gt; AsyncHttpResponse[EditGetResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the status and results of an edit run.

Use this endpoint to get results for an edit run that has already completed, or to check on the status of an asynchronous edit run initiated via the [Edit File Asynchronously](/developers/api-reference/edit-endpoints/edit-file-async) endpoint.

If editing is still in progress, you'll receive a response with just the status. Once complete, you'll receive the full edited file information in the response.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.edit.get(
    id="edit_run_id_here",
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

The unique identifier for the edit run.

Example: `"edit_run_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

<details><summary><code>client.edit.<a href="src/extend_ai/edit/client.py">delete</a>(...) -&gt; AsyncHttpResponse[EditDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an edit run and all associated data from Extend. This operation is permanent and cannot be undone.

This endpoint can be used if you'd like to manage data retention on your own rather than relying on automated data retention policies, or to make one-off deletions for your downstream customers.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.edit.delete(
    id="edit_run_id_here",
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

The ID of the edit run to delete.

Example: `"edit_run_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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
<details><summary><code>client.workflow.<a href="src/extend_ai/workflow/client.py">create</a>(...) -&gt; AsyncHttpResponse[WorkflowCreateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

## WorkflowRun
<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">list</a>(...) -&gt; AsyncHttpResponse[WorkflowRunListResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.workflow_run.list(
    status="PENDING",
    workflow_id="workflowId",
    batch_id="batchId",
    file_name_contains="fileNameContains",
    sort_by="updatedAt",
    sort_dir="asc",
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
    max_page_size=1,
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
 * `"CANCELLED"` - The workflow run was cancelled
 * `"CANCELLING"` - The workflow run is being cancelled
    
</dd>
</dl>

<dl>
<dd>

**workflow_id:** `typing.Optional[str]` 

Filters workflow runs by the workflow ID. If not provided, runs for all workflows are returned.

Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**batch_id:** `typing.Optional[str]` 

Filters workflow runs by the batch ID. This is useful for fetching all runs for a given batch created via the [Batch Run Workflow](/developers/api-reference/workflow-endpoints/batch-run-workflow) endpoint.

Example: `"batch_7Ws31-F5"`
    
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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">create</a>(...) -&gt; AsyncHttpResponse[WorkflowRunCreateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.workflow_run.create(
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

The ID of the workflow to run.

Example: `"workflow_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**files:** `typing.Optional[typing.Sequence[WorkflowRunFileInput]]` — An array of files to process through the workflow. Either the `files` array or `rawTexts` array must be provided. Supported file types can be found [here](/product/general/supported-file-types). There is a limit if 50 files that can be processed at once using this endpoint. If you wish to process more at a time, consider using the [Batch Run Workflow](/developers/api-reference/workflow-endpoints/batch-run-workflow) endpoint.
    
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

**metadata:** `typing.Optional[JsonObject]` 

An optional metadata object that can be assigned to a specific WorkflowRun to help identify it. It will be returned in the response and webhooks. You can place any arbitrary `key : value` pairs in this object.

To categorize workflow runs for billing and usage tracking, include `extend:usage_tags` with an array of string values (e.g., `{"extend:usage_tags": ["production", "team-eng", "customer-123"]}`). Tags must contain only alphanumeric characters, hyphens, and underscores; any special characters will be automatically removed.
    
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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">get</a>(...) -&gt; AsyncHttpResponse[WorkflowRunGetResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of the WorkflowRun that was outputted after a Workflow was run through the API.

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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">update</a>(...) -&gt; AsyncHttpResponse[WorkflowRunUpdateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

To categorize workflow runs for billing and usage tracking, include `extend:usage_tags` with an array of string values (e.g., `{"extend:usage_tags": ["production", "team-eng", "customer-123"]}`). Tags must contain only alphanumeric characters, hyphens, and underscores; any special characters will be automatically removed.
    
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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">delete</a>(...) -&gt; AsyncHttpResponse[WorkflowRunDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a workflow run and all associated data from Extend. This operation is permanent and cannot be undone.

This endpoint can be used if you'd like to manage data retention on your own rather than automated data retention policies. Or make one-off deletions for your downstream customers.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.workflow_run.delete(
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

The ID of the workflow run to delete.

Example: `"workflow_run_xKm9pNv3qWsY_jL2tR5Dh"`
    
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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[WorkflowRunCancelResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel a running workflow run by its ID. This endpoint allows you to stop a workflow run that is currently in progress.

Note: Only workflow runs with a status of `PROCESSING` or `PENDING` can be cancelled. Workflow runs that are completed, failed, in review, rejected, or already cancelled cannot be cancelled.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.workflow_run.cancel(
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

The ID of the workflow run to cancel.

Example: `"workflow_run_xKm9pNv3qWsY_jL2tR5Dh"`
    
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
<details><summary><code>client.batch_workflow_run.<a href="src/extend_ai/batch_workflow_run/client.py">create</a>(...) -&gt; AsyncHttpResponse[BatchWorkflowRunCreateResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to efficiently initiate large batches of workflow runs in a single request (up to 1,000 in a single request, but you can queue up multiple batches in rapid succession). It accepts an array of inputs, each containing a file and metadata pair. The primary use case for this endpoint is for doing large bulk runs of >1000 files at a time that can process over the course of a few hours without needing to manage rate limits that would likely occur using the primary run endpoint.

Unlike the single [Run Workflow](/developers/api-reference/workflow-endpoints/run-workflow) endpoint which returns the details of the created workflow runs immediately, this batch endpoint returns a `batchId`.

Our recommended usage pattern is to integrate with [Webhooks](/product/webhooks/configuration) for consuming results, using the `metadata` and `batchId` to match up results to the original inputs in your downstream systems. However, you can integrate in a polling mechanism by using a combination of the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint to fetch all runs via a batch, and then [Get Workflow Run](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/get-workflow-run) to fetch the full outputs each run.

**Priority:** All workflow runs created through this batch endpoint are automatically assigned a priority of 90.

**Processing and Monitoring:**
Upon successful submission, the endpoint returns a `batchId`. The individual workflow runs are then queued for processing.

- **Monitoring:** Track the progress and consume results of individual runs using [Webhooks](/product/webhooks/configuration). Subscribe to events like `workflow_run.completed`, `workflow_run.failed`, etc. The webhook payload for these events will include the corresponding `batchId` and the `metadata` you provided for each input.
- **Fetching Results:** You can also use the [List Workflow Runs](https://docs.extend.ai/2025-04-21/developers/api-reference/workflow-endpoints/list-workflow-runs) endpoint and filter using the `batchId` query param.
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
from extend_ai import Extend
from extend_ai.batch_workflow_run import BatchWorkflowRunCreateRequestInputsItem

client = Extend(
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

## BatchProcessorRun
<details><summary><code>client.batch_processor_run.<a href="src/extend_ai/batch_processor_run/client.py">get</a>(...) -&gt; AsyncHttpResponse[BatchProcessorRunGetResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

## EvaluationSet
<details><summary><code>client.evaluation_set.<a href="src/extend_ai/evaluation_set/client.py">list</a>(...) -&gt; AsyncHttpResponse[EvaluationSetListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List evaluation sets in your account. You can use the `processorId` parameter to filter evaluation sets by processor. 

This endpoint returns a paginated response. You can use the `nextPageToken` to fetch subsequent results.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.evaluation_set.list(
    processor_id="processor_id_here",
    sort_by="updatedAt",
    sort_dir="asc",
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
    max_page_size=1,
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

**processor_id:** `typing.Optional[str]` 

The ID of the processor to filter evaluation sets by.

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortByEnum]` — Sorts the evaluation sets by the given field.
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDirEnum]` — Sorts the evaluation sets in ascending or descending order. Ascending order means the earliest evaluation set is returned first.
    
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

<details><summary><code>client.evaluation_set.<a href="src/extend_ai/evaluation_set/client.py">create</a>(...) -&gt; AsyncHttpResponse[EvaluationSetCreateResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Evaluation sets are collections of files and expected outputs that are used to evaluate the performance of a given processor in Extend. This endpoint will create a new evaluation set in Extend, which items can be added to using the [Create Evaluation Set Item](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/create-evaluation-set-item) endpoint.

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
from extend_ai import Extend

client = Extend(
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

The ID of the processor to create an evaluation set for. Evaluation sets can in theory be run against any processor, but it is required to associate the evaluation set with a primary processor.

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

<details><summary><code>client.evaluation_set.<a href="src/extend_ai/evaluation_set/client.py">get</a>(...) -&gt; AsyncHttpResponse[EvaluationSetGetResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific evaluation set by ID. This returns an evaluation set object, but does not include the items in the evaluation set. You can use the [List Evaluation Set Items](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/list-evaluation-set-items) endpoint to get the items in an evaluation set.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.evaluation_set.get(
    id="evaluation_set_id_here",
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

The ID of the evaluation set to retrieve.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
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
<details><summary><code>client.evaluation_set_item.<a href="src/extend_ai/evaluation_set_item/client.py">list</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all items in a specific evaluation set. Evaluation set items are the individual files and expected outputs that are used to evaluate the performance of a given processor in Extend. 

This endpoint returns a paginated response. You can use the `nextPageToken` to fetch subsequent results.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.evaluation_set_item.list(
    id="evaluation_set_id_here",
    sort_by="updatedAt",
    sort_dir="asc",
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
    max_page_size=1,
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

The ID of the evaluation set to retrieve items for.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortByEnum]` — Sorts the evaluation set items by the given field.
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDirEnum]` — Sorts the evaluation set items in ascending or descending order. Ascending order means the earliest evaluation set is returned first.
    
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

<details><summary><code>client.evaluation_set_item.<a href="src/extend_ai/evaluation_set_item/client.py">create</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemCreateResponse]</code></summary>
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
from extend_ai import Extend, ProvidedJsonOutput

client = Extend(
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

The ID of the evaluation set to add the item to.

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

<details><summary><code>client.evaluation_set_item.<a href="src/extend_ai/evaluation_set_item/client.py">update</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemUpdateResponse]</code></summary>
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
from extend_ai import Extend, ProvidedJsonOutput

client = Extend(
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

The ID of the evaluation set item to update.

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

<details><summary><code>client.evaluation_set_item.<a href="src/extend_ai/evaluation_set_item/client.py">delete</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an evaluation set item from an evaluation set. This operation is permanent and cannot be undone.

This endpoint can be used to remove individual items from an evaluation set when they are no longer needed or if they were added in error.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.evaluation_set_item.delete(
    id="evaluation_set_item_id_here",
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

The ID of the evaluation set item to delete.

Example: `"evi_kR9mNP12Qw4yTv8BdR3H"`
    
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

<details><summary><code>client.evaluation_set_item.<a href="src/extend_ai/evaluation_set_item/client.py">create_batch</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemCreateBatchResponse]</code></summary>
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
from extend_ai import Extend, ProvidedJsonOutput
from extend_ai.evaluation_set_item import (
    EvaluationSetItemCreateBatchRequestItemsItem,
)

client = Extend(
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

The ID of the evaluation set to add the items to.

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

## ProcessorRun
<details><summary><code>client.processor_run.<a href="src/extend_ai/processor_run/client.py">list</a>(...) -&gt; AsyncHttpResponse[ProcessorRunListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List runs of a Processor. A ProcessorRun represents a single execution of a processor against a file.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.processor_run.list(
    status="PENDING",
    processor_id="processorId",
    processor_type="EXTRACT",
    source_id="sourceId",
    source="ADMIN",
    file_name_contains="fileNameContains",
    sort_by="updatedAt",
    sort_dir="asc",
    next_page_token="xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=",
    max_page_size=1,
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

**status:** `typing.Optional[ProcessorStatus]` 

Filters processor runs by their status. If not provided, no filter is applied.

 The status of a processor run:
 * `"PENDING"` - The processor run has not started yet
 * `"PROCESSING"` - The processor run is in progress
 * `"PROCESSED"` - The processor run completed successfully
 * `"FAILED"` - The processor run encountered an error
 * `"CANCELLED"` - The processor run was cancelled
    
</dd>
</dl>

<dl>
<dd>

**processor_id:** `typing.Optional[str]` 

Filters processor runs by the processor ID. If not provided, runs for all processors are returned.

Example: `"dp_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**processor_type:** `typing.Optional[ProcessorType]` 

Filters processor runs by the processor type. If not provided, runs for all processor types are returned.

Example: `"EXTRACT"`
    
</dd>
</dl>

<dl>
<dd>

**source_id:** `typing.Optional[str]` 

Filters processor runs by the source ID. The source ID corresponds to the entity that created the processor run.

Example: `"workflow_run_123"`
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[ProcessorRunListRequestSource]` 

Filters processor runs by the source that created them. If not provided, runs from all sources are returned.

The source of the processor run:
* `"ADMIN"` - Created by admin
* `"BATCH_PROCESSOR_RUN"` - Created from a batch processor run
* `"PLAYGROUND"` - Created from playground
* `"WORKFLOW_CONFIGURATION"` - Created from workflow configuration
* `"WORKFLOW_RUN"` - Created from a workflow run
* `"STUDIO"` - Created from Studio
* `"API"` - Created via API
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters processor runs by the name of the file. Only returns processor runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortByEnum]` — Sorts the processor runs by the given field.
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDirEnum]` — Sorts the processor runs in ascending or descending order. Ascending order means the earliest processor run is returned first.
    
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

<details><summary><code>client.processor_run.<a href="src/extend_ai/processor_run/client.py">create</a>(...) -&gt; AsyncHttpResponse[ProcessorRunCreateResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run processors (extraction, classification, splitting, etc.) on a given document.

**Synchronous vs Asynchronous Processing:**
- **Asynchronous (default)**: Returns immediately with `PROCESSING` status. Use webhooks or polling to get results.
- **Synchronous**: Set `sync: true` to wait for completion and get final results in the response (5-minute timeout).

**For asynchronous processing:**
- You can [configure webhooks](https://docs.extend.ai/product/webhooks/configuration) to receive notifications when a processor run is complete or failed.
- Or you can [poll the get endpoint](https://docs.extend.ai/2025-04-21/developers/api-reference/processor-endpoints/get-processor-run) for updates on the status of the processor run.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.processor_run.create(
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

**file:** `typing.Optional[ProcessorRunFileInput]` — The file to be processed. One of `file` or `rawText` must be provided. Supported file types can be found [here](/product/general/supported-file-types).
    
</dd>
</dl>

<dl>
<dd>

**raw_text:** `typing.Optional[str]` — A raw string to be processed. Can be used in place of file when passing raw text data streams. One of `file` or `rawText` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**sync:** `typing.Optional[bool]` 

Whether to run the processor synchronously. When `true`, the request will wait for the processor run to complete and return the final results. When `false` (default), the request returns immediately with a `PROCESSING` status, and you can poll for completion or use webhooks. For production use cases, we recommending leaving sync off and building around an async integration for more resiliency, unless your use case is predictably fast (e.g. sub < 30 seconds) run time or otherwise have integration constraints that require a synchronous API.

**Timeout**: Synchronous requests have a 5-minute timeout. If the processor run takes longer, it will continue processing asynchronously and you can retrieve the results via the GET endpoint.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[int]` — An optional value used to determine the relative order of ProcessorRuns when rate limiting is in effect. Lower values will be prioritized before higher values.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[JsonObject]` 

An optional object that can be passed in to identify the run of the document processor. It will be returned back to you in the response and webhooks.

To categorize processor runs for billing and usage tracking, include `extend:usage_tags` with an array of string values (e.g., `{"extend:usage_tags": ["production", "team-eng", "customer-123"]}`). Tags must contain only alphanumeric characters, hyphens, and underscores; any special characters will be automatically removed.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorRunCreateRequestConfig]` — The configuration for the processor run. If this is provided, this config will be used. If not provided, the config for the specific version you provide will be used. The type of configuration must match the processor type.
    
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

<details><summary><code>client.processor_run.<a href="src/extend_ai/processor_run/client.py">get</a>(...) -&gt; AsyncHttpResponse[ProcessorRunGetResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a specific processor run, including its status, outputs, and any edits made during review.

A common use case for this endpoint is to poll for the status and final output of an async processor run when using the [Run Processor](https://docs.extend.ai/2025-04-21/developers/api-reference/processor-endpoints/run-processor) endpoint. For instance, if you do not want to not configure webhooks to receive the output via completion/failure events.
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
from extend_ai import Extend

client = Extend(
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

The unique identifier for this processor run.

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

<details><summary><code>client.processor_run.<a href="src/extend_ai/processor_run/client.py">delete</a>(...) -&gt; AsyncHttpResponse[ProcessorRunDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a processor run and all associated data from Extend. This operation is permanent and cannot be undone.

This endpoint can be used if you'd like to manage data retention on your own rather than automated data retention policies. Or make one-off deletions for your downstream customers.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.processor_run.delete(
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

The ID of the processor run to delete.

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

<details><summary><code>client.processor_run.<a href="src/extend_ai/processor_run/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[ProcessorRunCancelResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel a running processor run by its ID. This endpoint allows you to stop a processor run that is currently in progress.

Note: Only processor runs with a status of `"PROCESSING"` can be cancelled. Processor runs that have already completed, failed, or been cancelled cannot be cancelled again.
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.processor_run.cancel(
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

The unique identifier for the processor run to cancel.

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
<details><summary><code>client.processor.<a href="src/extend_ai/processor/client.py">list</a>(...) -&gt; AsyncHttpResponse[ListProcessorsResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all processors in your organization
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
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
)
client.processor.list(
    type="EXTRACT",
    next_page_token="nextPageToken",
    max_page_size=1,
    sort_by="createdAt",
    sort_dir="asc",
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

**type:** `typing.Optional[ProcessorType]` — Filter processors by type
    
</dd>
</dl>

<dl>
<dd>

**next_page_token:** `typing.Optional[str]` — Token for retrieving the next page of results
    
</dd>
</dl>

<dl>
<dd>

**max_page_size:** `typing.Optional[int]` — Maximum number of processors to return per page
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[ProcessorListRequestSortBy]` — Field to sort by
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[ProcessorListRequestSortDir]` — Sort direction
    
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

<details><summary><code>client.processor.<a href="src/extend_ai/processor/client.py">create</a>(...) -&gt; AsyncHttpResponse[ProcessorCreateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of an existing processor to clone. One of `cloneProcessorId` or `config` must be provided.

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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.processor.<a href="src/extend_ai/processor/client.py">update</a>(...) -&gt; AsyncHttpResponse[ProcessorUpdateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of the processor to update.

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
<details><summary><code>client.processor_version.<a href="src/extend_ai/processor_version/client.py">list</a>(...) -&gt; AsyncHttpResponse[ProcessorVersionListResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of the processor to retrieve versions for.

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

<details><summary><code>client.processor_version.<a href="src/extend_ai/processor_version/client.py">create</a>(...) -&gt; AsyncHttpResponse[ProcessorVersionCreateResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of the processor to publish a new version for.

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

<details><summary><code>client.processor_version.<a href="src/extend_ai/processor_version/client.py">get</a>(...) -&gt; AsyncHttpResponse[ProcessorVersionGetResponse]</code></summary>
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
from extend_ai import Extend

client = Extend(
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

The ID of the processor.

Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**processor_version_id:** `str` 

The ID of the specific processor version to retrieve.

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

