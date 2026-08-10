# Extend Python Library

Official Python SDK for [Extend](https://www.extend.ai) (extend.ai) — the document processing API. Parse, extract, classify, split, and edit PDFs and 35+ file types via PyPI (`extend-ai`).

[![PyPI version](https://img.shields.io/pypi/v/extend-ai.svg)](https://pypi.python.org/pypi/extend-ai)
[![Python versions](https://img.shields.io/pypi/pyversions/extend-ai.svg)](https://pypi.python.org/pypi/extend-ai)

The Extend Python library provides convenient, typed access to the [Extend API](https://docs.extend.ai/2026-02-09/developers) — enabling you to parse, extract, classify, split, and edit documents with a few lines of code.

## Installation

```sh
pip install extend-ai
```

> Requires Python 3.8+

## Quick start

Parse any document in three lines:

```python
from extend_ai import Extend

client = Extend(token="YOUR_API_KEY")

result = client.parse(file={"url": "https://example.com/invoice.pdf"})

for chunk in result.output.chunks:
    print(chunk.content)
```

`client.parse` is synchronous — it sends the file, waits for processing, and returns a fully populated `ParseRun` with parsed chunks ready to use. The same pattern works for every capability:

```python
# Extract structured data
extract_run = client.extract(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ex_abc123"},
)

# Classify a document
classify_run = client.classify(
    file={"url": "https://example.com/document.pdf"},
    classifier={"id": "cls_abc123"},
)

# Split a multi-document file
split_run = client.split(
    file={"url": "https://example.com/packet.pdf"},
    splitter={"id": "spl_abc123"},
)

# Edit a PDF with instructions
edit_run = client.edit(
    file={"url": "https://example.com/form.pdf"},
    config={"instructions": "Fill out the applicant name as Jane Doe"},
)
```

> **Note:** The synchronous methods above have a 5-minute timeout and are best suited for onboarding and testing. For production workloads, use [polling helpers](#polling-helpers) or [webhooks](#webhook-verification) instead.

## Typed extraction with Pydantic

The SDK supports [pydantic](https://docs.pydantic.dev/) models for fully typed extraction -- define your schema once and get end-to-end type safety from request to response:

```python
from typing import List, Optional

from pydantic import BaseModel, Field

from extend_ai import Extend, ExtendCurrency, ExtendDate

class LineItem(BaseModel):
    description: Optional[str] = None
    amount: Optional[ExtendCurrency] = None

class Invoice(BaseModel):
    invoice_number: Optional[str] = Field(None, description="The invoice number")
    invoice_date: ExtendDate = Field(None, description="The invoice date")
    line_items: List[LineItem] = Field(default_factory=list, description="Line items on the invoice")
    total: Optional[ExtendCurrency] = Field(None, description="Total amount due")

client = Extend(token="YOUR_API_KEY")

result = client.extract(
    file={"url": "https://example.com/invoice.pdf"},
    config={"schema": Invoice},
)

# output.value is a validated Invoice instance
if result.status == "PROCESSED" and result.output is not None:
    invoice = result.output.value
    print(invoice.invoice_number)  # str | None
    print(invoice.invoice_date)    # datetime.date | None
    if invoice.total is not None:
        print(invoice.total.amount)                  # float | None
        print(invoice.total.iso_4217_currency_code)  # str | None
```

The model is converted to [Extend's JSON Schema format](https://docs.extend.ai/2026-02-09/extraction/schema) for the request, and the extraction output is validated back into model instances. Use `Field(description=...)` to guide the extraction.

Metadata set via `Field(json_schema_extra=...)` is carried into the JSON Schema: `{"extend:name": "..."}` names a field, and enum fields accept `{"extend:descriptions": ["..."]}` with one description per enum value.

Primitive, enum, and date fields must be declared `Optional` -- extraction can return `null` for any field, so a non-Optional field raises `SchemaConversionError` before any request is sent. In the unlikely event that a completed run's output fails model validation, the SDK raises `ExtractOutputValidationError`, which preserves the completed run (including its raw output) on the error's `run` attribute.

Pydantic model schemas are accepted everywhere an extraction schema can be provided:

```python
# Polling (see below), including extractor config overrides
result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    config={"schema": Invoice},
)

# Creating and updating extractors
extractor = client.extractors.create(name="Invoice Extractor", config={"schema": Invoice})
client.extractors.update(extractor.id, config={"schema": Invoice})

# Publishing extractor versions
client.extractor_versions.create(extractor.id, release_type="major", config={"schema": Invoice})
```

### Custom field types

The SDK provides field types for Extend-specific extraction behavior:

| Type | Output type | Description |
|---|---|---|
| `ExtendDate` | `datetime.date \| None` | ISO date (plain `datetime.date` annotations work too) |
| `ExtendCurrency` | `ExtendCurrency(amount, iso_4217_currency_code)` | Currency with amount and code |
| `ExtendSignature` | `ExtendSignature(printed_name, signature_date, is_signed, title_or_role)` | Signature detection |

Supported field types: `Optional[str]`, `Optional[float]`, `Optional[int]`, `Optional[bool]`, `Optional[datetime.date]`, `Optional[Literal[...]]` / string enums (converted to nullable enums), nested models, and lists of these (list items are non-Optional, e.g. `List[str]`). Unsupported constructs (non-Optional unions, dicts, recursive models, field aliases, etc.) raise `SchemaConversionError`.

## Polling helpers

Every run resource exposes a `create_and_poll()` method that creates the run and automatically polls until it reaches a terminal state (`PROCESSED`, `FAILED`, or `CANCELLED`):

```python
from extend_ai import Extend

client = Extend(token="YOUR_API_KEY")

result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ex_abc123"},
)

if result.status == "PROCESSED":
    print(result.output)
else:
    print(f"Failed: {result.failure_message}")
```

This works across all run types:

```python
parse_run     = client.parse_runs.create_and_poll(file={"url": "..."})
extract_run   = client.extract_runs.create_and_poll(file={"url": "..."}, extractor={"id": "..."})
classify_run  = client.classify_runs.create_and_poll(file={"url": "..."}, classifier={"id": "..."})
split_run     = client.split_runs.create_and_poll(file={"url": "..."}, splitter={"id": "..."})
workflow_run  = client.workflow_runs.create_and_poll(file={"url": "..."}, workflow={"id": "..."})
edit_run      = client.edit_runs.create_and_poll(file={"url": "..."})
```

### Custom polling options

```python
from extend_ai import Extend, PollingOptions

result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ex_abc123"},
    polling_options=PollingOptions(
        max_wait_ms=300_000,       # 5 minute timeout (default: no timeout)
        initial_delay_ms=1_000,    # start with 1s delay (default)
        max_delay_ms=60_000,       # cap at 60s delay (default: 30s)
    ),
)
```

## Running workflows

Workflows chain multiple processing steps (extraction, classification, splitting, etc.) into a single pipeline. Run a workflow by passing a workflow ID and a file:

```python
result = client.workflow_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    workflow={"id": "workflow_abc123"},
)

print(result.status)  # "PROCESSED"

for step_run in result.step_runs or []:
    print(step_run.step.type)   # "EXTRACT", "CLASSIFY", etc.
    print(step_run.result)
```

## Webhook verification

Verify and parse incoming webhook events using the built-in utilities. Known event types are returned as typed Pydantic models; unknown or future event types fall back to a plain dict so your handler keeps working without SDK updates.

```python
from extend_ai import Extend

client = Extend(token="YOUR_API_KEY")

def handle_webhook(request):
    event = client.webhooks.verify_and_parse(
        body=request.body.decode(),
        headers=dict(request.headers),
        signing_secret="wss_your_signing_secret",
    )

    # Works for both typed model and dict fallback
    event_type = getattr(event, "event_type", None) or event.get("eventType")
    payload = getattr(event, "payload", None) or event.get("payload")

    match event_type:
        case "extract_run.processed":
            run_id = getattr(payload, "id", None) or payload.get("id")
            print(f"Extraction complete: {run_id}")
        case "workflow_run.completed":
            run_id = getattr(payload, "id", None) or payload.get("id")
            print(f"Workflow complete: {run_id}")
        case _:
            print(f"Received event: {event_type}")
```

### Manual verification & parsing

```python
# Verify signature without parsing
is_valid = client.webhooks.verify(body, headers, signing_secret)

# Parse without verification (not recommended for production)
event = client.webhooks.parse(body)
```

### Signed URL payloads

For large payloads, Extend may send a signed URL instead of the full payload. Use `allow_signed_url=True`, then check and fetch when needed:

```python
event = client.webhooks.verify_and_parse(
    body=body,
    headers=headers,
    signing_secret=signing_secret,
    allow_signed_url=True,
)

if client.webhooks.is_signed_url_event(event):
    full_event = client.webhooks.fetch_signed_payload_sync(event)
    # full_event is typed or dict; use getattr(..., None) or .get() as in the example above
else:
    # Normal inline payload — handle event directly
    ...
```

## Async support

Every method has an async counterpart via `AsyncExtend`:

```python
import asyncio
from extend_ai import AsyncExtend

client = AsyncExtend(token="YOUR_API_KEY")

async def main():
    result = await client.parse(file={"url": "https://example.com/invoice.pdf"})

    for chunk in result.output.chunks:
        print(chunk.content)

asyncio.run(main())
```

Async polling works the same way:

```python
result = await client.extract_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ex_abc123"},
)
```

## Exception handling

The SDK raises typed exceptions for API errors:

```python
from extend_ai.core.api_error import ApiError

try:
    result = client.parse(file={"url": "https://example.com/invoice.pdf"})
except ApiError as e:
    print(e.status_code)  # 400, 401, 404, 429, etc.
    print(e.body)
```

Specific error classes are available for fine-grained handling:

```python
from extend_ai.errors import (
    BadRequestError,         # 400
    UnauthorizedError,       # 401
    PaymentRequiredError,    # 402
    ForbiddenError,          # 403
    NotFoundError,           # 404
    UnprocessableEntityError,# 422
    TooManyRequestsError,    # 429
    InternalServerError,     # 500
)
```

### Polling timeout

When `create_and_poll()` exceeds its timeout, a `PollingTimeoutError` is raised:

```python
from extend_ai import PollingTimeoutError

try:
    result = client.extract_runs.create_and_poll(
        file={"url": "..."},
        extractor={"id": "..."},
        polling_options=PollingOptions(max_wait_ms=60_000),
    )
except PollingTimeoutError as e:
    print(f"Timed out after {e.elapsed_ms}ms (limit: {e.max_wait_ms}ms)")
```

## Pagination

List endpoints return paginated results using `next_page_token`:

```python
# First page
response = client.extract_runs.list(max_page_size=10)

for run in response.data:
    print(f"{run.id}: {run.status}")

# Next page
if response.next_page_token:
    next_page = client.extract_runs.list(
        max_page_size=10,
        next_page_token=response.next_page_token,
    )
```

## Environments

The SDK defaults to the US production environment. Other regions are available:

```python
from extend_ai import Extend, ExtendEnvironment

# US (default)
client = Extend(token="YOUR_API_KEY")

# US2 (HIPAA)
client = Extend(token="YOUR_API_KEY", environment=ExtendEnvironment.PRODUCTION_US2)

# EU
client = Extend(token="YOUR_API_KEY", environment=ExtendEnvironment.PRODUCTION_EU1)

# Custom base URL
client = Extend(token="YOUR_API_KEY", base_url="https://custom-api.example.com")
```

## Advanced

### Retries

The SDK automatically retries failed requests with exponential backoff. Retries are triggered for:

- `408` Timeout
- `429` Too Many Requests
- `5xx` Server Errors

```python
# Override retries for a single request
client.extract_runs.create(..., request_options={"max_retries": 0})
```

### Timeouts

The default timeout is 300 seconds. Override globally or per-request:

```python
# Global timeout
client = Extend(token="YOUR_API_KEY", timeout=30.0)

# Per-request timeout
client.extract_runs.create(..., request_options={"timeout_in_seconds": 60})
```

### Custom headers

```python
client = Extend(
    token="YOUR_API_KEY",
    headers={"X-Custom-Header": "value"},
)
```

### Custom HTTP client

Pass a pre-configured `httpx.Client` for full control over transport:

```python
import httpx
from extend_ai import Extend

client = Extend(
    token="YOUR_API_KEY",
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

### Raw responses

Access the underlying HTTP response for any request:

```python
raw_response = client.with_raw_response.parse(file={"url": "https://example.com/invoice.pdf"})

print(raw_response.status_code)
print(raw_response.headers)
print(raw_response.data)  # ParseRun
```

## Documentation

Full API reference documentation is available at [docs.extend.ai](https://docs.extend.ai/2026-02-09/developers).

A complete SDK reference is available in [reference.md](./reference.md).

## Custom patches

This SDK includes patches to Fern-generated core files that fix bugs not yet addressed upstream. These files are listed in [`.fernignore`](.fernignore) so Fern does not overwrite them during generation.

| File | What it fixes |
|---|---|
| `src/extend_ai/core/serialization.py` | Circular TypedDict alias resolution on Python 3.10+ (field aliases like `extend_edit:bbox` were sent with underscores) |
| `src/extend_ai/core/unchecked_base_model.py` | ForwardRef resolution for `Chunk.blocks`, strict union discriminant matching for `BlockDetails`, enum serialization warnings |

Each patch has regression tests in `tests/custom/`. If a Fern update accidentally overwrites a patched file, CI will fail.

### Maintaining patches

1. Make your fix on a branch, add regression tests in `tests/custom/`
2. Add the patched file to `.fernignore` if not already listed
3. If the fix applies to the v0 API, cherry-pick it onto the `v0.x` branch and update `.fernignore` there too
4. Note: `.fernignore` means Fern won't auto-update the file — if Fern releases upstream improvements, merge them manually

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
