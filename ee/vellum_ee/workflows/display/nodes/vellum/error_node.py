from uuid import UUID
from typing import Any, ClassVar, Generic, Optional, TypeVar

from vellum.workflows.nodes import ErrorNode
from vellum.workflows.types.core import JsonObject
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.utils import raise_if_descriptor
from vellum_ee.workflows.display.nodes.vellum.utils import create_node_input
from vellum_ee.workflows.display.types import WorkflowDisplayContext

_ErrorNodeType = TypeVar("_ErrorNodeType", bound=ErrorNode)


class BaseErrorNodeDisplay(BaseNodeVellumDisplay[_ErrorNodeType], Generic[_ErrorNodeType]):
    error_source_input_id: ClassVar[Optional[UUID]] = None
    error_output_id: ClassVar[Optional[UUID]] = None

    def serialize(
        self, display_context: WorkflowDisplayContext, **kwargs: Any
    ) -> JsonObject:
        node = self._node
        node_id = self.node_id

        error_node_input = create_node_input(
            node_id=node_id,
            input_name="error_source_input_id",
            value=raise_if_descriptor(node.error),
            display_context=display_context,
            input_id=self.error_source_input_id,
        )

        inputs = [
            error_node_input
        ]

        return {
            "id": str(node_id),
            "type": "ERROR",
            "inputs": [input_.dict() for input_ in inputs],
            "data": {
                "label": self.label,
                "name": "error-node",
                "target_handle_id": str(self.get_target_handle_id()),
                "error_source_input_id": str(error_node_input.id),
                "error_output_id": self._get_node_display_uuid("error_output_id"),

            },
            "display_data": self.get_display_data().dict(),
            "definition": self.get_definition().dict(),
        }
