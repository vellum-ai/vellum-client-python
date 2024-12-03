from uuid import UUID
from typing import ClassVar, Generic, Optional, TypeVar

from vellum.workflows.nodes import ErrorNode
from vellum.workflows.types.core import JsonObject
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.vellum.utils import create_node_input
from vellum_ee.workflows.display.types import WorkflowDisplayContext

_ErrorNodeType = TypeVar("_ErrorNodeType", bound=ErrorNode)

class BaseErrorNodeDisplay(BaseNodeVellumDisplay[_ErrorNodeType], Generic[_ErrorNodeType]):
    error_output_id: ClassVar[Optional[UUID]] = None

    def serialize(
            self, display_context: WorkflowDisplayContext, error_output_id: Optional[UUID] = None, **kwargs
    ) -> JsonObject:
        node = self._node
        node_id = self.node_id

        error_source_input_id = self.node_input_ids_by_name.get("error_source_input_id")

        node_inputs = [
            create_node_input(
                node_id=node_id,
                input_name=variable_name,
                value={},
                display_context=display_context,
                input_id=variable_id,
            )
            for variable_name, variable_id in self.node_input_ids_by_name.items()
        ]

        return {
            "id": str(node_id),
            "type": "ERROR",
            "inputs": [node_input.dict() for node_input in node_inputs],
            "data": {
                "label": self.label,
                "target_handle_id": str(self.get_target_handle_id()),
                "error_source_input_id": str(error_source_input_id),
                "error_output_id": str(self.error_output_id),
            },
            "display_data": self.get_display_data().dict(),
            "definition": self.get_definition().dict(),
        }
