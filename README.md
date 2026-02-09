# Extend Python Library

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
    extractor={"id": "ext_abc123"},
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

# Fill form fields in a PDF
edit_run = client.edit(
    file={"url": "https://example.com/form.pdf"},
    config={"fields": [{"name": "Full Name", "value": "Jane Doe"}]},
)
```

> **Note:** The synchronous methods above have a 5-minute timeout and are best suited for onboarding and testing. For production workloads, use [polling helpers](#polling-helpers) or [webhooks](#webhook-verification) instead.

## Polling helpers

Every run resource exposes a `create_and_poll()` method that creates the run and automatically polls until it reaches a terminal state (`PROCESSED`, `FAILED`, or `CANCELLED`):

```python
from extend_ai import Extend

client = Extend(token="YOUR_API_KEY")

result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ext_abc123"},
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
    extractor={"id": "ext_abc123"},
    polling_options=PollingOptions(
        max_wait_ms=300_000,       # 5 minute timeout (default: no timeout)
        initial_delay_ms=1_000,    # start with 1s delay (default)
        max_delay_ms=60_000,       # cap at 60s delay (default: 30s)
    ),
)
```

## Webhook verification

Verify and parse incoming webhook events using the built-in utilities:

```python
from extend_ai import Extend

client = Extend(token="YOUR_API_KEY")

def handle_webhook(request):
    event = client.webhooks.verify_and_parse(
        body=request.body.decode(),
        headers=dict(request.headers),
        signing_secret="wss_your_signing_secret",
    )

    match event.get("eventType"):
        case "extract_run.processed":
            print(f"Extraction complete: {event['data']['id']}")
        case "workflow_run.completed":
            print(f"Workflow complete: {event['data']['id']}")
        case _:
            print(f"Received event: {event['eventType']}")
```

### Manual verification & parsing

```python
# Verify signature without parsing
is_valid = client.webhooks.verify(body, headers, signing_secret)

# Parse without verification (not recommended for production)
event = client.webhooks.parse(body)
```

### Signed URL payloads

For large payloads, Extend may send a signed URL instead of the full payload. The SDK handles this transparently:

```python
event = client.webhooks.verify_and_parse(
    body=body,
    headers=headers,
    signing_secret=signing_secret,
    allow_signed_url=True,
)

if client.webhooks.is_signed_url_event(event):
    full_payload = client.webhooks.fetch_signed_payload_sync(event)
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
    extractor={"id": "ext_abc123"},
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

### API versioning

The SDK targets a specific API version by default. Override it if needed:

```python
client = Extend(token="YOUR_API_KEY", extend_api_version="2026-02-09")
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

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
