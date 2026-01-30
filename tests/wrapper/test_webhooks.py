"""Tests for webhook utilities."""

import hashlib
import hmac
import json
import time
from typing import Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from extend_ai.wrapper.webhooks import (
    Webhooks,
    WebhookEventWithSignedUrl,
    SignedDataUrlPayload,
)
from extend_ai.wrapper.errors import (
    WebhookSignatureVerificationError,
    SignedUrlNotAllowedError,
    WebhookPayloadFetchError,
)


# ============================================================================
# Test Helpers
# ============================================================================


def create_signature(body: str, secret: str, timestamp: int) -> str:
    """Create a valid webhook signature."""
    message = f"v0:{timestamp}:{body}"
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()


def create_valid_headers(body: str, secret: str, timestamp: Optional[int] = None) -> Dict[str, str]:
    """Create valid webhook headers."""
    ts = timestamp if timestamp is not None else int(time.time())
    return {
        "x-extend-request-timestamp": str(ts),
        "x-extend-request-signature": create_signature(body, secret, ts),
    }


# Sample webhook event payloads
SAMPLE_WORKFLOW_RUN_EVENT = {
    "eventId": "evt_123",
    "eventType": "workflow_run.completed",
    "payload": {
        "object": "workflow_run",
        "id": "workflow_run_abc123",
        "status": "PROCESSED",
        "workflow": {
            "object": "workflow_summary",
            "id": "workflow_123",
            "name": "Test Workflow",
        },
    },
}

SAMPLE_EXTRACT_RUN_EVENT = {
    "eventId": "evt_456",
    "eventType": "extract_run.processed",
    "payload": {
        "object": "extract_run",
        "id": "extract_run_def456",
        "status": "PROCESSED",
        "output": {"value": {"field": "value"}},
    },
}

SAMPLE_SIGNED_URL_EVENT = {
    "eventId": "evt_789",
    "eventType": "workflow_run.completed",
    "payload": {
        "object": "signed_data_url",
        "data": "https://storage.example.com/signed-payload?token=abc123",
        "id": "wr_xyz",
        "metadata": {"env": "production"},
    },
}

SECRET = "wss_test_secret_123"


# ============================================================================
# Tests
# ============================================================================


