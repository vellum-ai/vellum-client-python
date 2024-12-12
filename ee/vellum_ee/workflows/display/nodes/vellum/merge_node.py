from uuid import UUID
from typing import Any, ClassVar, Generic, List, Optional, Type, TypeVar

from vellum.workflows.nodes.displayable import MergeNode
from vellum.workflows.types.core import JsonObject
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.types import WorkflowDisplayContext
from vellum_ee.workflows.display.utils.uuids import uuid4_from_hash
from vellum_ee.workflows.display.vellum import EdgeVellumDisplay

_MergeNodeType = TypeVar("_MergeNodeType", bound=MergeNode)


class BaseMergeNodeDisplay(BaseNodeVellumDisplay[_MergeNodeType], Generic[_MergeNodeType]):
    target_handle_ids: ClassVar[List[UUID]]

    def __init__(self, node: Type[_MergeNodeType]):
        super().__init__(node)
        self._target_handle_iterator = 0

    def serialize(self, display_context: WorkflowDisplayContext, **kwargs: Any) -> JsonObject:
        node = self._node
        node_id = self.node_id

        all_edges: List[EdgeVellumDisplay] = [edge_display for _, edge_display in display_context.edge_displays.items()]
        merged_edges = [edge for edge in all_edges if edge.target_node_id == self.node_id]

        target_handle_ids = self.get_target_handle_ids()

        if target_handle_ids is None:
            target_handle_ids = [
                uuid4_from_hash(f"{node_id}|target_handle|{edge.source_node_id}") for edge in merged_edges
            ]
        elif len(target_handle_ids) != len(merged_edges):
            raise ValueError("If you explicitly specify target_handle_ids, you must specify one for each incoming edge")

        return {
            "id": str(node_id),
            "type": "MERGE",
            "inputs": [],
            "data": {
                "label": self.label,
                "merge_strategy": node.Trigger.merge_behavior.value,
                "target_handles": [{"id": str(target_handle_id)} for target_handle_id in target_handle_ids],
                "source_handle_id": str(self.get_source_handle_id(display_context.port_displays)),
            },
            "display_data": self.get_display_data().dict(),
            "definition": self.get_definition().dict(),
        }

    def get_target_handle_ids(self) -> Optional[List[UUID]]:
        return self._get_explicit_node_display_attr("target_handle_ids", List[UUID])

    def get_target_handle_id(self) -> UUID:
        # Edges call this method to know which handle to connect to
        # We use the order of the edges to determine the handle id. This is quite brittle to the order of the
        # edges, and we should look into a longer term solution, or cutover Merge Nodes to Generic Nodes soon
        target_handle_id = self.target_handle_ids[self._target_handle_iterator]
        self._target_handle_iterator += 1
        if self._target_handle_iterator >= len(self.target_handle_ids):
            self._target_handle_iterator = 0
        return target_handle_id
