from tests.workflows.basic_try_node.workflow import SimpleTryExample
from vellum_ee.workflows.display.workflows import VellumWorkflowDisplay
from vellum_ee.workflows.display.workflows.get_vellum_workflow_display_class import get_workflow_display


def test_serialize_workflow():
    # GIVEN a Workflow with a TryNode
    # WHEN we serialize it
    workflow_display = get_workflow_display(base_display_class=VellumWorkflowDisplay, workflow_class=SimpleTryExample)
    workflow_display.serialize()
