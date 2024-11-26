import json

from deepdiff import DeepDiff

from vellum.workflows.workflows.base import BaseWorkflow
from vellum_ee.workflows.display.workflows import VellumWorkflowDisplay
from vellum_ee.workflows.display.workflows.get_vellum_workflow_display_class import get_workflow_display


def test_code_to_display_data(code_to_display_fixture_paths):
    """Confirms that code representations of workflows are correctly serialized into their display representations."""

    expected_display_data_file_path, code_dir = code_to_display_fixture_paths
    base_module_path = __name__.split(".")[:-1]
    code_sub_path = code_dir.split("/".join(base_module_path))[1].split("/")[1:]
    module_path = ".".join(base_module_path + code_sub_path)

    workflow = BaseWorkflow.load_from_module(module_path)
    workflow_display = get_workflow_display(base_display_class=VellumWorkflowDisplay, workflow_class=workflow)
    actual_serialized_workflow: dict = workflow_display.serialize()

    with open(expected_display_data_file_path) as file:
        expected_serialized_workflow = json.load(file)  # noqa: F841

    def exclude_obj_callback(value, key):
        if key.endswith("input_id']") or key.endswith("['input_variable_id']"):
            return True

        return False

    assert not DeepDiff(
        expected_serialized_workflow,
        actual_serialized_workflow,
        exclude_obj_callback=exclude_obj_callback,
        significant_digits=6,
    )
