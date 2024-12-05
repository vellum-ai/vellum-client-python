from typing import List

from vellum import ChatMessage
from vellum.workflows.nodes.displayable import SubworkflowDeploymentNode

from ..inputs import Inputs


class SubworkflowNode(SubworkflowDeploymentNode):
    deployment = "test-deployment"
    release_tag = "LATEST"
    subworkflow_inputs = {"chat_history": Inputs.chat_history}

    class Outputs(SubworkflowDeploymentNode.Outputs):
        chat_history: List[ChatMessage]