class TestVerifyAndParse:
    """Tests for verify_and_parse method."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_returns_event_for_valid_signature(self):
        """Should return WebhookEvent for normal payload with valid signature."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        event = self.webhooks.verify_and_parse(body, headers, SECRET)

        assert event["eventId"] == "evt_123"
        assert event["eventType"] == "workflow_run.completed"
        assert event["payload"] == SAMPLE_WORKFLOW_RUN_EVENT["payload"]

    def test_returns_event_for_extract_run_processed(self):
        """Should return WebhookEvent for extract_run.processed."""
        body = json.dumps(SAMPLE_EXTRACT_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        event = self.webhooks.verify_and_parse(body, headers, SECRET)

        assert event["eventId"] == "evt_456"
        assert event["eventType"] == "extract_run.processed"

    def test_throws_signed_url_not_allowed_error_without_opt_in(self):
        """Should throw SignedUrlNotAllowedError for signed URL payload without opt-in."""
        body = json.dumps(SAMPLE_SIGNED_URL_EVENT)
        headers = create_valid_headers(body, SECRET)

        with pytest.raises(SignedUrlNotAllowedError):
            self.webhooks.verify_and_parse(body, headers, SECRET)

    def test_returns_signed_url_event_with_allow_signed_url(self):
        """Should return WebhookEventWithSignedUrl with allow_signed_url=True."""
        body = json.dumps(SAMPLE_SIGNED_URL_EVENT)
        headers = create_valid_headers(body, SECRET)

        event = self.webhooks.verify_and_parse(body, headers, SECRET, allow_signed_url=True)

        assert isinstance(event, WebhookEventWithSignedUrl)
        assert event.event_id == "evt_789"
        assert event.event_type == "workflow_run.completed"
        assert event.payload.object == "signed_data_url"
        assert event.payload.data == "https://storage.example.com/signed-payload?token=abc123"
        assert event.payload.metadata["env"] == "production"

    def test_returns_normal_event_with_allow_signed_url_when_not_signed(self):
        """Should return normal event with allow_signed_url=True when not signed URL."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        event = self.webhooks.verify_and_parse(body, headers, SECRET, allow_signed_url=True)

        assert not self.webhooks.is_signed_url_event(event)
        assert event["eventType"] == "workflow_run.completed"


class TestVerifyAndParseInvalidSignature:
    """Tests for verify_and_parse with invalid signatures."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_throws_for_wrong_signature(self):
        """Should throw WebhookSignatureVerificationError for wrong signature."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = {
            "x-extend-request-timestamp": str(int(time.time())),
            "x-extend-request-signature": "invalid_signature",
        }

        with pytest.raises(WebhookSignatureVerificationError):
            self.webhooks.verify_and_parse(body, headers, SECRET)

    def test_throws_for_missing_timestamp_header(self):
        """Should throw for missing timestamp header."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = {"x-extend-request-signature": "some_signature"}

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "x-extend-request-timestamp" in str(exc_info.value)

    def test_throws_for_missing_signature_header(self):
        """Should throw for missing signature header."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = {"x-extend-request-timestamp": str(int(time.time()))}

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "x-extend-request-signature" in str(exc_info.value)

    def test_throws_for_missing_signing_secret(self):
        """Should throw for missing signing secret."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, "")

        assert "signing secret" in str(exc_info.value).lower()

    def test_throws_for_tampered_body(self):
        """Should throw for tampered body."""
        original_body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(original_body, SECRET)
        tampered_body = json.dumps({**SAMPLE_WORKFLOW_RUN_EVENT, "eventId": "evt_tampered"})

        with pytest.raises(WebhookSignatureVerificationError):
            self.webhooks.verify_and_parse(tampered_body, headers, SECRET)

    def test_throws_for_wrong_secret(self):
        """Should throw for wrong secret."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        with pytest.raises(WebhookSignatureVerificationError):
            self.webhooks.verify_and_parse(body, headers, "wrong_secret")


class TestTimestampValidation:
    """Tests for timestamp validation."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_rejects_old_requests(self):
        """Should reject requests older than max_age_seconds."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        old_timestamp = int(time.time()) - 600  # 10 minutes ago
        headers = create_valid_headers(body, SECRET, old_timestamp)

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "too old" in str(exc_info.value).lower()

    def test_accepts_recent_requests(self):
        """Should accept requests within max_age_seconds."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        recent_timestamp = int(time.time()) - 60  # 1 minute ago
        headers = create_valid_headers(body, SECRET, recent_timestamp)

        event = self.webhooks.verify_and_parse(body, headers, SECRET)
        assert event["eventId"] == "evt_123"

    def test_allows_custom_max_age_seconds(self):
        """Should allow custom max_age_seconds."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        old_timestamp = int(time.time()) - 600  # 10 minutes ago
        headers = create_valid_headers(body, SECRET, old_timestamp)

        # Should fail with default (300s)
        with pytest.raises(WebhookSignatureVerificationError):
            self.webhooks.verify_and_parse(body, headers, SECRET)

        # Should succeed with 900s
        event = self.webhooks.verify_and_parse(body, headers, SECRET, max_age_seconds=900)
        assert event["eventId"] == "evt_123"

    def test_disables_timestamp_validation_when_zero(self):
        """Should disable timestamp validation when max_age_seconds is 0."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        very_old_timestamp = int(time.time()) - 86400  # 1 day ago
        headers = create_valid_headers(body, SECRET, very_old_timestamp)

        event = self.webhooks.verify_and_parse(body, headers, SECRET, max_age_seconds=0)
        assert event["eventId"] == "evt_123"

    def test_rejects_future_timestamps(self):
        """Should reject timestamps too far in the future."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        future_timestamp = int(time.time()) + 120  # 2 minutes in future
        headers = create_valid_headers(body, SECRET, future_timestamp)

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "future" in str(exc_info.value).lower()

    def test_accepts_slight_clock_skew(self):
        """Should accept timestamps slightly in the future (clock skew)."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        slightly_future = int(time.time()) + 30  # 30 seconds in future
        headers = create_valid_headers(body, SECRET, slightly_future)

        event = self.webhooks.verify_and_parse(body, headers, SECRET)
        assert event["eventId"] == "evt_123"

    def test_throws_for_invalid_timestamp_format(self):
        """Should throw for invalid timestamp format."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = {
            "x-extend-request-timestamp": "not-a-number",
            "x-extend-request-signature": create_signature(body, SECRET, 0),
        }

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "timestamp" in str(exc_info.value).lower()


class TestJsonParsing:
    """Tests for JSON parsing."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_throws_for_invalid_json(self):
        """Should throw for invalid JSON body."""
        body = "not valid json"
        headers = create_valid_headers(body, SECRET)

        with pytest.raises(WebhookSignatureVerificationError) as exc_info:
            self.webhooks.verify_and_parse(body, headers, SECRET)

        assert "json" in str(exc_info.value).lower()


class TestCaseInsensitiveHeaders:
    """Tests for case-insensitive header handling."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_works_with_lowercase_headers(self):
        """Should work with lowercase header names."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        ts = int(time.time())
        headers = {
            "x-extend-request-timestamp": str(ts),
            "x-extend-request-signature": create_signature(body, SECRET, ts),
        }

        event = self.webhooks.verify_and_parse(body, headers, SECRET)
        assert event["eventId"] == "evt_123"

    def test_works_with_array_header_values(self):
        """Should work with array header values."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        ts = int(time.time())
        headers = {
            "x-extend-request-timestamp": [str(ts)],
            "x-extend-request-signature": [create_signature(body, SECRET, ts)],
        }

        event = self.webhooks.verify_and_parse(body, headers, SECRET)
        assert event["eventId"] == "evt_123"


class TestVerify:
    """Tests for verify method."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_returns_true_for_valid_signature(self):
        """Should return True for valid signature."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = create_valid_headers(body, SECRET)

        assert self.webhooks.verify(body, headers, SECRET) is True

    def test_returns_false_for_invalid_signature(self):
        """Should return False for invalid signature."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        headers = {
            "x-extend-request-timestamp": str(int(time.time())),
            "x-extend-request-signature": "invalid",
        }

        assert self.webhooks.verify(body, headers, SECRET) is False

    def test_returns_false_for_missing_headers(self):
        """Should return False for missing headers."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        assert self.webhooks.verify(body, {}, SECRET) is False

    def test_returns_false_for_expired_timestamp(self):
        """Should return False for expired timestamp."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        old_timestamp = int(time.time()) - 600
        headers = create_valid_headers(body, SECRET, old_timestamp)

        assert self.webhooks.verify(body, headers, SECRET) is False

    def test_respects_max_age_seconds_option(self):
        """Should respect max_age_seconds option."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)
        old_timestamp = int(time.time()) - 600
        headers = create_valid_headers(body, SECRET, old_timestamp)

        assert self.webhooks.verify(body, headers, SECRET) is False
        assert self.webhooks.verify(body, headers, SECRET, max_age_seconds=900) is True


class TestParse:
    """Tests for parse method."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_parses_normal_webhook_event(self):
        """Should parse a normal webhook event."""
        body = json.dumps(SAMPLE_WORKFLOW_RUN_EVENT)

        event = self.webhooks.parse(body)

        assert event["eventId"] == "evt_123"
        assert event["eventType"] == "workflow_run.completed"

    def test_parses_signed_url_webhook_event(self):
        """Should parse a signed URL webhook event."""
        body = json.dumps(SAMPLE_SIGNED_URL_EVENT)

        event = self.webhooks.parse(body)

        assert isinstance(event, WebhookEventWithSignedUrl)
        assert event.event_id == "evt_789"
        assert self.webhooks.is_signed_url_event(event) is True

    def test_throws_for_invalid_json(self):
        """Should throw for invalid JSON."""
        with pytest.raises(json.JSONDecodeError):
            self.webhooks.parse("not json")


