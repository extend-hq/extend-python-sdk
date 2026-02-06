"""Tests for ClassifyRunsWrapper."""

from unittest.mock import MagicMock

import pytest

from extend_ai.wrapper.polling import PollingOptions, PollingTimeoutError


# ============================================================================
# Mock Response Factories
# ============================================================================


def create_mock_create_response(status: str = "PROCESSING"):
    """Create a mock create response."""
    response = MagicMock()
    response.id = "classify_run_test123"
    response.status = status
    response.object = "classify_run"
    return response


def create_mock_retrieve_response(status: str = "PROCESSED"):
    """Create a mock retrieve response."""
    response = MagicMock()
    response.id = "classify_run_test123"
    response.status = status
    response.object = "classify_run"
    return response


# ============================================================================
# Tests
# ============================================================================


class TestClassifyRunsWrapperCreateAndPoll:
    """Tests for ClassifyRunsWrapper.create_and_poll method."""

    def setup_method(self):
        """Set up test fixtures."""
        from extend_ai.wrapper.resources.classify_runs import ClassifyRunsWrapper

        self.wrapper = MagicMock(spec=ClassifyRunsWrapper)
        self.wrapper.create = MagicMock()
        self.wrapper.retrieve = MagicMock()

        self.wrapper.create_and_poll = ClassifyRunsWrapper.create_and_poll.__get__(
            self.wrapper, ClassifyRunsWrapper
        )

    def test_creates_and_polls_until_processed(self):
        """Should create and poll until processed."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.side_effect = [
            create_mock_retrieve_response("PROCESSING"),
            create_mock_retrieve_response("PROCESSED"),
        ]

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            classifier=MagicMock(),
            polling_options=PollingOptions(
                initial_delay_ms=1,
                max_wait_ms=10000,
                jitter_fraction=0,
            ),
        )

        assert self.wrapper.create.call_count == 1
        assert self.wrapper.retrieve.call_count == 2
        assert result.status == "PROCESSED"

    def test_returns_immediately_if_processed_on_first_retrieve(self):
        """Should return immediately if already processed on first retrieve."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("PROCESSED")

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            classifier=MagicMock(),
        )

        assert result.status == "PROCESSED"
        assert self.wrapper.retrieve.call_count == 1

    def test_handles_failed_status_as_terminal(self):
        """Should handle FAILED status as terminal."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("FAILED")

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            classifier=MagicMock(),
        )

        assert result.status == "FAILED"

    def test_handles_cancelled_status_as_terminal(self):
        """Should handle CANCELLED status as terminal."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("CANCELLED")

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            classifier=MagicMock(),
        )

        assert result.status == "CANCELLED"

    def test_throws_polling_timeout_error(self):
        """Should throw PollingTimeoutError when timeout exceeded."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("PROCESSING")

        with pytest.raises(PollingTimeoutError):
            self.wrapper.create_and_poll(
                file=MagicMock(),
                classifier=MagicMock(),
                polling_options=PollingOptions(
                    max_wait_ms=50,
                    initial_delay_ms=10,
                    jitter_fraction=0,
                ),
            )
