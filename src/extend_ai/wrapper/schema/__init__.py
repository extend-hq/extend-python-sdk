"""
Schema utilities for typed extraction with pydantic models.

Define your extraction schema as a pydantic model and pass it as
``config["schema"]`` to get end-to-end typing: the SDK converts the model to
Extend's JSON Schema format for the request, and validates the extraction
output back into model instances.

Example:
    from typing import List, Optional
    from pydantic import BaseModel, Field
    from extend_ai import Extend, ExtendCurrency, ExtendDate

    class LineItem(BaseModel):
        description: Optional[str] = None
        quantity: Optional[float] = None
        price: Optional[ExtendCurrency] = None

    class Invoice(BaseModel):
        invoice_number: Optional[str] = Field(None, description="The invoice number")
        invoice_date: ExtendDate = Field(None, description="The invoice date")
        line_items: List[LineItem] = Field(default_factory=list)
        total: Optional[ExtendCurrency] = Field(None, description="Total amount due")

    client = Extend(token="...")
    result = client.extract(
        file={"url": "https://example.com/invoice.pdf"},
        config={"schema": Invoice},
    )

    # output.value is a validated Invoice instance
    if result.output is not None:
        print(result.output.value.invoice_number)
        print(result.output.value.total.amount if result.output.value.total else None)
"""

from .config_conversion import (
    TypedExtractConfigParams,
    TypedExtractorParams,
    convert_typed_config,
    convert_typed_extractor,
    get_extractor_schema_model,
    get_schema_model,
)
from .conversion import SchemaConversionError, pydantic_to_extend_schema
from .custom_types import ExtendCurrency, ExtendDate, ExtendSignature
from .typed_run import ExtractOutputValidationError, TypedExtractOutput, TypedExtractRun, parse_extract_run

__all__ = [
    # Custom field types
    "ExtendCurrency",
    "ExtendDate",
    "ExtendSignature",
    # Conversion
    "SchemaConversionError",
    "pydantic_to_extend_schema",
    # Errors
    "ExtractOutputValidationError",
    # Typed configs (for annotations / advanced usage)
    "TypedExtractConfigParams",
    "TypedExtractorParams",
    # Typed runs
    "TypedExtractOutput",
    "TypedExtractRun",
    "parse_extract_run",
    # Internal conversion helpers
    "convert_typed_config",
    "convert_typed_extractor",
    "get_extractor_schema_model",
    "get_schema_model",
]
