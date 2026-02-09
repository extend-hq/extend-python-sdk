"""
Extend SDK wrapper module with polling utilities and webhook verification.

This module provides extended versions of the generated SDK clients with:
- `create_and_poll()` methods for convenient polling
- Webhook signature verification utilities
- Custom error classes

Example:
    from extend_ai import Extend

    client = Extend(token="your-api-key")

    # Use create_and_poll for convenient polling
    result = client.extract_runs.create_and_poll(
        file={"url": "https://example.com/doc.pdf"},
        extractor={"id": "extractor_123"},
    )

    # Verify webhooks
    event = client.webhooks.verify_and_parse(body, headers, secret)
"""

from .client import AsyncExtend, Extend
from .errors import (
    PollingTimeoutError,
    SignedUrlNotAllowedError,
    WebhookParseError,
    WebhookPayloadFetchError,
    WebhookSignatureVerificationError,
)
from .polling import PollingOptions, calculate_backoff_delay, poll_until_done, poll_until_done_async
from .webhooks import RawWebhookEvent, SignedDataUrlPayload, WebhookEventWithSignedUrl, Webhooks

__all__ = [
    # Client
    "Extend",
    "AsyncExtend",
    # Webhooks
    "Webhooks",
    "RawWebhookEvent",
    "WebhookEventWithSignedUrl",
    "SignedDataUrlPayload",
    # Polling
    "PollingOptions",
    "poll_until_done",
    "poll_until_done_async",
    "calculate_backoff_delay",
    # Errors
    "PollingTimeoutError",
    "WebhookSignatureVerificationError",
    "WebhookParseError",
    "WebhookPayloadFetchError",
    "SignedUrlNotAllowedError",
]
