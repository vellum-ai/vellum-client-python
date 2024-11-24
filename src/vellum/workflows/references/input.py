from typing import Union

from vellum.workflows.references.external_input import ExternalInputReference
from vellum.workflows.references.workflow_input import WorkflowInputReference

# Note: We may want to consolidate these two into a single descriptor.
InputReference = Union[ExternalInputReference, WorkflowInputReference]
