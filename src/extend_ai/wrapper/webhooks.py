"""
Webhook utilities for signature verification and event parsing.

Example:
    from extend_ai import Extend

    client = Extend(token="...")

    @app.post("/webhook")
    def handle_webhook(request):
        try:
            event = client.webhooks.verify_and_parse(
                body=request.body.decode(),
                headers=dict(request.headers),
                signing_secret="wss_your_signing_secret"
            )

            if event.event_type == "workflow_run.completed":
                print("Workflow completed:", event.payload)

            return {"status": "ok"}
        except WebhookSignatureVerificationError:
            return {"error": "Invalid signature"}, 401
"""

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import httpx

from .errors import SignedUrlNotAllowedError, WebhookPayloadFetchError, WebhookSignatureVerificationError


@dataclass
class SignedDataUrlPayload:
    """Payload structure when webhook is delivered via signed URL (for large payloads)."""

    data: str  # The signed URL to fetch the full payload (expires in 1 hour)
    id: str  # The ID of the run/resource
    object: str  # Discriminator indicating this is a signed URL payload ("signed_data_url")
    metadata: Optional[Dict[str, Any]] = None  # Optional metadata passed when the run was created


@dataclass
class WebhookEventWithSignedUrl:
    """Webhook event when payload is delivered via signed URL (before fetching)."""

    event_id: str  # Unique identifier for this webhook event
    event_type: str  # The type of event (e.g., "workflow_run.completed")
    payload: SignedDataUrlPayload  # The signed URL payload - use fetch_signed_payload() to get the full data


# Union type representing either a normal webhook event or one with a signed URL payload
RawWebhookEvent = Union[Any, WebhookEventWithSignedUrl]  # Any represents the generated WebhookEvent types


def _is_signed_data_url_payload(payload: Any) -> bool:
    """Check if a payload is a signed URL payload."""
    if not isinstance(payload, dict):
        return False
    return payload.get("object") == "signed_data_url" and isinstance(payload.get("data"), str)


