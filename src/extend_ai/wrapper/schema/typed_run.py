"""
Typed extract run wrappers.

When an extraction is created with a pydantic model as its schema, the SDK
returns a :class:`TypedExtractRun` whose ``output.value`` (and
``initial_output.value`` / ``reviewed_output.value``) are validated instances
of that model instead of plain dicts.
"""

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from ...types.extract_config import ExtractConfig
from ...types.extract_output import ExtractOutput
from ...types.extract_output_edits import ExtractOutputEdits
from ...types.extract_output_metadata import ExtractOutputMetadata
from ...types.extract_run import ExtractRun
from ...types.extractor_summary import ExtractorSummary
from ...types.extractor_version_summary import ExtractorVersionSummary
from ...types.file_summary import FileSummary
from ...types.processor_run_status import ProcessorRunStatus
from ...types.run_metadata import RunMetadata
from ...types.run_usage import RunUsage

__all__ = ["ModelT", "TypedExtractOutput", "TypedExtractRun", "parse_extract_run"]

ModelT = typing.TypeVar("ModelT", bound=pydantic.BaseModel)


def _validate_model(model: typing.Type[ModelT], value: typing.Any) -> ModelT:
    if IS_PYDANTIC_V2:
        return typing.cast(ModelT, model.model_validate(value))  # type: ignore[attr-defined]
    return typing.cast(ModelT, model.parse_obj(value))


class TypedExtractOutput(typing.Generic[ModelT]):
    """Extract output whose value is a validated pydantic model instance."""

    value: ModelT
    metadata: ExtractOutputMetadata

    def __init__(self, *, value: ModelT, metadata: ExtractOutputMetadata) -> None:
        self.value = value
        self.metadata = metadata

    def __repr__(self) -> str:
        return f"TypedExtractOutput(value={self.value!r})"


class TypedExtractRun(typing.Generic[ModelT]):
    """
    An extract run whose outputs are validated instances of the pydantic model
    that was used as the extraction schema.

    Mirrors :class:`~extend_ai.types.extract_run.ExtractRun`; the original
    response is available as ``raw``.
    """

    object: str
    id: str
    status: ProcessorRunStatus
    output: typing.Optional[TypedExtractOutput[ModelT]]
    initial_output: typing.Optional[TypedExtractOutput[ModelT]]
    reviewed_output: typing.Optional[TypedExtractOutput[ModelT]]
    failure_reason: typing.Optional[str]
    failure_message: typing.Optional[str]
    metadata: typing.Optional[RunMetadata]
    reviewed: bool
    edited: bool
    edits: typing.Optional[typing.Dict[str, typing.Optional[ExtractOutputEdits]]]
    config: ExtractConfig
    extractor: typing.Optional[ExtractorSummary]
    extractor_version: typing.Optional[ExtractorVersionSummary]
    file: typing.Optional[FileSummary]
    files: typing.Optional[typing.List[FileSummary]]
    parse_run_id: typing.Optional[str]
    dashboard_url: str
    usage: typing.Optional[RunUsage]
    created_at: typing.Any
    updated_at: typing.Any
    raw: ExtractRun
    """The original, untyped extract run response."""

    def __init__(self, run: ExtractRun, model: typing.Type[ModelT]) -> None:
        self.raw = run
        self.object = run.object
        self.id = run.id
        self.status = run.status
        self.output = _parse_output(run.output, model)
        self.initial_output = _parse_output(run.initial_output, model)
        self.reviewed_output = _parse_output(run.reviewed_output, model)
        self.failure_reason = run.failure_reason
        self.failure_message = run.failure_message
        self.metadata = run.metadata
        self.reviewed = run.reviewed
        self.edited = run.edited
        self.edits = run.edits
        self.config = run.config
        self.extractor = run.extractor
        self.extractor_version = run.extractor_version
        self.file = run.file
        self.files = run.files
        self.parse_run_id = run.parse_run_id
        self.dashboard_url = run.dashboard_url
        self.usage = run.usage
        self.created_at = run.created_at
        self.updated_at = run.updated_at

    def __repr__(self) -> str:
        return f"TypedExtractRun(id={self.id!r}, status={self.status!r}, output={self.output!r})"


def _parse_output(
    output: typing.Optional[ExtractOutput], model: typing.Type[ModelT]
) -> typing.Optional[TypedExtractOutput[ModelT]]:
    if output is None:
        return None
    value = getattr(output, "value", None)
    if value is None:
        raise ValueError(
            "Extract run output has no 'value' field; typed schemas are only supported "
            "for runs created with a JSON Schema config."
        )
    return TypedExtractOutput(
        value=_validate_model(model, value),
        metadata=typing.cast(ExtractOutputMetadata, getattr(output, "metadata", None)),
    )


def parse_extract_run(run: ExtractRun, model: typing.Type[ModelT]) -> TypedExtractRun[ModelT]:
    """
    Validate an extract run's outputs against a pydantic model.

    Args:
        run: A completed extract run.
        model: The pydantic model class that was used as the extraction schema.

    Returns:
        A :class:`TypedExtractRun` whose output values are instances of ``model``.

    Raises:
        pydantic.ValidationError: If an output value does not conform to the model.
            Extraction can return ``null`` for any field, so model fields should
            be declared ``Optional``.
    """
    return TypedExtractRun(run, model)
