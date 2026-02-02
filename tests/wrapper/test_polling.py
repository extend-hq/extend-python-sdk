"""Tests for polling utilities."""

import time
from unittest.mock import MagicMock, patch

import pytest

from extend_ai.wrapper.polling import (
    calculate_backoff_delay,
    poll_until_done,
    poll_until_done_async,
    PollingOptions,
    PollingTimeoutError,
)


# ============================================================================
# calculate_backoff_delay tests
# ============================================================================


class TestCalculateBackoffDelay:
    """Tests for calculate_backoff_delay function."""

    def test_returns_initial_delay_for_attempt_zero(self):
        """Should return initialDelayMs for attempt 0."""
        with patch("random.random", return_value=0.5):  # Neutral jitter
            delay = calculate_backoff_delay(0, 1000, 30000, 0.25)
        assert delay == 1000

    def test_doubles_delay_for_each_attempt(self):
        """Should double delay for each attempt."""
        with patch("random.random", return_value=0.5):  # Neutral jitter
            assert calculate_backoff_delay(0, 1000, 30000, 0.25) == 1000
            assert calculate_backoff_delay(1, 1000, 30000, 0.25) == 2000
            assert calculate_backoff_delay(2, 1000, 30000, 0.25) == 4000
            assert calculate_backoff_delay(3, 1000, 30000, 0.25) == 8000
            assert calculate_backoff_delay(4, 1000, 30000, 0.25) == 16000

    def test_caps_delay_at_max(self):
        """Should cap delay at maxDelayMs."""
        with patch("random.random", return_value=0.5):
            delay = calculate_backoff_delay(10, 1000, 30000, 0.25)
        # 2^10 * 1000 = 1024000, but capped at 30000
        assert delay == 30000

    def test_respects_different_initial_delays(self):
        """Should respect different initialDelayMs."""
        with patch("random.random", return_value=0.5):
            assert calculate_backoff_delay(0, 500, 30000, 0.25) == 500
            assert calculate_backoff_delay(1, 500, 30000, 0.25) == 1000
            assert calculate_backoff_delay(2, 500, 30000, 0.25) == 2000

    def test_applies_positive_jitter(self):
        """Should apply positive jitter when random > 0.5."""
        with patch("random.random", return_value=1.0):  # Maximum positive jitter
            delay = calculate_backoff_delay(0, 1000, 30000, 0.25)
        # jitter = (1.0 * 2 - 1) * 0.25 = 0.25
        # delay = 1000 * (1 + 0.25) = 1250
        assert delay == 1250

    def test_applies_negative_jitter(self):
        """Should apply negative jitter when random < 0.5."""
        with patch("random.random", return_value=0.0):  # Maximum negative jitter
            delay = calculate_backoff_delay(0, 1000, 30000, 0.25)
        # jitter = (0.0 * 2 - 1) * 0.25 = -0.25
        # delay = 1000 * (1 - 0.25) = 750
        assert delay == 750

    def test_no_jitter_when_random_is_half(self):
        """Should apply no jitter when random = 0.5."""
        with patch("random.random", return_value=0.5):
            delay = calculate_backoff_delay(0, 1000, 30000, 0.25)
        assert delay == 1000

    def test_handles_zero_jitter_fraction(self):
        """Should handle zero jitter fraction."""
        with patch("random.random", return_value=1.0):
            delay = calculate_backoff_delay(0, 1000, 30000, 0)
        assert delay == 1000  # No jitter applied

    def test_handles_larger_jitter_fractions(self):
        """Should handle larger jitter fractions."""
        with patch("random.random", return_value=1.0):
            delay = calculate_backoff_delay(0, 1000, 30000, 0.5)
        # jitter = 0.5, delay = 1000 * 1.5 = 1500
        assert delay == 1500

    def test_returns_integer(self):
        """Should return rounded integer."""
        with patch("random.random", return_value=0.75):
            delay = calculate_backoff_delay(0, 1000, 30000, 0.25)
        assert isinstance(delay, int)

    def test_handles_small_initial_delays(self):
        """Should handle very small initial delays."""
        with patch("random.random", return_value=0.5):
            delay = calculate_backoff_delay(0, 10, 30000, 0.25)
        assert delay == 10

    def test_handles_max_smaller_than_initial(self):
        """Should handle maxDelay smaller than initial delay."""
        with patch("random.random", return_value=0.5):
            delay = calculate_backoff_delay(0, 1000, 500, 0.25)
        assert delay == 500


