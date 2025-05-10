# Reference
<details><summary><code>client.<a href="src/extend_ai/client.py">run_workflow</a>(...)</code></summary>
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
client = Extend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
client.run_workflow(workflow_id='workflow_id_here', )

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

## WorkflowRun
<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">list</a>(...)</code></summary>
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
client = Extend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
client.workflow_run.list(next_page_token='xK9mLPqRtN3vS8wF5hB2cQ==:zWvUxYjM4nKpL7aDgE9HbTcR2mAyX3/Q+CNkfBSw1dZ=', )

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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">get</a>(...)</code></summary>
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
client = Extend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
client.workflow_run.get(workflow_run_id='workflow_run_id_here', )

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

<details><summary><code>client.workflow_run.<a href="src/extend_ai/workflow_run/client.py">update</a>(...)</code></summary>
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
client = Extend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
client.workflow_run.update(workflow_run_id='workflow_run_id_here', )

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

