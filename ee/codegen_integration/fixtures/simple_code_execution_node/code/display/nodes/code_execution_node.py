from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseCodeExecutionNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.code_execution_node import CodeExecutionNode


class CodeExecutionNodeDisplay(BaseCodeExecutionNodeDisplay[CodeExecutionNode]):
    code_input_id = UUID("19b05769-cee3-4659-80d1-66fcae4e27c3")
    runtime_input_id = UUID("ebcd1dc6-b0cc-4e67-af67-a42993cf038b")
    output_id = UUID("9d1dae27-6e6a-40bf-a401-611c974d4143")
    log_output_id = UUID("b57399ac-93ce-4225-8543-10bac4fe82f4")
    node_input_ids_by_name = {
        "arg": UUID("78da07ee-cc77-445e-af85-f60ab4f7a59f"),
        "code": UUID("19b05769-cee3-4659-80d1-66fcae4e27c3"),
        "runtime": UUID("ebcd1dc6-b0cc-4e67-af67-a42993cf038b"),
    }
    port_displays = {
        CodeExecutionNode.Ports.default: PortDisplayOverrides(id=UUID("7775a376-e408-406e-aa46-c6c87ab95bfd"))
    }
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=1816.3157894736842, y=213.93599376731305), width=480, height=224
    )
