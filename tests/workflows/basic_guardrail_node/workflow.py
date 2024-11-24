from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes import GuardrailNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    actual: str
    expected: str


class ExampleGuardrailNode(GuardrailNode):
    metric_definition = "example_metric_definition"

    metric_inputs = {
        "expected": Inputs.expected,
        "actual": Inputs.actual,
    }


class BasicGuardrailNodeWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = ExampleGuardrailNode

    class Outputs(BaseOutputs):
        score = ExampleGuardrailNode.Outputs.score