class TestIsSignedUrlEvent:
    """Tests for is_signed_url_event method."""

    def setup_method(self):
        self.webhooks = Webhooks()

    def test_returns_true_for_signed_url_events(self):
        """Should return True for signed URL events."""
        event = WebhookEventWithSignedUrl(
            event_id="evt_789",
            event_type="workflow_run.completed",
            payload=SignedDataUrlPayload(
                data="https://example.com/signed",
                id="wr_xyz",
                object="signed_data_url",
                metadata=None,
            ),
        )
        assert self.webhooks.is_signed_url_event(event) is True

    def test_returns_false_for_normal_events(self):
        """Should return False for normal events."""
        event = SAMPLE_WORKFLOW_RUN_EVENT
        assert self.webhooks.is_signed_url_event(event) is False


class TestFetchSignedPayload:
    """Tests for fetch_signed_payload method."""

    def setup_method(self):
        self.webhooks = Webhooks()
        self.signed_event = WebhookEventWithSignedUrl(
            event_id="evt_789",
            event_type="workflow_run.completed",
            payload=SignedDataUrlPayload(
                data="https://storage.example.com/signed-payload?token=abc123",
                id="wr_xyz",
                object="signed_data_url",
                metadata={"env": "production"},
            ),
        )

    @pytest.mark.asyncio
    async def test_fetches_and_returns_full_event(self):
        """Should fetch and return the full event."""
        full_payload = {
            "id": "wr_xyz",
            "object": "workflow_run",
            "status": "PROCESSED",
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = full_payload

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__aenter__.return_value = mock_client

            result = await self.webhooks.fetch_signed_payload(self.signed_event)

            mock_client.get.assert_called_once_with(self.signed_event.payload.data)
            assert result["eventId"] == "evt_789"
            assert result["eventType"] == "workflow_run.completed"
            assert result["payload"] == full_payload

    @pytest.mark.asyncio
    async def test_throws_on_http_error(self):
        """Should throw WebhookPayloadFetchError on HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.reason_phrase = "Forbidden"

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__aenter__.return_value = mock_client

            with pytest.raises(WebhookPayloadFetchError) as exc_info:
                await self.webhooks.fetch_signed_payload(self.signed_event)

            assert "403" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_throws_on_network_error(self):
        """Should throw WebhookPayloadFetchError on network error."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = Exception("Network error")
            mock_client_class.return_value.__aenter__.return_value = mock_client

            with pytest.raises(WebhookPayloadFetchError) as exc_info:
                await self.webhooks.fetch_signed_payload(self.signed_event)

            assert "Network error" in str(exc_info.value)


class TestFetchSignedPayloadSync:
    """Tests for fetch_signed_payload_sync method."""

    def setup_method(self):
        self.webhooks = Webhooks()
        self.signed_event = WebhookEventWithSignedUrl(
            event_id="evt_789",
            event_type="workflow_run.completed",
            payload=SignedDataUrlPayload(
                data="https://storage.example.com/signed-payload?token=abc123",
                id="wr_xyz",
                object="signed_data_url",
                metadata={"env": "production"},
            ),
        )

    def test_fetches_and_returns_full_event(self):
        """Should fetch and return the full event (sync)."""
        full_payload = {
            "id": "wr_xyz",
            "object": "workflow_run",
            "status": "PROCESSED",
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = full_payload

        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client

            result = self.webhooks.fetch_signed_payload_sync(self.signed_event)

            mock_client.get.assert_called_once_with(self.signed_event.payload.data)
            assert result["eventId"] == "evt_789"
            assert result["payload"] == full_payload


class TestErrorClasses:
    """Tests for error classes."""

    def test_webhook_signature_verification_error(self):
        """WebhookSignatureVerificationError should have correct attributes."""
        error = WebhookSignatureVerificationError("test message")
        assert str(error) == "test message"
        assert isinstance(error, Exception)

    def test_signed_url_not_allowed_error(self):
        """SignedUrlNotAllowedError should have correct message."""
        error = SignedUrlNotAllowedError()
        assert "allow_signed_url" in str(error)
        assert isinstance(error, Exception)

    def test_webhook_payload_fetch_error(self):
        """WebhookPayloadFetchError should have correct attributes."""
        error = WebhookPayloadFetchError("fetch failed")
        assert str(error) == "fetch failed"
        assert isinstance(error, Exception)
