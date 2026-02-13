# Reference
<details><summary><code>client.<a href="src/extend_ai/client.py">parse</a>(...) -&gt; AsyncHttpResponse[ParseRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Parse a file synchronously, waiting for the result before returning. This endpoint has a **5-minute timeout** — if processing takes longer, the request will fail.

**Note:** This endpoint is intended for onboarding and testing only. For production workloads, use `POST /parse_runs` with [polling or webhooks](https://docs.extend.ai/2026-02-09/developers/async-processing) instead, as it provides better reliability for large files and avoids timeout issues.

The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

For more details, see the [Parse File guide](https://docs.extend.ai/2026-02-09/product/parsing/parse).
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
client.parse(
    file={"url": "url"},
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

**file:** `ParseRequestFileParams` — The file to be parsed. Files can be provided as a URL or an Extend file ID.
    
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

**config:** `typing.Optional[ParseConfigParams]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.<a href="src/extend_ai/client.py">edit</a>(...) -&gt; AsyncHttpResponse[EditRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit a file synchronously, waiting for the result before returning. This endpoint has a **5-minute timeout** — if processing takes longer, the request will fail.

**Note:** This endpoint is intended for onboarding and testing only. For production workloads, use `POST /edit_runs` with [polling or webhooks](https://docs.extend.ai/2026-02-09/developers/async-processing) instead, as it provides better reliability for large files and avoids timeout issues.

The Edit endpoint allows you to detect and fill form fields in PDF documents.

For more details, see the [Edit File guide](https://docs.extend.ai/2026-02-09/product/editing/edit).
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
client.edit(
    file={"url": "url"},
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

**file:** `EditRequestFileParams` — The file to be edited. Files can be provided as a URL or an Extend file ID.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[EditConfigParams]` 
    
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

<details><summary><code>client.<a href="src/extend_ai/client.py">extract</a>(...) -&gt; AsyncHttpResponse[ExtractRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Extract structured data from a file synchronously, waiting for the result before returning. This endpoint has a **5-minute timeout** — if processing takes longer, the request will fail.

**Note:** This endpoint is intended for onboarding and testing only. For production workloads, use `POST /extract_runs` with [polling or webhooks](https://docs.extend.ai/2026-02-09/developers/async-processing) instead, as it provides better reliability for large files and avoids timeout issues.

The Extract endpoint allows you to extract structured data from files using an existing extractor or an inline configuration.

For more details, see the [Extract File guide](https://docs.extend.ai/2026-02-09/product/extracting/extract).
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
client.extract(
    file={"url": "url"},
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

**file:** `ExtractRequestFileParams` — The file to be extracted from. Files can be provided as a URL, Extend file ID, or raw text.
    
</dd>
</dl>

<dl>
<dd>

**extractor:** `typing.Optional[ExtractRequestExtractorParams]` — Reference to an existing extractor. One of `extractor` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ExtractConfigJsonParams]` — Inline extract configuration. One of `extractor` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.<a href="src/extend_ai/client.py">classify</a>(...) -&gt; AsyncHttpResponse[ClassifyRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Classify a document synchronously, waiting for the result before returning. This endpoint has a **5-minute timeout** — if processing takes longer, the request will fail.

**Note:** This endpoint is intended for onboarding and testing only. For production workloads, use `POST /classify_runs` with [polling or webhooks](https://docs.extend.ai/2026-02-09/developers/async-processing) instead, as it provides better reliability for large files and avoids timeout issues.

The Classify endpoint allows you to classify documents using an existing classifier or an inline configuration.

For more details, see the [Classify File guide](https://docs.extend.ai/2026-02-09/product/classifying/classify).
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
client.classify(
    file={"url": "url"},
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

**file:** `ClassifyRequestFileParams` — The file to be classified. Files can be provided as a URL, an Extend file ID, or raw text.
    
</dd>
</dl>

<dl>
<dd>

**classifier:** `typing.Optional[ClassifyRequestClassifierParams]` — Reference to an existing classifier. One of `classifier` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ClassifyConfigParams]` — Inline classify configuration. One of `classifier` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.<a href="src/extend_ai/client.py">split</a>(...) -&gt; AsyncHttpResponse[SplitRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Split a document synchronously, waiting for the result before returning. This endpoint has a **5-minute timeout** — if processing takes longer, the request will fail.

**Note:** This endpoint is intended for onboarding and testing only. For production workloads, use `POST /split_runs` with [polling or webhooks](https://docs.extend.ai/2026-02-09/developers/async-processing) instead, as it provides better reliability for large files and avoids timeout issues.

The Split endpoint allows you to split documents into multiple parts using an existing splitter or an inline configuration.

For more details, see the [Split File guide](https://docs.extend.ai/2026-02-09/product/splitting/split).
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
client.split(
    file={"url": "url"},
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

**file:** `SplitRequestFileParams` — The file to be split. Files can be provided as a URL or an Extend file ID.
    
</dd>
</dl>

<dl>
<dd>

**splitter:** `typing.Optional[SplitRequestSplitterParams]` — Reference to an existing splitter. One of `splitter` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[SplitConfigParams]` — Inline splitter configuration. One of `splitter` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

## Files
<details><summary><code>client.files.<a href="src/extend_ai/files/client.py">list</a>(...) -&gt; AsyncHttpResponse[FilesListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List files.
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
client.files.list(
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

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.files.<a href="src/extend_ai/files/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[File]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch a file by its ID.
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
client.files.retrieve(
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

ID for the file. It will always start with `"file_"`.

Example: `"file_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**raw_text:** `typing.Optional[bool]` 

**Deprecated:** Use `POST /parse_runs` instead to parse file contents.

If set to true, the raw text content of the file will be included in the response.
    
</dd>
</dl>

<dl>
<dd>

**markdown:** `typing.Optional[bool]` 

**Deprecated:** Use `POST /parse_runs` instead to parse file contents.

If set to true, the markdown content of the file will be included in the response.

Only available for files with a type of PDF, IMG, or DOCX files that were auto-converted to PDFs.
    
</dd>
</dl>

<dl>
<dd>

**html:** `typing.Optional[bool]` 

**Deprecated:** Use `POST /parse_runs` instead to parse file contents.

If set to true, the html content of the file will be included in the response.

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

<details><summary><code>client.files.<a href="src/extend_ai/files/client.py">delete</a>(...) -&gt; AsyncHttpResponse[FilesDeleteResponse]</code></summary>
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
client.files.delete(
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

<details><summary><code>client.files.<a href="src/extend_ai/files/client.py">upload</a>(...) -&gt; AsyncHttpResponse[File]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upload and create a new file in Extend.

This endpoint accepts file contents and registers them as a File in Extend, which can be used for [running workflows](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/run-workflow), [creating evaluation set items](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/evaluation/bulk-create-evaluation-set-items), [parsing](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/parse/parse-file), etc.

If an uploaded file is detected as a Word or PowerPoint document, it will be automatically converted to a PDF.

Supported file types can be found [here](https://docs.extend.ai/2026-02-09/product/general/supported-file-types).

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
client.files.upload()

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

## ParseRuns
<details><summary><code>client.parse_runs.<a href="src/extend_ai/parse_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[ParseRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Parse files to get cleaned, chunked target content (e.g. markdown).

The Parse endpoint allows you to convert documents into structured, machine-readable formats with fine-grained control over the parsing process. This endpoint is ideal for extracting cleaned document content to be used as context for downstream processing, e.g. RAG pipelines, custom ingestion pipelines, embeddings classification, etc.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Parse Run endpoint for results.
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
client.parse_runs.create(
    file={"url": "url"},
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

**file:** `ParseRunsCreateRequestFileParams` — The file to be parsed. Files can be provided as a URL or an Extend file ID.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ParseConfigParams]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.parse_runs.<a href="src/extend_ai/parse_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[ParseRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the status and results of a parse run.

Use this endpoint to get results for a parse run that has already completed, or to check on the status of a parse run initiated by the [Create Parse Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/parse/create-parse-run) endpoint.
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
client.parse_runs.retrieve(
    id="parse_run_id_here",
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

The unique identifier for the parse run.

Example: `"pr_xK9mLPqRtN3vS8wF5hB2cQ"`
    
</dd>
</dl>

<dl>
<dd>

**response_type:** `typing.Optional[ParseRunsRetrieveRequestResponseType]` 

Controls how the output is delivered. Defaults to `inline`.
* `json` - Returns the output directly in the `output` field of the response body.
* `url` - Returns a presigned URL in the `outputUrl` field to download the output as a JSON file. The URL expires after 15 minutes. Useful for large outputs.
    
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

<details><summary><code>client.parse_runs.<a href="src/extend_ai/parse_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[ParseRunsDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a parse run and all associated data from Extend. This operation is permanent and cannot be undone.

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
client.parse_runs.delete(
    id="parse_run_id_here",
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

The ID of the parse run to delete.

Example: `"pr_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

## EditRuns
<details><summary><code>client.edit_runs.<a href="src/extend_ai/edit_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[EditRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit and manipulate PDF documents by detecting and filling form fields.

The Edit Runs endpoint allows you to convert and edit documents and get an edit run ID that can be used to check status and retrieve results with the Get Edit Run endpoint.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Edit Run endpoint for results.
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
client.edit_runs.create(
    file={"url": "url"},
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

**file:** `EditRunsCreateRequestFileParams` — The file to be edited. Files can be provided as a URL or an Extend file ID.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[EditConfigParams]` 
    
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

<details><summary><code>client.edit_runs.<a href="src/extend_ai/edit_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[EditRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the status and results of an edit run.

Use this endpoint to get results for an edit run that has already completed, or to check on the status of an edit run initiated via the [Create Edit Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/edit/create-edit-run) endpoint.
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
client.edit_runs.retrieve(
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

Example: `"edr_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

<details><summary><code>client.edit_runs.<a href="src/extend_ai/edit_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[EditRunsDeleteResponse]</code></summary>
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
client.edit_runs.delete(
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

Example: `"edr_xK9mLPqRtN3vS8wF5hB2cQ"`
    
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

## ExtractRuns
<details><summary><code>client.extract_runs.<a href="src/extend_ai/extract_runs/client.py">list</a>(...) -&gt; AsyncHttpResponse[ExtractRunsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all extract runs.

Returns a summary of each run. Use `GET /extract_runs/{id}` to retrieve the full object including `output` and `config`.
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
client.extract_runs.list(
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

**status:** `typing.Optional[ProcessorRunStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**extractor_id:** `typing.Optional[str]` 

Filters extract runs by the extractor ID. If not provided, all extract runs are returned.

Example: `"ex_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**source_id:** `typing.Optional[RunSourceId]` — Filters runs by the source ID.
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[RunSource]` — Filters runs by the source that created them. If not provided, runs from all sources are returned.
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters runs by the name of the file. Only returns runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.extract_runs.<a href="src/extend_ai/extract_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[ExtractRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Extract structured data from a file using an existing extractor or an inline configuration.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Extract Run endpoint for results.
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
client.extract_runs.create(
    file={"url": "url"},
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

**file:** `ExtractRunsCreateRequestFileParams` — The file to be extracted from. Files can be provided as a URL, Extend file ID, or raw text.
    
</dd>
</dl>

<dl>
<dd>

**extractor:** `typing.Optional[ExtractRunsCreateRequestExtractorParams]` — Reference to an existing extractor. One of `extractor` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ExtractConfigJsonParams]` — Inline extract configuration. One of `extractor` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[RunPriority]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.extract_runs.<a href="src/extend_ai/extract_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[ExtractRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a specific extract run, including its status, outputs, and any edits made during review.

A common use case for this endpoint is to poll for the status and final output of an extract run when using the [Create Extract Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/extract/create-extract-run) endpoint. For instance, if you do not want to not configure webhooks to receive the output via completion/failure events.
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
client.extract_runs.retrieve(
    id="extract_run_id_here",
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

The unique identifier for this extract run.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.extract_runs.<a href="src/extend_ai/extract_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[ExtractRunsDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an extract run and all associated data from Extend. This operation is permanent and cannot be undone.

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
client.extract_runs.delete(
    id="id",
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

**id:** `str` — The ID of the extract run.
    
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

<details><summary><code>client.extract_runs.<a href="src/extend_ai/extract_runs/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[ExtractRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel an in-progress extract run.

Note: Only extract runs with a status of `"PROCESSING"` can be cancelled. Extractor runs that have already completed, failed, or been cancelled cannot be cancelled again.
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
client.extract_runs.cancel(
    id="extract_run_id_here",
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

The ID of the extract run to cancel.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

## Extractors
<details><summary><code>client.extractors.<a href="src/extend_ai/extractors/client.py">list</a>(...) -&gt; AsyncHttpResponse[ExtractorsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all extractors.

Returns a summary of each extractor. Use `GET /extractors/{id}` to retrieve the full object including `draftVersion`.
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
client.extractors.list(
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

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.extractors.<a href="src/extend_ai/extractors/client.py">create</a>(...) -&gt; AsyncHttpResponse[Extractor]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new extractor.
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
client.extractors.create(
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

**name:** `str` — The name of the extractor.
    
</dd>
</dl>

<dl>
<dd>

**clone_extractor_id:** `typing.Optional[str]` 

The ID of an existing extractor to clone. If provided, the new extractor will be created with the same config as the extractor with this ID. Cannot be provided together with `config`.

Example: `"ex_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ExtractConfigJsonParams]` — The configuration for the extractor. Cannot be provided together with `cloneExtractorId`.
    
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

<details><summary><code>client.extractors.<a href="src/extend_ai/extractors/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[Extractor]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details of an extractor.
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
client.extractors.retrieve(
    id="extractor_id_here",
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

The ID of the extractor to get.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.extractors.<a href="src/extend_ai/extractors/client.py">update</a>(...) -&gt; AsyncHttpResponse[Extractor]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing extractor.
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
client.extractors.update(
    id="extractor_id_here",
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

The ID of the extractor to update.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name of the extractor.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ExtractConfigJsonParams]` — The new configuration for the extractor. This will update the draft version of the extractor.
    
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

## ExtractorVersions
<details><summary><code>client.extractor_versions.<a href="src/extend_ai/extractor_versions/client.py">list</a>(...) -&gt; AsyncHttpResponse[ExtractorVersionsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to fetch all versions of a given extractor, including the current `draft` version.

Versions are returned in descending order of creation (newest first) with the `draft` version first. The `draft` version is the latest unpublished version of the extractor, which can be published to create a new version. It might not have any changes from the last published version.
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
client.extractor_versions.list(
    extractor_id="extractor_id_here",
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

**extractor_id:** `str` 

The ID of the extractor.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.extractor_versions.<a href="src/extend_ai/extractor_versions/client.py">create</a>(...) -&gt; AsyncHttpResponse[ExtractorVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to publish a new version of an existing extractor. Publishing a new version creates a snapshot of the extractor's current configuration and makes it available for use in workflows.

Publishing a new version does not automatically update existing workflows using this extractor. You may need to manually update workflows to use the new version if desired.
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
from extend_ai import Extend, ReleaseType

client = Extend(
    token="YOUR_TOKEN",
)
client.extractor_versions.create(
    extractor_id="extractor_id_here",
    release_type=ReleaseType.MAJOR,
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

**extractor_id:** `str` 

The ID of the extractor.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**release_type:** `ReleaseType` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[VersionDescription]` 
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ExtractConfigJsonParams]` — The configuration for this version of the extractor.
    
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

<details><summary><code>client.extractor_versions.<a href="src/extend_ai/extractor_versions/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[ExtractorVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific version of an extractor in Extend
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
client.extractor_versions.retrieve(
    extractor_id="extractor_id_here",
    version_id="extractor_version_id_here",
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

**extractor_id:** `str` 

The ID of the extractor.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` 

The ID of the specific extractor version.

Example: `"extv_QYk6jgHA_8CsO8rVWhyNC"`
    
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

## ClassifyRuns
<details><summary><code>client.classify_runs.<a href="src/extend_ai/classify_runs/client.py">list</a>(...) -&gt; AsyncHttpResponse[ClassifyRunsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all classify runs.

Returns a summary of each run. Use `GET /classify_runs/{id}` to retrieve the full object including `output` and `config`.
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
client.classify_runs.list(
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

**status:** `typing.Optional[ProcessorRunStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**classifier_id:** `typing.Optional[str]` 

Filters classify runs by the classifier ID. If not provided, all classify runs are returned.

Example: `"cl_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**source_id:** `typing.Optional[RunSourceId]` — Filters runs by the source ID.
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[RunSource]` — Filters runs by the source that created them. If not provided, runs from all sources are returned.
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters runs by the name of the file. Only returns runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.classify_runs.<a href="src/extend_ai/classify_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[ClassifyRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Classify a document using an existing classifier or an inline configuration.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Classify Run endpoint for results.
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
client.classify_runs.create(
    file={"url": "url"},
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

**file:** `ClassifyRunsCreateRequestFileParams` — The file to be classified. Files can be provided as a URL, an Extend file ID, or raw text.
    
</dd>
</dl>

<dl>
<dd>

**classifier:** `typing.Optional[ClassifyRunsCreateRequestClassifierParams]` — Reference to an existing classifier. One of `classifier` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ClassifyConfigParams]` — Inline classify configuration. One of `classifier` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[RunPriority]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.classify_runs.<a href="src/extend_ai/classify_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[ClassifyRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a specific classify run, including its status and outputs.

A common use case for this endpoint is to poll for the status and final output of a classify run when using the [Create Classify Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/classify/create-classify-run) endpoint. For instance, if you do not want to not configure webhooks to receive the output via completion/failure events.
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
client.classify_runs.retrieve(
    id="classify_run_id_here",
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

The unique identifier for this classify run.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.classify_runs.<a href="src/extend_ai/classify_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[ClassifyRunsDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a classify run and all associated data from Extend. This operation is permanent and cannot be undone.

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
client.classify_runs.delete(
    id="id",
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

**id:** `str` — The ID of the classify run.
    
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

<details><summary><code>client.classify_runs.<a href="src/extend_ai/classify_runs/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[ClassifyRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel an in-progress classify run.

Note: Only classify runs with a status of `"PROCESSING"` can be cancelled. Classifier runs that have already completed, failed, or been cancelled cannot be cancelled again.
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
client.classify_runs.cancel(
    id="classify_run_id_here",
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

The ID of the classify run to cancel.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

## Classifiers
<details><summary><code>client.classifiers.<a href="src/extend_ai/classifiers/client.py">list</a>(...) -&gt; AsyncHttpResponse[ClassifiersListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all classifiers.

Returns a summary of each classifier. Use `GET /classifiers/{id}` to retrieve the full object including `draftVersion`.
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
client.classifiers.list(
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

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.classifiers.<a href="src/extend_ai/classifiers/client.py">create</a>(...) -&gt; AsyncHttpResponse[Classifier]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new classifier.
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
client.classifiers.create(
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

**name:** `str` — The name of the classifier.
    
</dd>
</dl>

<dl>
<dd>

**clone_classifier_id:** `typing.Optional[str]` 

The ID of an existing classifier to clone. If provided, the new classifier will be created with the same config as the classifier with this ID. Cannot be provided together with `config`.

Example: `"cl_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ClassifyConfigParams]` — The configuration for the classifier. Cannot be provided together with `cloneClassifierId`.
    
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

<details><summary><code>client.classifiers.<a href="src/extend_ai/classifiers/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[Classifier]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details of a classifier.
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
client.classifiers.retrieve(
    id="classifier_id_here",
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

The ID of the classifier to get.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.classifiers.<a href="src/extend_ai/classifiers/client.py">update</a>(...) -&gt; AsyncHttpResponse[Classifier]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing classifier.
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
client.classifiers.update(
    id="classifier_id_here",
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

The ID of the classifier to update.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name of the classifier.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ClassifyConfigParams]` — The new configuration for the classifier. This will update the draft version of the classifier.
    
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

## ClassifierVersions
<details><summary><code>client.classifier_versions.<a href="src/extend_ai/classifier_versions/client.py">list</a>(...) -&gt; AsyncHttpResponse[ClassifierVersionsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to fetch all versions of a given classifier, including the current `draft` version.

Versions are returned in descending order of creation (newest first) with the `draft` version first. The `draft` version is the latest unpublished version of the classifier, which can be published to create a new version. It might not have any changes from the last published version.
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
client.classifier_versions.list(
    classifier_id="classifier_id_here",
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

**classifier_id:** `str` 

The ID of the classifier.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.classifier_versions.<a href="src/extend_ai/classifier_versions/client.py">create</a>(...) -&gt; AsyncHttpResponse[ClassifierVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to publish a new version of an existing classifier. Publishing a new version creates a snapshot of the classifier's current configuration and makes it available for use in workflows.

Publishing a new version does not automatically update existing workflows using this classifier. You may need to manually update workflows to use the new version if desired.
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
from extend_ai import Extend, ReleaseType

client = Extend(
    token="YOUR_TOKEN",
)
client.classifier_versions.create(
    classifier_id="classifier_id_here",
    release_type=ReleaseType.MAJOR,
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

**classifier_id:** `str` 

The ID of the classifier.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**release_type:** `ReleaseType` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[VersionDescription]` 
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ClassifyConfigParams]` — The configuration for this version of the classifier.
    
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

<details><summary><code>client.classifier_versions.<a href="src/extend_ai/classifier_versions/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[ClassifierVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific version of a classifier in Extend
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
client.classifier_versions.retrieve(
    classifier_id="classifier_id_here",
    version_id="classifier_version_id_here",
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

**classifier_id:** `str` 

The ID of the classifier.

Example: `"cl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` 

The ID of the specific classifier version.

Example: `"clsv_QYk6jgHA_8CsO8rVWhyNC"`
    
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

## SplitRuns
<details><summary><code>client.split_runs.<a href="src/extend_ai/split_runs/client.py">list</a>(...) -&gt; AsyncHttpResponse[SplitRunsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all split runs.

Returns a summary of each run. Use `GET /split_runs/{id}` to retrieve the full object including `output` and `config`.
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
client.split_runs.list(
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

**status:** `typing.Optional[ProcessorRunStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**splitter_id:** `typing.Optional[str]` 

Filters split runs by the splitter ID. If not provided, all split runs are returned.

Example: `"spl_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**source_id:** `typing.Optional[RunSourceId]` — Filters runs by the source ID.
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[RunSource]` — Filters runs by the source that created them. If not provided, runs from all sources are returned.
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters runs by the name of the file. Only returns runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.split_runs.<a href="src/extend_ai/split_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[SplitRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Split a document into multiple parts using an existing splitter or an inline configuration.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Split Run endpoint for results.
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
client.split_runs.create(
    file={"url": "url"},
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

**file:** `SplitRunsCreateRequestFileParams` — The file to be split. Files can be provided as a URL or an Extend file ID.
    
</dd>
</dl>

<dl>
<dd>

**splitter:** `typing.Optional[SplitRunsCreateRequestSplitterParams]` — Reference to an existing splitter. One of `splitter` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[SplitConfigParams]` — Inline splitter configuration. One of `splitter` or `config` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[RunPriority]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
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

<details><summary><code>client.split_runs.<a href="src/extend_ai/split_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[SplitRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve details about a specific split run, including its status and outputs.

A common use case for this endpoint is to poll for the status and final output of a split run when using the [Create Split Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/split/create-split-run) endpoint. For instance, if you do not want to not configure webhooks to receive the output via completion/failure events.
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
client.split_runs.retrieve(
    id="split_run_id_here",
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

The unique identifier for this split run.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.split_runs.<a href="src/extend_ai/split_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[SplitRunsDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a split run and all associated data from Extend. This operation is permanent and cannot be undone.

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
client.split_runs.delete(
    id="id",
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

**id:** `str` — The ID of the split run.
    
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

<details><summary><code>client.split_runs.<a href="src/extend_ai/split_runs/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[SplitRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel an in-progress split run.

Note: Only split runs with a status of `"PROCESSING"` can be cancelled. Splitter runs that have already completed, failed, or been cancelled cannot be cancelled again.
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
client.split_runs.cancel(
    id="split_run_id_here",
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

The ID of the split run to cancel.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

## Splitters
<details><summary><code>client.splitters.<a href="src/extend_ai/splitters/client.py">list</a>(...) -&gt; AsyncHttpResponse[SplittersListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all splitters.

Returns a summary of each splitter. Use `GET /splitters/{id}` to retrieve the full object including `draftVersion`.
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
client.splitters.list(
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

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.splitters.<a href="src/extend_ai/splitters/client.py">create</a>(...) -&gt; AsyncHttpResponse[Splitter]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new splitter.
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
client.splitters.create(
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

**name:** `str` — The name of the splitter.
    
</dd>
</dl>

<dl>
<dd>

**clone_splitter_id:** `typing.Optional[str]` 

The ID of an existing splitter to clone. If provided, the new splitter will be created with the same config as the splitter with this ID. Cannot be provided together with `config`.

Example: `"spl_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[SplitConfigParams]` — The configuration for the splitter. Cannot be provided together with `cloneSplitterId`.
    
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

<details><summary><code>client.splitters.<a href="src/extend_ai/splitters/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[Splitter]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details of a splitter.
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
client.splitters.retrieve(
    id="splitter_id_here",
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

The ID of the splitter to get.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

<details><summary><code>client.splitters.<a href="src/extend_ai/splitters/client.py">update</a>(...) -&gt; AsyncHttpResponse[Splitter]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing splitter.
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
client.splitters.update(
    id="splitter_id_here",
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

The ID of the splitter to update.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name of the splitter.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[SplitConfigParams]` — The new configuration for the splitter. This will update the draft version of the splitter.
    
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

## SplitterVersions
<details><summary><code>client.splitter_versions.<a href="src/extend_ai/splitter_versions/client.py">list</a>(...) -&gt; AsyncHttpResponse[SplitterVersionsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to fetch all versions of a given splitter, including the current `draft` version.

Versions are returned in descending order of creation (newest first) with the `draft` version first. The `draft` version is the latest unpublished version of the splitter, which can be published to create a new version. It might not have any changes from the last published version.
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
client.splitter_versions.list(
    splitter_id="splitter_id_here",
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

**splitter_id:** `str` 

The ID of the splitter.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.splitter_versions.<a href="src/extend_ai/splitter_versions/client.py">create</a>(...) -&gt; AsyncHttpResponse[SplitterVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to publish a new version of an existing splitter. Publishing a new version creates a snapshot of the splitter's current configuration and makes it available for use in workflows.

Publishing a new version does not automatically update existing workflows using this splitter. You may need to manually update workflows to use the new version if desired.
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
from extend_ai import Extend, ReleaseType

client = Extend(
    token="YOUR_TOKEN",
)
client.splitter_versions.create(
    splitter_id="splitter_id_here",
    release_type=ReleaseType.MAJOR,
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

**splitter_id:** `str` 

The ID of the splitter.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**release_type:** `ReleaseType` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[VersionDescription]` 
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[SplitConfigParams]` — The configuration for this version of the splitter.
    
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

<details><summary><code>client.splitter_versions.<a href="src/extend_ai/splitter_versions/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[SplitterVersion]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific version of a splitter in Extend
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
client.splitter_versions.retrieve(
    splitter_id="splitter_id_here",
    version_id="splitter_version_id_here",
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

**splitter_id:** `str` 

The ID of the splitter.

Example: `"spl_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` 

The ID of the specific splitter version.

Example: `"splv_QYk6jgHA_8CsO8rVWhyNC"`
    
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

## Workflows
<details><summary><code>client.workflows.<a href="src/extend_ai/workflows/client.py">create</a>(...) -&gt; AsyncHttpResponse[Workflow]</code></summary>
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
client.workflows.create(
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

## WorkflowRuns
<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">list</a>(...) -&gt; AsyncHttpResponse[WorkflowRunsListResponse]</code></summary>
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
client.workflow_runs.list(
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

**status:** `typing.Optional[WorkflowRunStatus]` 
    
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

Filters workflow runs by the batch ID. This is useful for fetching all runs for a given batch created via the [Batch Run Workflow](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/batch-run-workflow) endpoint.

Example: `"batch_7Ws31-F5"`
    
</dd>
</dl>

<dl>
<dd>

**file_name_contains:** `typing.Optional[str]` 

Filters runs by the name of the file. Only returns runs where the file name contains this string.

Example: `"invoice"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">create</a>(...) -&gt; AsyncHttpResponse[WorkflowRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run a workflow with a file. A workflow is a sequence of steps that process files and data in a specific order to achieve a desired outcome.

The request returns immediately with a `PROCESSING` status. Use webhooks or poll the Get Workflow Run endpoint for results.
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
client.workflow_runs.create(
    workflow={"id": "workflow_BMdfq_yWM3sT-ZzvCnA3f"},
    file={"url": "url"},
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

**workflow:** `WorkflowReferenceParams` 
    
</dd>
</dl>

<dl>
<dd>

**file:** `WorkflowRunsCreateRequestFileParams` — The file to be processed. Supported file types can be found [here](https://docs.extend.ai/2026-02-09/product/general/supported-file-types). Files can be provided as a URL, an Extend file ID, or raw text. If you wish to process more at a time, consider using the [Batch Run Workflow](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/batch-run-workflow) endpoint.
    
</dd>
</dl>

<dl>
<dd>

**outputs:** `typing.Optional[typing.Sequence[WorkflowRunsCreateRequestOutputsItemParams]]` — Predetermined outputs to be used for the workflow run. Generally not recommended for most use cases, however, can be useful in cases of overriding a classification in a workflow, or a subset of extraction fields when data is known.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[RunPriority]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[RunMetadata]` 
    
</dd>
</dl>

<dl>
<dd>

**secrets:** `typing.Optional[RunSecrets]` 
    
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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[WorkflowRun]</code></summary>
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
client.workflow_runs.retrieve(
    id="workflow_run_id_here",
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

The ID of the workflow run.

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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">update</a>(...) -&gt; AsyncHttpResponse[WorkflowRun]</code></summary>
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
client.workflow_runs.update(
    id="workflow_run_id_here",
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

The ID of the workflow run.

Example: `"workflow_run_xKm9pNv3qWsY_jL2tR5Dh"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — An optional name that can be assigned to a specific WorkflowRun
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Any]]` 

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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">delete</a>(...) -&gt; AsyncHttpResponse[WorkflowRunsDeleteResponse]</code></summary>
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
client.workflow_runs.delete(
    id="workflow_run_id_here",
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

The ID of the workflow run.

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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">cancel</a>(...) -&gt; AsyncHttpResponse[WorkflowRun]</code></summary>
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
client.workflow_runs.cancel(
    id="workflow_run_id_here",
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

The ID of the workflow run.

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

<details><summary><code>client.workflow_runs.<a href="src/extend_ai/workflow_runs/client.py">create_batch</a>(...) -&gt; AsyncHttpResponse[WorkflowRunsCreateBatchResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint allows you to efficiently initiate large batches of workflow runs in a single request (up to 1,000 in a single request, but you can queue up multiple batches in rapid succession). It accepts an array of inputs, each containing a file and metadata pair. The primary use case for this endpoint is for doing large bulk runs of >1000 files at a time that can process over the course of a few hours without needing to manage rate limits that would likely occur using the primary run endpoint.

Unlike the single [Run Workflow](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/run-workflow) endpoint which returns the details of the created workflow runs immediately, this batch endpoint returns a `batchId`.

Our recommended usage pattern is to integrate with [Webhooks](https://docs.extend.ai/2026-02-09/product/webhooks/configuration) for consuming results, using the `metadata` and `batchId` to match up results to the original inputs in your downstream systems. However, you can integrate in a polling mechanism by using a combination of the [List Workflow Runs](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/list-workflow-runs) endpoint to fetch all runs via a batch, and then [Get Workflow Run](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/get-workflow-run) to fetch the full outputs each run.

**Priority:** All workflow runs created through this batch endpoint are automatically assigned a priority of 90.

**Processing and Monitoring:**
Upon successful submission, the endpoint returns a `batchId`. The individual workflow runs are then queued for processing.

- **Monitoring:** Track the progress and consume results of individual runs using [Webhooks](https://docs.extend.ai/2026-02-09/product/webhooks/configuration). Subscribe to events like `workflow_run.completed`, `workflow_run.failed`, etc. The webhook payload for these events will include the corresponding `batchId` and the `metadata` you provided for each input.
- **Fetching Results:** You can also use the [List Workflow Runs](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/workflow/list-workflow-runs) endpoint and filter using the `batchId` query param.
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
client.workflow_runs.create_batch(
    workflow={"id": "workflow_BMdfq_yWM3sT-ZzvCnA3f"},
    inputs=[{"file": {"url": "url"}}],
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

**workflow:** `WorkflowReferenceParams` 
    
</dd>
</dl>

<dl>
<dd>

**inputs:** `typing.Sequence[WorkflowRunsCreateBatchRequestInputsItemParams]` — An array of input objects to be processed by the workflow. Each object represents a single workflow run to be created. The array must contain at least 1 input and at most 1000 inputs.
    
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

**status:** `typing.Optional[LegacyProcessorStatus]` 

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

Example: `"ex_BMdfq_yWM3sT-ZzvCnA3f"`
    
</dd>
</dl>

<dl>
<dd>

**processor_type:** `typing.Optional[LegacyProcessorType]` 

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

**sort_by:** `typing.Optional[LegacySortByEnum]` — Sorts the processor runs by the given field.
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[LegacySortDirEnum]` — Sorts the processor runs in ascending or descending order. Ascending order means the earliest processor run is returned first.
    
</dd>
</dl>

<dl>
<dd>

**next_page_token:** `typing.Optional[LegacyNextPageToken]` 
    
</dd>
</dl>

<dl>
<dd>

**max_page_size:** `typing.Optional[LegacyMaxPageSize]` 
    
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

**processor_id:** `LegacyProcessorId` 
    
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

**file:** `typing.Optional[LegacyProcessorRunFileInputParams]` — The file to be processed. One of `file` or `rawText` must be provided. Supported file types can be found [here](/product/general/supported-file-types).
    
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

Whether to run the processor synchronously. When `true`, the request will wait for the processor run to complete and return the final results. When `false` (default), the request returns immediately with a `PROCESSING` status, and you can poll for completion or use webhooks. For production use cases, we recommending leaving sync off and building around an async integration for more resiliency, unless your use case is predictably fast (e.g. sub < 30 seconds) run time or otherwise have integration constraints that require a synchronous API. See [Async Processing](https://docs.extend.ai/2026-02-09/developers/async-processing) for more details.

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

**metadata:** `typing.Optional[LegacyJsonObject]` 

An optional object that can be passed in to identify the run of the document processor. It will be returned back to you in the response and webhooks.

To categorize processor runs for billing and usage tracking, include `extend:usage_tags` with an array of string values (e.g., `{"extend:usage_tags": ["production", "team-eng", "customer-123"]}`). Tags must contain only alphanumeric characters, hyphens, and underscores; any special characters will be automatically removed.
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorRunCreateRequestConfigParams]` — The configuration for the processor run. If this is provided, this config will be used. If not provided, the config for the specific version you provide will be used. The type of configuration must match the processor type.
    
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

Example: `"exr_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

Example: `"exr_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

Example: `"exr_Xj8mK2pL9nR4vT7qY5wZ"`
    
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
<details><summary><code>client.processor.<a href="src/extend_ai/processor/client.py">list</a>(...) -&gt; AsyncHttpResponse[LegacyListProcessorsResponse]</code></summary>
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
client.processor.list()

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

**type:** `typing.Optional[LegacyProcessorType]` — Filter processors by type
    
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
from extend_ai import Extend, LegacyProcessorType

client = Extend(
    token="YOUR_TOKEN",
)
client.processor.create(
    name="My Processor Name",
    type=LegacyProcessorType.EXTRACT,
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

**type:** `LegacyProcessorType` 
    
</dd>
</dl>

<dl>
<dd>

**clone_processor_id:** `typing.Optional[str]` 

The ID of an existing processor to clone. One of `cloneProcessorId` or `config` must be provided.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorCreateRequestConfigParams]` — The configuration for the processor. The type of configuration must match the processor type. One of `cloneProcessorId` or `config` must be provided.
    
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

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name for the processor
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[ProcessorUpdateRequestConfigParams]` 

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

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
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
from extend_ai.processor_version import ProcessorVersionCreateRequestReleaseType

client = Extend(
    token="YOUR_TOKEN",
)
client.processor_version.create(
    id="processor_id_here",
    release_type=ProcessorVersionCreateRequestReleaseType.MAJOR,
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

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

**config:** `typing.Optional[ProcessorVersionCreateRequestConfigParams]` — The configuration for this version of the processor. The type of configuration must match the processor type.
    
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

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**processor_version_id:** `str` 

The ID of the specific processor version to retrieve.

Example: `"exv_QYk6jgHA_8CsO8rVWhyNC"`
    
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

Retrieve details about a batch processor run, including evaluation runs.

**Deprecated:** This endpoint is maintained for backwards compatibility only and will be replaced in a future API version. Use [Get Evaluation Set Run](/2026-02-09/developers/api-reference/endpoints/evaluation/get-evaluation-set-run) for interacting with evaluation set runs.
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
    id="bpr_id_here",
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

The unique identifier of the batch processor run to retrieve.

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

## EvaluationSets
<details><summary><code>client.evaluation_sets.<a href="src/extend_ai/evaluation_sets/client.py">list</a>(...) -&gt; AsyncHttpResponse[EvaluationSetsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List evaluation sets in your account.
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
client.evaluation_sets.list(
    entity_id="entity_id_here",
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

**entity_id:** `typing.Optional[str]` 

The ID of the extractor, classifier, or splitter to filter evaluation sets by.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.evaluation_sets.<a href="src/extend_ai/evaluation_sets/client.py">create</a>(...) -&gt; AsyncHttpResponse[EvaluationSet]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Evaluation sets are collections of files and expected outputs that are used to evaluate the performance of a given extractor, classifier, or splitter. This endpoint will create a new evaluation set, which items can be added to using the [Create Evaluation Set Item](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/evaluation/create-evaluation-set-item) endpoint.

Note: It is not necessary to create an evaluation set via API. You can also create an evaluation set via the Extend dashboard and take the ID from there. To learn more about how to create evaluation sets, see the [Evaluation Sets](https://docs.extend.ai/product/evaluation/overview) product page.
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
client.evaluation_sets.create(
    name="My Evaluation Set",
    entity_id="entity_id_here",
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

**entity_id:** `str` 

The ID of the extractor, classifier, or splitter to create an evaluation set for. Evaluation sets can in theory be run against any extractor, classifier, or splitter, but it is required to associate the evaluation set with a primary extractor, classifier, or splitter.

Example: `"ex_Xj8mK2pL9nR4vT7qY5wZ"`
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 

A description of what this evaluation set is used for.

Example: `"Q4 2023 vendor invoices"`
    
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

<details><summary><code>client.evaluation_sets.<a href="src/extend_ai/evaluation_sets/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[EvaluationSet]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific evaluation set by ID. This returns an evaluation set object, but does not include the items in the evaluation set. You can use the [List Evaluation Set Items](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/evaluation/list-evaluation-set-items) endpoint to get the items in an evaluation set.
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
client.evaluation_sets.retrieve(
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

The ID of the evaluation set.

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

## EvaluationSetItems
<details><summary><code>client.evaluation_set_items.<a href="src/extend_ai/evaluation_set_items/client.py">list</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemsListResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List items in a specific evaluation set.

Returns a summary of each evaluation set item. Use the [Get Evaluation Set Item](https://docs.extend.ai/2026-02-09/developers/api-reference/endpoints/evaluation/get-evaluation-set-item) endpoint to get the full details of an evaluation set item.
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
client.evaluation_set_items.list(
    evaluation_set_id="evaluation_set_id_here",
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

**evaluation_set_id:** `str` 

The ID of the evaluation set.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_dir:** `typing.Optional[SortDir]` 
    
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

<details><summary><code>client.evaluation_set_items.<a href="src/extend_ai/evaluation_set_items/client.py">create</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemsCreateResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Evaluation set items are the individual files and expected outputs that are used to evaluate the performance of a given extractor, classifier, or splitter in Extend. This endpoint will create new evaluation set items in Extend, which will be used during an evaluation run.

**Limit:** You can create up to 100 items at a time.

Learn more about how to create evaluation set items in the [Evaluation Sets](https://docs.extend.ai/product/evaluation/overview) product page.
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
client.evaluation_set_items.create(
    evaluation_set_id="evaluation_set_id_here",
    items=[{"file_id": "file_id_here", "expected_output": {}}],
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

The ID of the evaluation set.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.Sequence[EvaluationSetItemsCreateRequestItemsItemParams]` — An array of objects representing the evaluation set items to create.
    
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

<details><summary><code>client.evaluation_set_items.<a href="src/extend_ai/evaluation_set_items/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItem]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details of an evaluation set item.
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
client.evaluation_set_items.retrieve(
    evaluation_set_id="evaluation_set_id_here",
    item_id="evaluation_set_item_id_here",
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

The ID of the evaluation set.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` 

The ID of the evaluation set item.

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

<details><summary><code>client.evaluation_set_items.<a href="src/extend_ai/evaluation_set_items/client.py">update</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItem]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

If you need to change the expected output for a given evaluation set item, you can use this endpoint to update the item. This can be useful if you need to correct an error in the expected output or if the output of the extractor, classifier, or splitter has changed.
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
client.evaluation_set_items.update(
    evaluation_set_id="evaluation_set_id_here",
    item_id="evaluation_set_item_id_here",
    expected_output={},
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

The ID of the evaluation set.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` 

The ID of the evaluation set item.

Example: `"evi_kR9mNP12Qw4yTv8BdR3H"`
    
</dd>
</dl>

<dl>
<dd>

**expected_output:** `ProvidedProcessorOutputParams` — The expected output of the extractor, classifier, or splitter when run against the file. This must conform to the output schema of the entity associated with the evaluation set.
    
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

<details><summary><code>client.evaluation_set_items.<a href="src/extend_ai/evaluation_set_items/client.py">delete</a>(...) -&gt; AsyncHttpResponse[EvaluationSetItemsDeleteResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an evaluation set item.
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
client.evaluation_set_items.delete(
    evaluation_set_id="evaluation_set_id_here",
    item_id="evaluation_set_item_id_here",
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

The ID of the evaluation set.

Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` 

The ID of the evaluation set item.

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

## EvaluationSetRuns
<details><summary><code>client.evaluation_set_runs.<a href="src/extend_ai/evaluation_set_runs/client.py">retrieve</a>(...) -&gt; AsyncHttpResponse[EvaluationSetRun]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details of an evaluation set run.
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
client.evaluation_set_runs.retrieve(
    id="evaluation_set_run_id_here",
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

The ID of the evaluation set run.

Example: `"evr_Xj8mK2pL9nR4vT7qY5wZ"`
    
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

