"""
Detection and conversion of typed (pydantic) extract configs to API format.

Used by ``Extend.extract()``, ``ExtractRunsClient.create_and_poll()``,
``ExtractorsClient.create()/update()``, and ``ExtractorVersionsClient.create()``.
"""

import typing

import pydantic
import typing_extensions
from ...requests.extract_advanced_options import ExtractAdvancedOptionsParams
from ...requests.parse_config import ParseConfigParams
from ...types.extract_base_processor import ExtractBaseProcessor
from ...types.processor_version_string import ProcessorVersionString
from .conversion import pydantic_to_extend_schema
from .typed_run import ModelT

__all__ = [
    "TypedExtractConfigParams",
    "TypedExtractorParams",
    "convert_typed_config",
    "convert_typed_extractor",
    "get_extractor_schema_model",
    "get_schema_model",
]

_OVERRIDE_CONFIG_KEYS = ("override_config", "overrideConfig")


class TypedExtractConfigParams(typing_extensions.TypedDict, typing.Generic[ModelT], total=False):
    """
    Extract configuration whose ``schema`` is a pydantic model class.
    Extraction output will be validated against the model.
    """

    schema: typing_extensions.Required[typing.Type[ModelT]]
    base_processor: ExtractBaseProcessor
    base_version: str
    extraction_rules: str
    advanced_options: ExtractAdvancedOptionsParams
    parse_config: ParseConfigParams


class TypedExtractorParams(typing_extensions.TypedDict, typing.Generic[ModelT]):
    """
    Reference to an existing extractor whose ``override_config.schema`` is a
    pydantic model class. Extraction output will be validated against the model.
    """

    id: str
    version: typing_extensions.NotRequired[ProcessorVersionString]
    override_config: TypedExtractConfigParams[ModelT]


def _as_schema_model(schema: typing.Any) -> typing.Optional[typing.Type[pydantic.BaseModel]]:
    if isinstance(schema, type) and issubclass(schema, pydantic.BaseModel):
        return schema
    return None


def get_schema_model(config: typing.Any) -> typing.Optional[typing.Type[pydantic.BaseModel]]:
    """Return the pydantic model used as ``config["schema"]``, if there is one."""
    if isinstance(config, typing.Mapping):
        return _as_schema_model(config.get("schema"))
    return None


def convert_typed_config(config: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Return a copy of ``config`` with its pydantic model schema converted to JSON Schema."""
    converted = dict(config)
    converted["schema"] = pydantic_to_extend_schema(converted["schema"])
    return converted


def get_extractor_schema_model(extractor: typing.Any) -> typing.Optional[typing.Type[pydantic.BaseModel]]:
    """Return the pydantic model used as ``extractor["override_config"]["schema"]``, if there is one."""
    if not isinstance(extractor, typing.Mapping):
        return None
    for key in _OVERRIDE_CONFIG_KEYS:
        model = get_schema_model(extractor.get(key))
        if model is not None:
            return model
    return None


def convert_typed_extractor(extractor: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Return a copy of ``extractor`` with its override config's schema converted to JSON Schema."""
    converted = dict(extractor)
    for key in _OVERRIDE_CONFIG_KEYS:
        if get_schema_model(converted.get(key)) is not None:
            converted[key] = convert_typed_config(converted[key])
    return converted
