# Extendconfig Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fextend-hq%2Fextend-python-sdk)
[![pypi](https://img.shields.io/pypi/v/extend_ai)](https://pypi.python.org/pypi/extend_ai)

The Extendconfig Python library provides convenient access to the Extendconfig APIs from Python.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Polling Helpers](#polling-helpers)
- [Running Workflows](#running-workflows)
- [Webhook Verification](#webhook-verification)
- [Async Support](#async-support)
- [Reference](#reference)
- [Usage](#usage)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Pagination](#pagination)
- [Environments](#environments)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Installation

```sh
pip install extend_ai
```

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

## Reference

A full reference for this library is available [here](https://github.com/extend-hq/extend-python-sdk/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

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

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from extend_ai import AsyncExtend, ParseRequestFile

client = AsyncExtend(
    token="YOUR_TOKEN",
)


async def main() -> None:
    await client.parse(
        response_type="json",
        file=ParseRequestFile(),
    )


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from extend_ai.core.api_error import ApiError

try:
    client.parse(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
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

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from extend_ai import Extend

client = Extend(
    ...,
)
response = client.with_raw_response.parse(...)
print(response.headers)  # access the response headers
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.parse(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from extend_ai import Extend

client = Extend(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.parse(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from extend_ai import Extend

client = Extend(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Documentation

API reference documentation is available [here](https://docs.extend.ai/2025-04-21/developers).

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
