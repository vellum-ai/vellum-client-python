from vellum.workflows.nodes.bases.base import BaseNode

from ..inputs import Inputs


class ErrorNode(BaseNode):
    error = Inputs.error_source_input_id  # Not sure if this is the right way to get this
