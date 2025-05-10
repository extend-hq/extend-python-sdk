# Extendconfig Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fextend-hq%2Fextend-python-sdk)
[![pypi](https://img.shields.io/pypi/v/extend_ai)](https://pypi.python.org/pypi/extend_ai)

The Extendconfig Python library provides convenient access to the Extendconfig API from Python.

## Documentation

API reference documentation is available [here](https://docs.extend.ai/2025-04-21/developers/authentication).

## Installation

```sh
pip install extend_ai
```

## Reference

A full reference for this library is available [here](./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from extend_ai import Extend
client = Extend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
client.run_workflow(workflow_id='workflow_id_here', )
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
from extend_ai import AsyncExtend
import asyncio
client = AsyncExtend(extend_api_version="YOUR_EXTEND_API_VERSION", token="YOUR_TOKEN", )
async def main() -> None:
    await client.run_workflow(workflow_id='workflow_id_here', )
asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from extend_ai.core.api_error import ApiError
try:
    client.run_workflow(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from extend_ai import Extend
client = Extend(..., )
response = client.with_raw_response.run_workflow(...)
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
client.run_workflow(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from extend_ai import Extend
client = Extend(..., timeout=20.0, )

# Override timeout for a specific method
client.run_workflow(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
from extend_ai import Extend
import httpx
client = Extend(..., httpx_client=httpx.Client(proxies="http://my.test.proxy.example.com", transport=httpx.HTTPTransport(local_address="0.0.0.0"), ))```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
