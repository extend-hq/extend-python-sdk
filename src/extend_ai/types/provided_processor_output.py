# This file was auto-generated by Fern from our API Definition.

import typing

from .provided_classifier_output import ProvidedClassifierOutput
from .provided_extraction_output import ProvidedExtractionOutput
from .provided_splitter_output import ProvidedSplitterOutput

ProvidedProcessorOutput = typing.Union[ProvidedExtractionOutput, ProvidedClassifierOutput, ProvidedSplitterOutput]