class Webhooks:
    """
    Webhook utilities for signature verification and event parsing.

    Example:
        client = Extend(token="...")

        # Simple usage - verify and parse in one step
        event = client.webhooks.verify_and_parse(body, headers, secret)

        # Or verify first, then parse separately
        if client.webhooks.verify(body, headers, secret):
            event = client.webhooks.parse(body)
            # handle event
    """

    def verify_and_parse(
        self,
        body: str,
        headers: Dict[str, Any],
        signing_secret: str,
        max_age_seconds: int = 300,
        allow_signed_url: bool = False,
    ) -> RawWebhookEvent:
        """
        Verifies the webhook signature and parses the event.

        By default, this method returns a WebhookEvent. If the webhook contains a
        signed URL payload (used for large payloads), it throws a SignedUrlNotAllowedError.

        To handle signed URL payloads, pass allow_signed_url=True. Use is_signed_url_event()
        to check if you received a signed URL, then call fetch_signed_payload() to get the
        full payload.

        Args:
            body: The raw request body as a string
            headers: The request headers (must include x-extend-request-timestamp and
                    x-extend-request-signature)
            signing_secret: Your webhook signing secret (starts with wss_)
            max_age_seconds: Maximum age of the request in seconds (default: 300 = 5 minutes).
                            Set to 0 to disable timestamp validation.
            allow_signed_url: Whether to allow signed URL payloads. Default: False.
                            When False: Raises SignedUrlNotAllowedError if a signed URL payload
                            is received.
                            When True: Returns RawWebhookEvent (may be WebhookEventWithSignedUrl).

        Returns:
            The verified and parsed webhook event

        Raises:
            WebhookSignatureVerificationError: If signature verification fails
            SignedUrlNotAllowedError: If a signed URL payload is received without
                                     allow_signed_url=True

        Example:
            # Simple usage (most users) - raises if signed URL received
            event = client.webhooks.verify_and_parse(body, headers, secret)

            # Handle signed URL payloads
            event = client.webhooks.verify_and_parse(body, headers, secret, allow_signed_url=True)
            if client.webhooks.is_signed_url_event(event):
                # Check metadata before fetching (e.g., environment check)
                if event.payload.metadata.get("env") == "production":
                    full_event = await client.webhooks.fetch_signed_payload(event)
                    # handle full_event
            else:
                # Normal inline payload
                # handle event
        """
        # Verify the signature
        self._verify_signature(body, headers, signing_secret, max_age_seconds)

        # Parse the event
        try:
            event_data = json.loads(body)
        except json.JSONDecodeError as e:
            raise WebhookSignatureVerificationError(f"Failed to parse webhook body as JSON: {e}")

        # Check if it's a signed URL payload
        payload = event_data.get("payload", {})
        if _is_signed_data_url_payload(payload):
            if not allow_signed_url:
                raise SignedUrlNotAllowedError()

            # Return as WebhookEventWithSignedUrl
            return WebhookEventWithSignedUrl(
                event_id=event_data.get("eventId", ""),
                event_type=event_data.get("eventType", ""),
                payload=SignedDataUrlPayload(
                    data=payload.get("data", ""),
                    id=payload.get("id", ""),
                    object=payload.get("object", ""),
                    metadata=payload.get("metadata"),
                ),
            )

        # Return typed event when possible, fall back to raw dict for unknown event types
        return self._try_parse_webhook_event(event_data)

    def verify(
        self,
        body: str,
        headers: Dict[str, Any],
        signing_secret: str,
        max_age_seconds: int = 300,
    ) -> bool:
        """
        Verifies a webhook signature without parsing the body.

        Args:
            body: The raw request body as a string
            headers: The request headers
            signing_secret: Your webhook signing secret
            max_age_seconds: Maximum age of the request in seconds (default: 300)

        Returns:
            True if the signature is valid, False otherwise

        Example:
            is_valid = client.webhooks.verify(body, headers, secret)
            if is_valid:
                event = client.webhooks.parse(body)
                # handle event
        """
        try:
            self._verify_signature(body, headers, signing_secret, max_age_seconds)
            return True
        except Exception:
            return False

    def parse(self, body: str) -> RawWebhookEvent:
        """
        Parses a webhook event from a raw body without verification.
        Use this only if you've already verified the signature using verify().

        Args:
            body: The raw request body as a string

        Returns:
            The parsed webhook event (may be a signed URL event)

        Example:
            if client.webhooks.verify(body, headers, secret):
                event = client.webhooks.parse(body)
                if client.webhooks.is_signed_url_event(event):
                    full_event = await client.webhooks.fetch_signed_payload(event)
        """
        event_data = json.loads(body)

        # Check if it's a signed URL payload
        payload = event_data.get("payload", {})
        if _is_signed_data_url_payload(payload):
            return WebhookEventWithSignedUrl(
                event_id=event_data.get("eventId", ""),
                event_type=event_data.get("eventType", ""),
                payload=SignedDataUrlPayload(
                    data=payload.get("data", ""),
                    id=payload.get("id", ""),
                    object=payload.get("object", ""),
                    metadata=payload.get("metadata"),
                ),
            )

        return self._try_parse_webhook_event(event_data)

    async def fetch_signed_payload(self, event: WebhookEventWithSignedUrl) -> Any:
        """
        Fetches the full payload from a signed URL webhook event.

        Use this when you've received a WebhookEventWithSignedUrl (from verify_and_parse
        with allow_signed_url=True) and want to retrieve the full payload.

        Args:
            event: The webhook event with a signed URL payload

        Returns:
            The full webhook event with the resolved payload

        Raises:
            WebhookPayloadFetchError: If fetching the signed URL fails

        Example:
            event = client.webhooks.verify_and_parse(body, headers, secret, allow_signed_url=True)
            if client.webhooks.is_signed_url_event(event):
                # Check metadata before fetching (e.g., environment check)
                if event.payload.metadata.get("env") == "production":
                    full_event = await client.webhooks.fetch_signed_payload(event)
                    # full_event["payload"] is now the full WorkflowRun, ExtractRun, etc.
        """
        url = event.payload.data

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

                if not response.is_success:
                    raise WebhookPayloadFetchError(
                        f"Failed to fetch signed payload: {response.status_code} {response.reason_phrase}"
                    )

                full_payload = response.json()

                full_event = {
                    "eventId": event.event_id,
                    "eventType": event.event_type,
                    "payload": full_payload,
                }
                return self._try_parse_webhook_event(full_event)
        except WebhookPayloadFetchError:
            raise
        except Exception as e:
            raise WebhookPayloadFetchError(f"Failed to fetch signed payload: {e}")

    def fetch_signed_payload_sync(self, event: WebhookEventWithSignedUrl) -> Any:
        """
        Fetches the full payload from a signed URL webhook event (synchronous version).

        Args:
            event: The webhook event with a signed URL payload

        Returns:
            The full webhook event with the resolved payload

        Raises:
            WebhookPayloadFetchError: If fetching the signed URL fails
        """
        url = event.payload.data

        try:
            with httpx.Client() as client:
                response = client.get(url)

                if not response.is_success:
                    raise WebhookPayloadFetchError(
                        f"Failed to fetch signed payload: {response.status_code} {response.reason_phrase}"
                    )

                full_payload = response.json()

                full_event = {
                    "eventId": event.event_id,
                    "eventType": event.event_type,
                    "payload": full_payload,
                }
                return self._try_parse_webhook_event(full_event)
        except WebhookPayloadFetchError:
            raise
        except Exception as e:
            raise WebhookPayloadFetchError(f"Failed to fetch signed payload: {e}")

    def is_signed_url_event(self, event: RawWebhookEvent) -> bool:
        """
        Check if a webhook event has a signed URL payload.

        Use this to determine if you need to call fetch_signed_payload() to get the
        full payload.

        Args:
            event: The webhook event to check

        Returns:
            True if the event has a signed URL payload

        Example:
            event = client.webhooks.verify_and_parse(body, headers, secret, allow_signed_url=True)
            if client.webhooks.is_signed_url_event(event):
                # event is WebhookEventWithSignedUrl
                print("Signed URL:", event.payload.data)
                print("Metadata:", event.payload.metadata)
            else:
                # event is WebhookEvent
                print("Full payload:", event.get("payload"))
        """
        if isinstance(event, WebhookEventWithSignedUrl):
            return True
        if isinstance(event, dict):
            return _is_signed_data_url_payload(event.get("payload", {}))
        return False

    def _try_parse_webhook_event(self, event_data: Dict[str, Any]) -> Any:
        """Try to parse as typed WebhookEvent, fall back to raw dict for unknown event types."""
        try:
            from ..types.webhook_event import WebhookEvent
            from ..core.unchecked_base_model import construct_type
            return construct_type(type_=WebhookEvent, object_=event_data)
        except Exception:
            return event_data

    def _verify_signature(
        self,
        body: str,
        headers: Dict[str, Any],
        signing_secret: str,
        max_age_seconds: int = 300,
    ) -> None:
        """Verifies the webhook signature. Raises on failure."""
        # Extract headers (handle case-insensitive lookup)
        timestamp = self._get_header(headers, "x-extend-request-timestamp")
        signature = self._get_header(headers, "x-extend-request-signature")

        if not timestamp:
            raise WebhookSignatureVerificationError("Missing x-extend-request-timestamp header")

        if not signature:
            raise WebhookSignatureVerificationError("Missing x-extend-request-signature header")

        if not signing_secret:
            raise WebhookSignatureVerificationError("Missing signing secret")

        # Validate timestamp to prevent replay attacks
        if max_age_seconds > 0:
            current_time = int(time.time())
            try:
                request_time = int(timestamp)
            except ValueError:
                raise WebhookSignatureVerificationError("Invalid timestamp format")

            age = current_time - request_time
            if age > max_age_seconds:
                raise WebhookSignatureVerificationError(
                    f"Request timestamp too old ({age}s > {max_age_seconds}s)"
                )

            if age < -60:  # Allow 1 minute clock skew
                raise WebhookSignatureVerificationError("Request timestamp in the future")

        # Compute expected signature
        message = f"v0:{timestamp}:{body}"
        expected_signature = hmac.new(
            signing_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        # Use timing-safe comparison to prevent timing attacks
        if not hmac.compare_digest(signature, expected_signature):
            raise WebhookSignatureVerificationError("Invalid signature")

    def _get_header(self, headers: Dict[str, Any], name: str) -> Optional[str]:
        """Get a header value (case-insensitive)."""
        # Try exact match first
        value = headers.get(name) or headers.get(name.lower())

        if isinstance(value, list):
            return value[0] if value else None

        return value
