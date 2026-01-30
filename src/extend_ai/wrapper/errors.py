"""
Custom error classes for the Extend SDK wrapper.
"""


class PollingTimeoutError(Exception):
    """Error thrown when polling exceeds the maximum wait time."""

    def __init__(self, message: str, elapsed_ms: int, max_wait_ms: int):
        super().__init__(message)
        self.elapsed_ms = elapsed_ms
        self.max_wait_ms = max_wait_ms


class WebhookSignatureVerificationError(Exception):
    """Error thrown when webhook signature verification fails."""

    pass


class WebhookPayloadFetchError(Exception):
    """Error thrown when fetching signed URL payload fails."""

    pass


class SignedUrlNotAllowedError(Exception):
    """Error thrown when a signed URL payload is received but not allowed."""

    def __init__(self):
        super().__init__(
            "Received signed URL payload but allow_signed_url option is not enabled. "
            "Either pass allow_signed_url=True to verify_and_parse() to handle signed URL payloads, "
            "or configure your webhook endpoint in the Extend dashboard to not use signed URLs."
        )
