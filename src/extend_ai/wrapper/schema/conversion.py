"""
Converts pydantic models to Extend's JSON Schema format.

The converter is strict: mistakes that would otherwise surface as a 400 from
the API, or worse as a validation failure after a completed extraction run,
are raised as SchemaConversionError before any request is sent. In
particular, fields whose emitted schema is nullable (primitives, enums,
dates) must be declared Optional, because extraction can return null for any
field and the output is validated back into the model.

Structural limits (nesting depth, property counts, property key format) are
validated server-side.
"""

import datetime as dt
import enum
import types
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from .custom_types import get_extend_type

__all__ = ["SchemaConversionError", "pydantic_to_extend_schema"]

_NoneType = type(None)

# typing.Literal and typing_extensions.Literal are distinct objects on some
# Python versions (e.g. 3.8), so origins must be checked against both.
_LITERAL_ORIGINS = {typing_extensions.Literal, getattr(typing, "Literal", typing_extensions.Literal)}


class SchemaConversionError(Exception):
    """Raised when a pydantic model cannot be converted to Extend JSON Schema."""

    def __init__(self, message: str, path: typing.Optional[typing.List[str]] = None):
        self.path: typing.List[str] = list(path or [])
        if self.path:
            message = f"{message} at path: {'.'.join(self.path)}"
        super().__init__(message)


def _iter_model_fields(
    model: typing.Type[pydantic.BaseModel],
) -> typing.Iterator[typing.Tuple[str, typing.Any, typing.Optional[str], typing.Any]]:
    """
    Yield (field_name, annotation, description, alias) for each field of a
    pydantic model, working under both pydantic v1 and v2.
    """
    # Raw class annotations (via get_type_hints) preserve Optional wrappers,
    # which pydantic v1's `outer_type_` strips.
    try:
        hints = typing_extensions.get_type_hints(model, include_extras=True)
    except Exception:
        hints = {}

    if IS_PYDANTIC_V2:
        for name, field in model.model_fields.items():  # type: ignore[attr-defined]
            alias = field.alias or getattr(field, "validation_alias", None)
            yield name, hints.get(name, field.annotation), field.description, alias
    else:
        for name, field in model.__fields__.items():  # type: ignore[attr-defined]
            info = field.field_info  # type: ignore[attr-defined]
            annotation = hints.get(name)
            if annotation is None:
                annotation = field.outer_type_  # type: ignore[attr-defined]
                if field.allow_none:  # type: ignore[attr-defined]
                    annotation = typing.Optional[annotation]
            yield name, annotation, getattr(info, "description", None), getattr(info, "alias", None)


def _is_union_origin(origin: typing.Any) -> bool:
    if origin is typing.Union:
        return True
    union_type = getattr(types, "UnionType", None)  # X | Y syntax on Python 3.10+
    return union_type is not None and origin is union_type


def _unwrap_annotation(annotation: typing.Any, path: typing.List[str]) -> typing.Any:
    """
    Strip Annotated metadata and Optional/None-unions from an annotation,
    returning the inner type. Unions of multiple non-None types are rejected.
    """
    while True:
        origin = typing_extensions.get_origin(annotation)
        if origin is typing_extensions.Annotated:
            annotation = typing_extensions.get_args(annotation)[0]
        elif _is_union_origin(origin):
            non_none = [arg for arg in typing_extensions.get_args(annotation) if arg is not _NoneType]
            if len(non_none) != 1:
                raise SchemaConversionError(
                    "Union types are not supported (only Optional[...] is allowed)", path
                )
            annotation = non_none[0]
        else:
            return annotation


def _accepts_none(annotation: typing.Any) -> bool:
    """Whether a value of None validates against the annotation."""
    origin = typing_extensions.get_origin(annotation)
    if origin is typing_extensions.Annotated:
        return _accepts_none(typing_extensions.get_args(annotation)[0])
    if _is_union_origin(origin):
        return any(arg is _NoneType or _accepts_none(arg) for arg in typing_extensions.get_args(annotation))
    if origin in _LITERAL_ORIGINS:
        return None in typing_extensions.get_args(annotation)
    return annotation is _NoneType


