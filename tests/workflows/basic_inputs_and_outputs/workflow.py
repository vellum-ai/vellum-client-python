from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    initial_value: int


class StartNode(BaseNode):
    value = Inputs.initial_value

    class Outputs(BaseOutputs):
        output_value: int

    def run(self) -> BaseOutputs:
        intermediate_value = self.value + 1
        computed_value = intermediate_value**2

        return self.Outputs(output_value=computed_value)


class BasicInputsAndOutputsWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = StartNode

    class Outputs(BaseOutputs):
        final_value = StartNode.Outputs.output_value
