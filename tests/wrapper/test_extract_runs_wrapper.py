"""Tests for ExtractRunsClient."""

from unittest.mock import MagicMock

import pytest

from extend_ai.wrapper.polling import PollingOptions, PollingTimeoutError


# ============================================================================
# Mock Response Factories
# ============================================================================


def create_mock_create_response(status: str = "PROCESSING"):
    """Create a mock create response."""
    response = MagicMock()
    response.id = "extract_run_test123"
    response.status = status
    response.object = "extract_run"
    return response


def create_mock_retrieve_response(status: str = "PROCESSED"):
    """Create a mock retrieve response."""
    response = MagicMock()
    response.id = "extract_run_test123"
    response.status = status
    response.object = "extract_run"
    return response


# ============================================================================
# Tests
# ============================================================================


class TestExtractRunsClientCreateAndPoll:
    """Tests for ExtractRunsClient.create_and_poll method."""

    def setup_method(self):
        """Set up test fixtures."""
        # Import here to avoid import errors if SDK structure changes
        from extend_ai.wrapper.resources.extract_runs import ExtractRunsClient

        # Create a wrapper with mocked methods
        self.wrapper = MagicMock(spec=ExtractRunsClient)
        self.wrapper.create = MagicMock()
        self.wrapper.retrieve = MagicMock()

        # Bind the actual create_and_poll method
        self.wrapper.create_and_poll = ExtractRunsClient.create_and_poll.__get__(
            self.wrapper, ExtractRunsClient
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
            extractor=MagicMock(),
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
            extractor=MagicMock(),
        )

        assert result.status == "PROCESSED"
        assert self.wrapper.retrieve.call_count == 1

    def test_handles_failed_status_as_terminal(self):
        """Should handle FAILED status as terminal."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("FAILED")

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            extractor=MagicMock(),
        )

        assert result.status == "FAILED"

    def test_handles_cancelled_status_as_terminal(self):
        """Should handle CANCELLED status as terminal."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("CANCELLED")

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            extractor=MagicMock(),
        )

        assert result.status == "CANCELLED"

    def test_throws_polling_timeout_error(self):
        """Should throw PollingTimeoutError when timeout exceeded."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("PROCESSING")

        with pytest.raises(PollingTimeoutError):
            self.wrapper.create_and_poll(
                file=MagicMock(),
                extractor=MagicMock(),
                polling_options=PollingOptions(
                    max_wait_ms=50,
                    initial_delay_ms=10,
                    jitter_fraction=0,
                ),
            )

    def test_continues_polling_during_pending(self):
        """Should continue polling during PENDING status."""
        self.wrapper.create.return_value = create_mock_create_response("PENDING")
        self.wrapper.retrieve.side_effect = [
            create_mock_retrieve_response("PENDING"),
            create_mock_retrieve_response("PROCESSING"),
            create_mock_retrieve_response("PROCESSED"),
        ]

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            extractor=MagicMock(),
            polling_options=PollingOptions(
                initial_delay_ms=1,
                max_wait_ms=10000,
                jitter_fraction=0,
            ),
        )

        assert result.status == "PROCESSED"
        assert self.wrapper.retrieve.call_count == 3

    def test_supports_package_for_multifile_extraction(self):
        """Should accept package instead of file and pass it through to create."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("PROCESSED")

        package = {"files": [{"id": "file_1"}, {"id": "file_2"}]}
        result = self.wrapper.create_and_poll(
            package=package,
            extractor=MagicMock(),
        )

        assert result.status == "PROCESSED"
        create_kwargs = self.wrapper.create.call_args.kwargs
        assert create_kwargs["package"] == package
        assert "file" not in create_kwargs

    def test_passes_file_through_to_create(self):
        """Should pass file through to create and omit package when not given."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_retrieve_response("PROCESSED")

        file = {"id": "file_1"}
        self.wrapper.create_and_poll(file=file, extractor=MagicMock())

        create_kwargs = self.wrapper.create.call_args.kwargs
        assert create_kwargs["file"] == file
        assert "package" not in create_kwargs

    def test_continues_polling_during_cancelling(self):
        """Should continue polling during CANCELLING status."""
        self.wrapper.create.return_value = create_mock_create_response("PROCESSING")
        self.wrapper.retrieve.side_effect = [
            create_mock_retrieve_response("CANCELLING"),
            create_mock_retrieve_response("CANCELLED"),
        ]

        result = self.wrapper.create_and_poll(
            file=MagicMock(),
            extractor=MagicMock(),
            polling_options=PollingOptions(
                initial_delay_ms=1,
                max_wait_ms=10000,
                jitter_fraction=0,
            ),
        )

        assert result.status == "CANCELLED"
        assert self.wrapper.retrieve.call_count == 2