def _require_nullable(annotation: typing.Any, kind: str, path: typing.List[str]) -> None:
    """
    Fields whose emitted schema is nullable must accept None, otherwise
    extraction output containing null would fail model validation after the
    run has already completed.
    """
    if not _accepts_none(annotation):
        raise SchemaConversionError(
            f"Field must be Optional: extraction can return null for any field, "
            f"so declare it as Optional[{kind}]",
            path,
        )


def _with_description(schema: typing.Dict[str, typing.Any], description: typing.Optional[str]) -> typing.Dict[str, typing.Any]:
    if description:
        schema["description"] = description
    return schema


def _date_schema() -> typing.Dict[str, typing.Any]:
    return {"type": ["string", "null"], "extend:type": "date"}


def _currency_schema() -> typing.Dict[str, typing.Any]:
    return {
        "type": "object",
        "extend:type": "currency",
        "properties": {
            "amount": {"type": ["number", "null"]},
            "iso_4217_currency_code": {"type": ["string", "null"]},
        },
        "required": ["amount", "iso_4217_currency_code"],
        "additionalProperties": False,
    }


def _signature_schema() -> typing.Dict[str, typing.Any]:
    return {
        "type": "object",
        "extend:type": "signature",
        "properties": {
            "printed_name": {"type": ["string", "null"]},
            "signature_date": {"type": ["string", "null"], "extend:type": "date"},
            "is_signed": {"type": ["boolean", "null"]},
            "title_or_role": {"type": ["string", "null"]},
        },
        "required": ["printed_name", "signature_date", "is_signed", "title_or_role"],
        "additionalProperties": False,
    }


def _enum_values(annotation: typing.Any, path: typing.List[str]) -> typing.List[typing.Optional[str]]:
    """Extract string enum values from a Literal[...] or string Enum class."""
    if typing_extensions.get_origin(annotation) in _LITERAL_ORIGINS:
        raw_values: typing.List[typing.Any] = [v for v in typing_extensions.get_args(annotation) if v is not None]
    else:  # enum.Enum subclass
        raw_values = [member.value for member in annotation]

    values: typing.List[typing.Optional[str]] = []
    for value in raw_values:
        if not isinstance(value, str):
            raise SchemaConversionError(
                f"Enums must only contain strings, got {type(value).__name__}: {value!r}", path
            )
        values.append(value)
    values.append(None)
    return values


def _is_enum_annotation(annotation: typing.Any) -> bool:
    if typing_extensions.get_origin(annotation) in _LITERAL_ORIGINS:
        return True
    return isinstance(annotation, type) and issubclass(annotation, enum.Enum)


def pydantic_to_extend_schema(model: typing.Type[pydantic.BaseModel]) -> typing.Dict[str, typing.Any]:
    """
    Convert a pydantic model class to Extend's JSON Schema format.

    Every property is listed as required, and field descriptions come from
    ``Field(description=...)``. Primitive, enum, and date fields must be
    declared ``Optional`` — extraction can return ``null`` for any field, and
    the emitted schema marks them nullable per Extend's schema requirements.

    Args:
        model: A ``pydantic.BaseModel`` subclass describing the data to extract.

    Returns:
        The Extend JSON Schema as a plain dict.

    Raises:
        SchemaConversionError: If the model uses unsupported types, recursive
            references, field aliases, or non-Optional nullable fields.
    """
    if not (isinstance(model, type) and issubclass(model, pydantic.BaseModel)):
        raise SchemaConversionError(f"Schema must be a pydantic BaseModel subclass, got {model!r}")
    return _convert_object(model, [], frozenset())


