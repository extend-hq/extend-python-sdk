# Extend Python Library

The Extend Python library provides convenient access to the Extend API from Python.

## Documentation

API reference documentation is available [here](https://docs.extend.ai/2026-02-09/developers).

## Installation

```sh
pip install extend-ai
```

## Reference

A full reference for this library is available [here](./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from extend_ai import Extend

client = Extend(token="YOUR_TOKEN")

# Create a workflow run
result = client.workflow_runs.create(
    file={"url": "https://example.com/doc.pdf"},
    workflow={"id": "workflow_id_here"},
)
```

## Polling Helpers

The SDK includes `create_and_poll()` methods for run resources that automatically poll until completion:

```python
from extend_ai import Extend

client = Extend(token="YOUR_TOKEN")

# Create and wait for extract run to complete
result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/doc.pdf"},
    extractor={"id": "extractor_123"},
)

print(f"Status: {result.extract_run.status}")  # PROCESSED or FAILED

# Works with all run types
classify_result = client.classify_runs.create_and_poll(
    file={"url": "https://example.com/doc.pdf"},
    classifier={"id": "classifier_123"},
)

workflow_result = client.workflow_runs.create_and_poll(
    file={"url": "https://example.com/doc.pdf"},
    workflow={"id": "workflow_123"},
)
```

### Custom Polling Options

```python
from extend_ai import Extend, PollingOptions

client = Extend(token="YOUR_TOKEN")

result = client.extract_runs.create_and_poll(
    file={"url": "https://example.com/doc.pdf"},
    extractor={"id": "extractor_123"},
    polling_options=PollingOptions(
        max_wait_ms=600_000,      # 10 minute timeout
        initial_delay_ms=2_000,   # Start with 2s delay
        max_delay_ms=30_000,      # Cap at 30s delay
    ),
)
```

## Webhook Verification

The SDK includes utilities for verifying webhook signatures:

```python
from extend_ai import Extend

client = Extend(token="YOUR_TOKEN")

# In your webhook handler
def handle_webhook(request):
    body = request.body.decode()
    headers = dict(request.headers)

    # Verify and parse the webhook
    event = client.webhooks.verify_and_parse(
        body=body,
        headers=headers,
        signing_secret="wss_your_signing_secret",
    )

    if event.get("eventType") == "workflow_run.completed":
        print("Workflow completed!")
        print(f"Run ID: {event['data']['id']}")
```

### Manual Verification

```python
# Just verify without parsing
is_valid = client.webhooks.verify(body, headers, signing_secret)

# Just parse without verification (not recommended for production)
event = client.webhooks.parse(body)
```

## Async Client

The SDK also exports an async client for non-blocking operations:

```python
import asyncio
from extend_ai import AsyncExtend

client = AsyncExtend(token="YOUR_TOKEN")

async def main():
    result = await client.extract_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        extractor={"id": "extractor_123"},
    )
    print(f"Status: {result.extract_run.status}")

asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error will be thrown:

```python
from extend_ai.core.api_error import ApiError

try:
    result = client.extract_runs.create(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

### Polling Timeout

When `create_and_poll()` exceeds its timeout, a `PollingTimeoutError` is raised:

```python
from extend_ai import Extend, PollingTimeoutError

client = Extend(token="YOUR_TOKEN")

try:
    result = client.extract_runs.create_and_poll(...)
except PollingTimeoutError as e:
    print(f"Polling timed out after {e.elapsed_ms}ms")
```

## Advanced

### Additional Headers

If you would like to send additional headers as part of the request, use the `headers` parameter:

```python
client = Extend(
    token="YOUR_TOKEN",
    headers={"X-Custom-Header": "custom value"},
)
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long as the request is deemed retryable and the number of retry attempts has not grown larger than the configured retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior:

```python
client.extract_runs.create(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 300 second timeout. Use the `timeout` option to configure this behavior:

```python
client = Extend(
    token="YOUR_TOKEN",
    timeout=30.0,
)

# Override timeout for a specific method
client.extract_runs.create(..., request_options={
    "timeout_in_seconds": 60
})
```

### Custom HTTP Client

You can override the `httpx` client to customize it for your use-case:

```python
import httpx
from extend_ai import Extend

client = Extend(
    token="YOUR_TOKEN",
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
