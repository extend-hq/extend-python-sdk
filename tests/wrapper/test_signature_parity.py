"""
Guards against wrapper code drifting from the Fern-generated SDK.

The wrapper layer re-declares parts of the generated API surface:

- `create_and_poll()` mirrors each generated `create()` signature
- `TypedExtractConfigParams` / `TypedExtractorParams` mirror the generated
  request TypedDicts (with `schema` retyped to a pydantic model class)
- `TypedExtractRun` mirrors the fields of the generated `ExtractRun`

When SDK regeneration adds a parameter, key, or field, these tests fail so the
wrapper gets updated in the same change. (Methods that *override* a generated
method, like `Extend.extract()` and `ExtractorsClient.create()`, are already
covered: mypy rejects overrides whose signatures are incompatible with the
generated superclass.)
"""

import inspect
import typing

import pytest

from extend_ai.core.pydantic_utilities import IS_PYDANTIC_V2
from extend_ai.wrapper.resources import (
    classify_runs,
    edit_runs,
    extract_runs,
    parse_runs,
    split_runs,
    workflow_runs,
)


def _param_names(func: typing.Any) -> typing.Set[str]:
    return {name for name in inspect.signature(func).parameters if name != "self"}


def _typed_dict_keys(td: typing.Any) -> typing.Set[str]:
    return set(td.__annotations__)


RUN_CLIENTS = [
    classify_runs.ClassifyRunsClient,
    classify_runs.AsyncClassifyRunsClient,
    edit_runs.EditRunsClient,
    edit_runs.AsyncEditRunsClient,
    extract_runs.ExtractRunsClient,
    extract_runs.AsyncExtractRunsClient,
    parse_runs.ParseRunsClient,
    parse_runs.AsyncParseRunsClient,
    split_runs.SplitRunsClient,
    split_runs.AsyncSplitRunsClient,
    workflow_runs.WorkflowRunsClient,
    workflow_runs.AsyncWorkflowRunsClient,
]


@pytest.mark.parametrize("wrapper_client", RUN_CLIENTS, ids=lambda cls: cls.__name__)
def test_create_and_poll_accepts_all_create_params(wrapper_client):
    """Every parameter of the generated create() must be exposed by create_and_poll()."""
    generated_client = wrapper_client.__mro__[1]
    create_params = _param_names(generated_client.create) - {"request_options"}
    create_and_poll_params = _param_names(wrapper_client.create_and_poll)

    missing = create_params - create_and_poll_params
    assert not missing, (
        f"{wrapper_client.__name__}.create_and_poll() is missing parameters that "
        f"{generated_client.__name__}.create() accepts: {sorted(missing)}. "
        "Add them to create_and_poll() and forward them to create()."
    )


def test_typed_extract_config_matches_generated_config_keys():
    from extend_ai.requests.extract_config_json import ExtractConfigJsonParams
    from extend_ai.wrapper.schema import TypedExtractConfigParams

    generated_keys = _typed_dict_keys(ExtractConfigJsonParams)
    typed_keys = _typed_dict_keys(TypedExtractConfigParams)

    missing = generated_keys - typed_keys
    assert not missing, (
        f"TypedExtractConfigParams is missing keys that ExtractConfigJsonParams has: {sorted(missing)}. "
        "Add them so typed configs accept the same options as untyped configs."
    )
    extra = typed_keys - generated_keys
    assert not extra, f"TypedExtractConfigParams has keys the generated config does not: {sorted(extra)}"


def test_typed_extractor_matches_generated_extractor_keys():
    from extend_ai.extract_runs.requests.extract_runs_create_request_extractor import (
        ExtractRunsCreateRequestExtractorParams,
    )
    from extend_ai.wrapper.schema import TypedExtractorParams

    generated_keys = _typed_dict_keys(ExtractRunsCreateRequestExtractorParams)
    typed_keys = _typed_dict_keys(TypedExtractorParams)

    assert generated_keys == typed_keys, (
        f"TypedExtractorParams keys {sorted(typed_keys)} differ from generated "
        f"ExtractRunsCreateRequestExtractorParams keys {sorted(generated_keys)}."
    )


def test_typed_extract_run_mirrors_extract_run_fields():
    from extend_ai.types.extract_run import ExtractRun
    from extend_ai.wrapper.schema import TypedExtractRun

    if IS_PYDANTIC_V2:
        run_fields = set(ExtractRun.model_fields)
    else:
        run_fields = set(ExtractRun.__fields__)

    typed_fields = set(TypedExtractRun.__annotations__)

    missing = run_fields - typed_fields
    assert not missing, (
        f"TypedExtractRun is missing fields that ExtractRun has: {sorted(missing)}. "
        "Add the attributes to TypedExtractRun and copy them in its constructor."
    )