# ============================================================================
# poll_until_done tests
# ============================================================================


class TestPollUntilDone:
    """Tests for poll_until_done function."""

    def test_returns_immediately_when_terminal_on_first_call(self):
        """Should return immediately when isTerminal returns True on first call."""
        retrieve = MagicMock(return_value={"status": "DONE", "value": 42})
        is_terminal = MagicMock(return_value=True)

        result = poll_until_done(retrieve, is_terminal)

        assert result == {"status": "DONE", "value": 42}
        assert retrieve.call_count == 1
        assert is_terminal.call_count == 1

    def test_polls_until_terminal(self):
        """Should poll until isTerminal returns True."""
        call_count = {"value": 0}

        def retrieve():
            call_count["value"] += 1
            return {"status": "DONE" if call_count["value"] >= 3 else "PROCESSING"}

        def is_terminal(result):
            return result["status"] == "DONE"

        options = PollingOptions(
            initial_delay_ms=1,  # Very short delays for testing
            max_wait_ms=10000,
            jitter_fraction=0,
        )

        result = poll_until_done(retrieve, is_terminal, options)

        assert call_count["value"] == 3
        assert result["status"] == "DONE"

    def test_passes_result_to_is_terminal(self):
        """Should pass result to isTerminal function."""
        test_result = {"status": "DONE", "data": {"foo": "bar"}}
        retrieve = MagicMock(return_value=test_result)
        is_terminal = MagicMock(return_value=True)

        poll_until_done(retrieve, is_terminal)

        is_terminal.assert_called_with(test_result)

    def test_throws_timeout_error_when_exceeded(self):
        """Should throw PollingTimeoutError when maxWaitMs is set and exceeded."""
        retrieve = MagicMock(return_value={"status": "PROCESSING"})
        is_terminal = MagicMock(return_value=False)

        options = PollingOptions(
            max_wait_ms=50,
            initial_delay_ms=10,
            jitter_fraction=0,
        )

        with pytest.raises(PollingTimeoutError):
            poll_until_done(retrieve, is_terminal, options)

    def test_timeout_error_includes_elapsed_time(self):
        """Should include elapsed time in timeout error."""
        retrieve = MagicMock(return_value={"status": "PROCESSING"})
        is_terminal = MagicMock(return_value=False)

        options = PollingOptions(
            max_wait_ms=50,
            initial_delay_ms=10,
            jitter_fraction=0,
        )

        with pytest.raises(PollingTimeoutError) as exc_info:
            poll_until_done(retrieve, is_terminal, options)

        error = exc_info.value
        assert error.max_wait_ms == 50
        assert error.elapsed_ms >= 50

    def test_propagates_retrieve_errors(self):
        """Should propagate errors from retrieve function."""
        retrieve = MagicMock(side_effect=Exception("API Error"))
        is_terminal = MagicMock()

        with pytest.raises(Exception) as exc_info:
            poll_until_done(retrieve, is_terminal)

        assert "API Error" in str(exc_info.value)
        assert is_terminal.call_count == 0

    def test_propagates_is_terminal_errors(self):
        """Should propagate errors from isTerminal function."""
        retrieve = MagicMock(return_value={"status": "DONE"})
        is_terminal = MagicMock(side_effect=Exception("isTerminal Error"))

        with pytest.raises(Exception) as exc_info:
            poll_until_done(retrieve, is_terminal)

        assert "isTerminal Error" in str(exc_info.value)


# ============================================================================
# poll_until_done_async tests
# ============================================================================


