from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseTemplatingNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.templating_node import TemplatingNode


class TemplatingNodeDisplay(BaseTemplatingNodeDisplay[TemplatingNode]):
    label = "Templating Node"
    node_id = UUID("557f9b98-2229-437e-844b-cac7868a0534")
    output_id = UUID("adf0256c-cdcd-4e62-92a3-a9c1b8e70e0f")
    target_handle_id = UUID("73d41849-2a2d-4994-b220-b636c51fab42")
    template_input_id = UUID("ed2cf7f8-2620-4a8e-bea2-51ba8f48d9ac")
    node_input_ids_by_name = {
        "example_var_1": UUID("60888a25-050a-4593-8d82-ba7d40eda1ac"),
        "template": UUID("ed2cf7f8-2620-4a8e-bea2-51ba8f48d9ac"),
    }
    port_displays = {
        TemplatingNode.Ports.default: PortDisplayOverrides(id=UUID("0f8cbd50-1919-4c2e-8b1b-1ad741b5da35"))
    }
    display_data = NodeDisplayData(position=NodeDisplayPosition(x=1474, y=540.5), width=480, height=221)
