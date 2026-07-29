"""Tests for typed (pydantic schema) extraction across the wrapper clients."""

import datetime as dt
from typing import List, Optional
from unittest.mock import MagicMock

import pydantic
import pytest

from extend_ai.wrapper.schema import (
    ExtendCurrency,
    ExtendDate,
    ExtractOutputValidationError,
    TypedExtractOutput,
    TypedExtractRun,
    parse_extract_run,
)


class LineItem(pydantic.BaseModel):
    description: Optional[str] = None
    amount: Optional[ExtendCurrency] = None


class Invoice(pydantic.BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: ExtendDate = None
    total: Optional[ExtendCurrency] = None
    line_items: List[LineItem] = []


INVOICE_OUTPUT_VALUE = {
    "invoice_number": "INV-123",
    "invoice_date": "2026-01-15",
    "total": {"amount": 99.5, "iso_4217_currency_code": "USD"},
    "line_items": [
        {"description": "Widget", "amount": {"amount": 99.5, "iso_4217_currency_code": "USD"}},
    ],
}


def create_mock_run(status: str = "PROCESSED", value=None):
    """Create a mock extract run with a JSON-schema output."""
    run = MagicMock()
    run.id = "extract_run_test123"
    run.status = status
    run.object = "extract_run"
    if value is None:
        run.output = None
    else:
        run.output = MagicMock()
        run.output.value = value
    run.initial_output = None
    run.reviewed_output = None
    return run


# ============================================================================
# parse_extract_run
# ============================================================================


class TestParseExtractRun:
    def test_parses_output_value_into_model_instance(self):
        run = create_mock_run(value=INVOICE_OUTPUT_VALUE)

        typed = parse_extract_run(run, Invoice)

        assert isinstance(typed, TypedExtractRun)
        assert isinstance(typed.output, TypedExtractOutput)
        assert isinstance(typed.output.value, Invoice)
        assert typed.output.value.invoice_number == "INV-123"
        assert typed.output.value.invoice_date == dt.date(2026, 1, 15)
        assert isinstance(typed.output.value.total, ExtendCurrency)
        assert typed.output.value.total.amount == 99.5
        assert typed.output.value.line_items[0].description == "Widget"

    def test_copies_run_fields_and_keeps_raw(self):
        run = create_mock_run(value=INVOICE_OUTPUT_VALUE)

        typed = parse_extract_run(run, Invoice)

        assert typed.id == run.id
        assert typed.status == run.status
        assert typed.raw is run

    def test_handles_none_outputs(self):
        run = create_mock_run(status="FAILED", value=None)

        typed = parse_extract_run(run, Invoice)

        assert typed.output is None
        assert typed.initial_output is None
        assert typed.reviewed_output is None

    def test_null_field_values_validate_into_none(self):
        run = create_mock_run(
            value={"invoice_number": None, "invoice_date": None, "total": None, "line_items": []}
        )

        typed = parse_extract_run(run, Invoice)

        assert typed.output.value.invoice_number is None
        assert typed.output.value.total is None

    def test_raises_for_output_without_value(self):
        run = create_mock_run(value=INVOICE_OUTPUT_VALUE)
        run.output = MagicMock(spec=[])  # legacy output shape: no `value` attribute

        with pytest.raises(ExtractOutputValidationError) as exc_info:
            parse_extract_run(run, Invoice)
        assert exc_info.value.run is run

    def test_validation_failure_preserves_completed_run_on_error(self):
        run = create_mock_run(value={"invoice_number": "INV-1", "line_items": "not-a-list"})

        with pytest.raises(ExtractOutputValidationError) as exc_info:
            parse_extract_run(run, Invoice)

        error = exc_info.value
        assert error.run is run
        assert error.run.output.value["line_items"] == "not-a-list"
        assert "Invoice" in str(error)
        assert isinstance(error.__cause__, pydantic.ValidationError)


# ============================================================================
# ExtractRunsClient.create_and_poll with typed schemas
# ============================================================================


class TestCreateAndPollTypedSchema:
    def setup_method(self):
        from extend_ai.wrapper.resources.extract_runs import ExtractRunsClient

        self.wrapper = MagicMock(spec=ExtractRunsClient)
        self.wrapper.create = MagicMock()
        self.wrapper.retrieve = MagicMock()
        self.wrapper.create_and_poll = ExtractRunsClient.create_and_poll.__get__(self.wrapper, ExtractRunsClient)

    def test_converts_config_schema_and_returns_typed_run(self):
        self.wrapper.create.return_value = create_mock_run("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)

        result = self.wrapper.create_and_poll(
            file={"id": "file_1"},
            config={"schema": Invoice, "base_processor": "extraction_performance"},
        )

        create_kwargs = self.wrapper.create.call_args.kwargs
        sent_schema = create_kwargs["config"]["schema"]
        assert isinstance(sent_schema, dict)
        assert sent_schema["type"] == "object"
        assert sent_schema["properties"]["invoice_number"] == {"type": ["string", "null"]}
        # Other config keys pass through untouched
        assert create_kwargs["config"]["base_processor"] == "extraction_performance"

        assert isinstance(result, TypedExtractRun)
        assert isinstance(result.output.value, Invoice)
        assert result.output.value.invoice_number == "INV-123"

    def test_converts_extractor_override_config_schema(self):
        self.wrapper.create.return_value = create_mock_run("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)

        result = self.wrapper.create_and_poll(
            file={"id": "file_1"},
            extractor={"id": "extractor_abc", "override_config": {"schema": Invoice}},
        )

        create_kwargs = self.wrapper.create.call_args.kwargs
        sent_extractor = create_kwargs["extractor"]
        assert sent_extractor["id"] == "extractor_abc"
        assert isinstance(sent_extractor["override_config"]["schema"], dict)
        assert sent_extractor["override_config"]["schema"]["type"] == "object"

        assert isinstance(result, TypedExtractRun)

    def test_untyped_config_passes_through_and_returns_plain_run(self):
        self.wrapper.create.return_value = create_mock_run("PROCESSING")
        processed = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)
        self.wrapper.retrieve.return_value = processed

        json_config = {"schema": {"type": "object", "properties": {}}}
        result = self.wrapper.create_and_poll(file={"id": "file_1"}, config=json_config)

        assert self.wrapper.create.call_args.kwargs["config"] is json_config
        assert result is processed
        assert not isinstance(result, TypedExtractRun)

    def test_typed_failed_run_has_no_output(self):
        self.wrapper.create.return_value = create_mock_run("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_run("FAILED", value=None)

        result = self.wrapper.create_and_poll(file={"id": "file_1"}, config={"schema": Invoice})

        assert isinstance(result, TypedExtractRun)
        assert result.status == "FAILED"
        assert result.output is None


class TestAsyncCreateAndPollTypedSchema:
    def setup_method(self):
        from unittest.mock import AsyncMock

        from extend_ai.wrapper.resources.extract_runs import AsyncExtractRunsClient

        self.wrapper = MagicMock(spec=AsyncExtractRunsClient)
        self.wrapper.create = AsyncMock()
        self.wrapper.retrieve = AsyncMock()
        self.wrapper.create_and_poll = AsyncExtractRunsClient.create_and_poll.__get__(
            self.wrapper, AsyncExtractRunsClient
        )

    async def test_converts_config_schema_and_returns_typed_run(self):
        self.wrapper.create.return_value = create_mock_run("PROCESSING")
        self.wrapper.retrieve.return_value = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)

        result = await self.wrapper.create_and_poll(file={"id": "file_1"}, config={"schema": Invoice})

        sent_schema = self.wrapper.create.call_args.kwargs["config"]["schema"]
        assert isinstance(sent_schema, dict)
        assert isinstance(result, TypedExtractRun)
        assert result.output.value.invoice_number == "INV-123"


# ============================================================================
# ExtractRunsClient.create (plain, non-polling) with typed schemas
# ============================================================================


class TestPlainCreateTypedSchema:
    def setup_method(self):
        from extend_ai.wrapper.resources.extract_runs import ExtractRunsClient

        self.client = ExtractRunsClient(client_wrapper=MagicMock())
        self.raw_client = MagicMock()
        self.client._raw_client = self.raw_client

    def test_create_converts_model_schema(self):
        self.client.create(file={"id": "file_1"}, config={"schema": Invoice})

        sent_config = self.raw_client.create.call_args.kwargs["config"]
        assert isinstance(sent_config["schema"], dict)
        assert sent_config["schema"]["type"] == "object"

    def test_create_converts_extractor_override_config_schema(self):
        self.client.create(
            file={"id": "file_1"},
            extractor={"id": "extractor_abc", "override_config": {"schema": Invoice}},
        )

        sent_extractor = self.raw_client.create.call_args.kwargs["extractor"]
        assert isinstance(sent_extractor["override_config"]["schema"], dict)

    def test_create_passes_through_json_schema(self):
        json_config = {"schema": {"type": "object", "properties": {}}}
        self.client.create(file={"id": "file_1"}, config=json_config)

        assert self.raw_client.create.call_args.kwargs["config"] is json_config


# ============================================================================
# Extend.extract with typed schemas
# ============================================================================


class TestClientExtractTypedSchema:
    def setup_method(self):
        from extend_ai.wrapper.client import Extend

        self.client = Extend(token="test-token")
        self.raw_client = MagicMock()
        self.client._raw_client = self.raw_client

    def test_converts_config_schema_and_returns_typed_run(self):
        response = MagicMock()
        response.data = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)
        self.raw_client.extract.return_value = response

        result = self.client.extract(
            file={"url": "https://example.com/invoice.pdf"},
            config={"schema": Invoice},
        )

        sent_config = self.raw_client.extract.call_args.kwargs["config"]
        assert isinstance(sent_config["schema"], dict)
        assert sent_config["schema"]["type"] == "object"

        assert isinstance(result, TypedExtractRun)
        assert isinstance(result.output.value, Invoice)

    def test_untyped_extract_returns_plain_run(self):
        response = MagicMock()
        run = create_mock_run("PROCESSED", value=INVOICE_OUTPUT_VALUE)
        response.data = run
        self.raw_client.extract.return_value = response

        result = self.client.extract(file={"url": "https://example.com/invoice.pdf"})

        assert result is run


# ============================================================================
# Extractors / ExtractorVersions with typed schemas
# ============================================================================


class TestExtractorsTypedSchema:
    def setup_method(self):
        from extend_ai.wrapper.resources.extractors import ExtractorsClient

        self.client = ExtractorsClient(client_wrapper=MagicMock())
        self.raw_client = MagicMock()
        self.client._raw_client = self.raw_client

    def test_create_converts_model_schema(self):
        self.client.create(name="Invoice Extractor", config={"schema": Invoice})

        sent_config = self.raw_client.create.call_args.kwargs["config"]
        assert isinstance(sent_config["schema"], dict)
        assert sent_config["schema"]["type"] == "object"

    def test_create_passes_through_json_schema(self):
        json_config = {"schema": {"type": "object", "properties": {}}}
        self.client.create(name="Invoice Extractor", config=json_config)

        assert self.raw_client.create.call_args.kwargs["config"] is json_config

    def test_update_converts_model_schema(self):
        self.client.update("extractor_abc", config={"schema": Invoice})

        sent_config = self.raw_client.update.call_args.kwargs["config"]
        assert isinstance(sent_config["schema"], dict)

    def test_create_without_config_passes_omit(self):
        self.client.create(name="Invoice Extractor")

        sent_config = self.raw_client.create.call_args.kwargs["config"]
        assert sent_config is ...


class TestExtractorVersionsTypedSchema:
    def setup_method(self):
        from extend_ai.wrapper.resources.extractor_versions import ExtractorVersionsClient

        self.client = ExtractorVersionsClient(client_wrapper=MagicMock())
        self.raw_client = MagicMock()
        self.client._raw_client = self.raw_client

    def test_create_converts_model_schema(self):
        self.client.create("extractor_abc", release_type="minor", config={"schema": Invoice})

        sent_config = self.raw_client.create.call_args.kwargs["config"]
        assert isinstance(sent_config["schema"], dict)
        assert sent_config["schema"]["properties"]["invoice_number"] == {"type": ["string", "null"]}