class TestPollUntilDoneAsync:
    """Tests for poll_until_done_async function."""

    @pytest.mark.asyncio
    async def test_returns_immediately_when_terminal_on_first_call(self):
        """Should return immediately when isTerminal returns True on first call."""
        async def retrieve():
            return {"status": "DONE", "value": 42}

        is_terminal = MagicMock(return_value=True)

        result = await poll_until_done_async(retrieve, is_terminal)

        assert result == {"status": "DONE", "value": 42}
        assert is_terminal.call_count == 1

    @pytest.mark.asyncio
    async def test_polls_until_terminal(self):
        """Should poll until isTerminal returns True."""
        call_count = {"value": 0}

        async def retrieve():
            call_count["value"] += 1
            return {"status": "DONE" if call_count["value"] >= 3 else "PROCESSING"}

        def is_terminal(result):
            return result["status"] == "DONE"

        options = PollingOptions(
            initial_delay_ms=1,
            max_wait_ms=10000,
            jitter_fraction=0,
        )

        result = await poll_until_done_async(retrieve, is_terminal, options)

        assert call_count["value"] == 3
        assert result["status"] == "DONE"

    @pytest.mark.asyncio
    async def test_throws_timeout_error_when_exceeded(self):
        """Should throw PollingTimeoutError when maxWaitMs is exceeded."""
        async def retrieve():
            return {"status": "PROCESSING"}

        is_terminal = MagicMock(return_value=False)

        options = PollingOptions(
            max_wait_ms=50,
            initial_delay_ms=10,
            jitter_fraction=0,
        )

        with pytest.raises(PollingTimeoutError):
            await poll_until_done_async(retrieve, is_terminal, options)

    @pytest.mark.asyncio
    async def test_propagates_retrieve_errors(self):
        """Should propagate errors from retrieve function."""
        async def retrieve():
            raise Exception("API Error")

        is_terminal = MagicMock()

        with pytest.raises(Exception) as exc_info:
            await poll_until_done_async(retrieve, is_terminal)

        assert "API Error" in str(exc_info.value)


# ============================================================================
# PollingTimeoutError tests
# ============================================================================


class TestPollingTimeoutError:
    """Tests for PollingTimeoutError class."""

    def test_has_correct_message(self):
        """Should have correct message."""
        error = PollingTimeoutError("Polling timed out", 1000, 5000)
        assert str(error) == "Polling timed out"

    def test_exposes_elapsed_ms(self):
        """Should expose elapsedMs property."""
        error = PollingTimeoutError("test", 1234, 5000)
        assert error.elapsed_ms == 1234

    def test_exposes_max_wait_ms(self):
        """Should expose maxWaitMs property."""
        error = PollingTimeoutError("test", 1234, 5000)
        assert error.max_wait_ms == 5000

    def test_is_instance_of_exception(self):
        """Should be an instance of Exception."""
        error = PollingTimeoutError("test", 1000, 5000)
        assert isinstance(error, Exception)


# ============================================================================
# PollingOptions tests
# ============================================================================


class TestPollingOptions:
    """Tests for PollingOptions dataclass."""

    def test_default_values(self):
        """Should have sensible defaults matching TypeScript SDK."""
        options = PollingOptions()
        assert options.max_wait_ms == 300_000  # 5 minutes
        assert options.initial_delay_ms == 1_000  # 1 second
        assert options.max_delay_ms == 30_000  # 30 seconds
        assert options.jitter_fraction == 0.25

    def test_custom_values(self):
        """Should accept custom values."""
        options = PollingOptions(
            max_wait_ms=60_000,
            initial_delay_ms=500,
            max_delay_ms=10_000,
            jitter_fraction=0.1,
        )
        assert options.max_wait_ms == 60_000
        assert options.initial_delay_ms == 500
        assert options.max_delay_ms == 10_000
        assert options.jitter_fraction == 0.1


class TestInfinitePolling:
    """Tests for infinite polling behavior."""

    def test_polls_indefinitely_when_no_timeout(self):
        """Should poll indefinitely when max_wait_ms is not set."""
        call_count = {"value": 0}

        def retrieve():
            call_count["value"] += 1
            return {"done": call_count["value"] >= 3}

        def is_terminal(result):
            return result["done"]

        # No max_wait_ms - should complete without timeout
        options = PollingOptions(
            initial_delay_ms=1,
            jitter_fraction=0,
        )

        result = poll_until_done(retrieve, is_terminal, options)

        assert call_count["value"] == 3
        assert result["done"] is True
