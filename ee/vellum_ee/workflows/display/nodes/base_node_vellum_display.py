from uuid import UUID
from typing import ClassVar, Dict, Optional

from vellum_ee.workflows.display.nodes.base_node_display import BaseNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplay
from vellum_ee.workflows.display.utils.uuids import uuid4_from_hash
from vellum_ee.workflows.display.vellum import NodeDisplayData
from vellum.workflows.ports import Port
from vellum.workflows.types.generics import NodeType


class BaseNodeVellumDisplay(BaseNodeDisplay[NodeType]):
    # Used to explicitly set display data for a node
    display_data: ClassVar[Optional[NodeDisplayData]] = None

    # Used to explicitly set the target handle id for a node
    target_handle_id: ClassVar[Optional[UUID]] = None

    # Used to explicitly set the node input ids by name for a node
    node_input_ids_by_name: ClassVar[Dict[str, UUID]] = {}

    def _get_node_display_uuid(self, attribute: str) -> UUID:
        explicit_value = self._get_explicit_node_display_attr(attribute, UUID)
        return explicit_value if explicit_value else uuid4_from_hash(f"{self.node_id}|{attribute}")

    def get_display_data(self) -> NodeDisplayData:
        explicit_value = self._get_explicit_node_display_attr("display_data", NodeDisplayData)
        return explicit_value if explicit_value else NodeDisplayData()

    def get_target_handle_id(self) -> UUID:
        return self._get_node_display_uuid("target_handle_id")

    def get_source_handle_id(self, port_displays: Dict[Port, PortDisplay]) -> UUID:
        default_port = self._node.Ports.default
        default_port_display = port_displays[default_port]
        return default_port_display.id
