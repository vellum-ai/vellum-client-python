from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes import SubworkflowDeploymentNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    city: str
    date: str


class ExampleSubworkflowDeploymentNode(SubworkflowDeploymentNode):
    deployment = "example_workflow_deployment"

    class Outputs(BaseOutputs):
        temperature: float
        reasoning: str

    subworkflow_inputs = {
        "city": Inputs.city,
        "date": Inputs.date,
    }


class BasicSubworkflowDeploymentWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = ExampleSubworkflowDeploymentNode

    class Outputs(BaseOutputs):
        temperature = ExampleSubworkflowDeploymentNode.Outputs.temperature
        reasoning = ExampleSubworkflowDeploymentNode.Outputs.reasoning