def _convert_object(
    model: typing.Type[pydantic.BaseModel],
    path: typing.List[str],
    seen: typing.FrozenSet[type],
) -> typing.Dict[str, typing.Any]:
    # Extend's schema format cannot express recursion, and recursive models
    # would otherwise overflow the stack (fatally on some Python versions).
    if model in seen:
        raise SchemaConversionError(
            f"Recursive model references are not supported: {model.__name__} refers back to itself",
            path,
        )
    seen = seen | {model}

    properties: typing.Dict[str, typing.Any] = {}
    required: typing.List[str] = []

    for name, annotation, description, alias in _iter_model_fields(model):
        if alias:
            raise SchemaConversionError(
                f"Field aliases are not supported for extraction schemas "
                f"(field {name!r} has alias {alias!r}): the extraction output uses field names, "
                f"so aliased fields would silently validate to None. Remove the alias.",
                path + [name],
            )
        properties[name] = _convert_annotation(annotation, description, path + [name], seen)
        required.append(name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def _convert_annotation(
    annotation: typing.Any,
    description: typing.Optional[str],
    path: typing.List[str],
    seen: typing.FrozenSet[type],
) -> typing.Dict[str, typing.Any]:
    inner = _unwrap_annotation(annotation, path)

    if typing_extensions.get_origin(inner) is list or inner is list:
        args = typing_extensions.get_args(inner)
        if not args:
            raise SchemaConversionError("Arrays must declare an item type (use List[...])", path)
        return _with_description({"type": "array", "items": _convert_array_item(args[0], path, seen)}, description)

    if _is_enum_annotation(inner):
        kind = inner.__name__ if isinstance(inner, type) else "Literal[...]"
        _require_nullable(annotation, kind, path)
        return _with_description({"enum": _enum_values(inner, path)}, description)

    if isinstance(inner, type):
        if issubclass(inner, pydantic.BaseModel):
            extend_type = get_extend_type(inner)
            if extend_type == "currency":
                return _with_description(_currency_schema(), description)
            if extend_type == "signature":
                return _with_description(_signature_schema(), description)
            return _with_description(_convert_object(inner, path, seen), description)
        if issubclass(inner, bool):
            _require_nullable(annotation, "bool", path)
            return _with_description({"type": ["boolean", "null"]}, description)
        if issubclass(inner, int):
            _require_nullable(annotation, "int", path)
            return _with_description({"type": ["integer", "null"]}, description)
        if issubclass(inner, float):
            _require_nullable(annotation, "float", path)
            return _with_description({"type": ["number", "null"]}, description)
        if issubclass(inner, dt.datetime):
            raise SchemaConversionError(
                "datetime.datetime is not supported; use datetime.date (or ExtendDate) for date fields", path
            )
        if issubclass(inner, dt.date):
            _require_nullable(annotation, "datetime.date", path)
            return _with_description(_date_schema(), description)
        if issubclass(inner, str):
            _require_nullable(annotation, "str", path)
            return _with_description({"type": ["string", "null"]}, description)

    raise SchemaConversionError(f"Unsupported type: {inner!r}", path)


def _convert_array_item(
    annotation: typing.Any,
    path: typing.List[str],
    seen: typing.FrozenSet[type],
) -> typing.Dict[str, typing.Any]:
    """
    Convert array item types, which have different rules than top-level types:
    items can be objects or primitives, and primitive items are NOT nullable.
    """
    inner = _unwrap_annotation(annotation, path)

    # Array items are never null in extraction output, so an Optional item
    # annotation would misleadingly suggest otherwise.
    if _accepts_none(annotation) and not (isinstance(inner, type) and issubclass(inner, pydantic.BaseModel)):
        raise SchemaConversionError(
            "Array items must not be Optional: extraction never returns null array items "
            "(use e.g. List[str] instead of List[Optional[str]])",
            path,
        )

    if _is_enum_annotation(inner):
        raise SchemaConversionError(
            "Enums are not supported as array items. "
            "Array items must be objects or primitives (string, number, integer, boolean).",
            path,
        )

    if isinstance(inner, type) and issubclass(inner, pydantic.BaseModel):
        extend_type = get_extend_type(inner)
        if extend_type == "currency":
            return _currency_schema()
        if extend_type == "signature":
            return _signature_schema()
        return _convert_object(inner, path, seen)

    if isinstance(inner, type):
        if issubclass(inner, bool):
            return {"type": "boolean"}
        if issubclass(inner, int):
            return {"type": "integer"}
        if issubclass(inner, float):
            return {"type": "number"}
        if issubclass(inner, dt.datetime):
            raise SchemaConversionError(
                "datetime.datetime is not supported; use datetime.date (or ExtendDate) for date fields", path
            )
        if issubclass(inner, dt.date):
            return {"type": "string", "extend:type": "date"}
        if issubclass(inner, str):
            return {"type": "string"}

    raise SchemaConversionError(
        f"Unsupported array item type: {inner!r}. "
        "Array items must be objects or primitives (string, number, integer, boolean).",
        path,
    )
