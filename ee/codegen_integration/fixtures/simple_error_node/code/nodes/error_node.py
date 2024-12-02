from vellum.workflows.nodes.bases.base import BaseNode

from ..inputs import Inputs


class ErrorNode(BaseNode):
    error_source_input_id = Inputs.error_source_input_id
