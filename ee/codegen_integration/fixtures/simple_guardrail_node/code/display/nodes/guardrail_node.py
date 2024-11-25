from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseGuardrailNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.guardrail_node import GuardrailNode


class GuardrailNodeDisplay(BaseGuardrailNodeDisplay[GuardrailNode]):
    label = "Guardrail Node"
    node_id = UUID("c207b440-6aac-4047-a37c-e25fcb5b9cfb")
    target_handle_id = UUID("1817fbab-db21-4219-8b34-0e150ce78887")
    metric_input_ids_by_name = {
        "expected": UUID("3f917af8-03a4-4ca4-8d40-fa662417fe9c"),
        "actual": UUID("bed55ada-923e-46ef-8340-1a5b0b563dc1"),
    }
    node_input_ids_by_name = {
        "expected": UUID("3f917af8-03a4-4ca4-8d40-fa662417fe9c"),
        "actual": UUID("bed55ada-923e-46ef-8340-1a5b0b563dc1"),
    }
    port_displays = {GuardrailNode.Ports.default: PortDisplayOverrides(id=UUID("92aafe31-101b-47d3-86f2-e261c7747c16"))}
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=1985.9562846580402, y=180.75743992606283), width=464, height=224
    )