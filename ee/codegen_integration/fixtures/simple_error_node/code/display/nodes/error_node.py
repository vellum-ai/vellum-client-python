from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseSearchNodeDisplay
from vellum_ee.workflows.display.nodes.types import NodeOutputDisplay, PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes import ErrorNode


class ErrorNodeDisplay(ErrorNode):
    label = "Error Node"
    node_id = UUID("e5ff9360-a29c-437b-a9c1-05fc52df2834")
    target_handle_id = UUID("370d712d-3369-424e-bcf7-f4da1aef3928")
    node_input_ids_by_name = {
        "query": UUID("f3a0d8b9-7772-4db6-8e28-f49f8c4d9e2a"),
        "document_index_id": UUID("b49bc1ab-2ad5-4cf2-8966-5cc87949900d"),
        "weights": UUID("1daf3180-4b92-472a-8665-a7703c84a94e"),
        "limit": UUID("161d264e-d04e-4c37-8e50-8bbb4c90c46e"),
        "separator": UUID("4eddefc0-90d5-422a-aec2-bc94c8f1d83c"),
        "result_merging_enabled": UUID("dc9f880b-81bc-4644-b025-8f7d5db23a48"),
        "external_id_filters": UUID("61933e79-b0c2-4e3c-bf07-e2d93b9d9c54"),
        "metadata_filters": UUID("7c43b315-d1f2-4727-9540-6cc3fd4641f3"),
    }
    output_display = {
        ErrorNode.Outputs.error: NodeOutputDisplay(id=UUID("77839b3c-fe1c-4dcb-9c61-2fac827f729b"), name="error"),
    }
    port_displays = {ErrorNode.Ports.default: PortDisplayOverrides(id=UUID("e4dedb66-0638-4f0c-9941-6420bfe353b2"))}
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=1966.960664819945, y=223.1684037396122), width=480, height=180
    )
