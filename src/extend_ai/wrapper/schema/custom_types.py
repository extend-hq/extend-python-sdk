"""
Custom pydantic field types for Extend-specific extraction fields.

These map to the `extend:type` custom field types in Extend's JSON Schema
format (see https://docs.extend.ai/2026-02-09/extraction/schema). Use them as
field annotations in the pydantic model you pass as an extraction schema.

Example:
    import datetime
    from typing import Optional
    from pydantic import BaseModel, Field
    from extend_ai import ExtendCurrency, ExtendDate, ExtendSignature

    class Invoice(BaseModel):
        invoice_number: Optional[str] = Field(None, description="The invoice number")
        invoice_date: ExtendDate = Field(None, description="The invoice date")
        total: Optional[ExtendCurrency] = Field(None, description="Total amount due")
        signature: Optional[ExtendSignature] = None
"""

import datetime as dt
import typing

import pydantic

__all__ = ["ExtendCurrency", "ExtendDate", "ExtendSignature"]


# Fields annotated with `ExtendDate` (or plain `datetime.date`) convert to:
#
#     {"type": ["string", "null"], "extend:type": "date"}
#
# The API returns an ISO date string (yyyy-mm-dd) or null; pydantic parses it
# back into a `datetime.date` when the output is validated.
ExtendDate = typing.Optional[dt.date]


class ExtendCurrency(pydantic.BaseModel):
    """
    Currency field type.

    Converts to Extend's currency schema:

        {
            "type": "object",
            "extend:type": "currency",
            "properties": {
                "amount": {"type": ["number", "null"]},
                "iso_4217_currency_code": {"type": ["string", "null"]}
            },
            "required": ["amount", "iso_4217_currency_code"]
        }
    """

    __extend_type__: typing.ClassVar[str] = "currency"

    amount: typing.Optional[float] = None
    iso_4217_currency_code: typing.Optional[str] = None


class ExtendSignature(pydantic.BaseModel):
    """
    Signature field type.

    Converts to Extend's signature schema, which enables advanced signature
    detection during parsing and post-processing heuristics that reduce false
    positives on unsigned signature blocks:

        {
            "type": "object",
            "extend:type": "signature",
            "properties": {
                "printed_name": {"type": ["string", "null"]},
                "signature_date": {"type": ["string", "null"], "extend:type": "date"},
                "is_signed": {"type": ["boolean", "null"]},
                "title_or_role": {"type": ["string", "null"]}
            },
            "required": ["printed_name", "signature_date", "is_signed", "title_or_role"]
        }
    """

    __extend_type__: typing.ClassVar[str] = "signature"

    printed_name: typing.Optional[str] = None
    signature_date: typing.Optional[dt.date] = None
    is_signed: typing.Optional[bool] = None
    title_or_role: typing.Optional[str] = None


def get_extend_type(model: type) -> typing.Optional[str]:
    """Return the extend:type marker for a model class, if it has one."""
    return getattr(model, "__extend_type__", None)
