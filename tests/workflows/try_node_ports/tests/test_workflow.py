import pytest

from pytest_mock import MockerFixture

from tests.workflows.try_node_ports.workflow import TryNodePortsWorkflow


@pytest.fixture
def mock_random_int(mocker: MockerFixture):
    base_module = __name__.split(".")[:-2]
    return mocker.patch(".".join(base_module + ["workflow", "random", "randint"]))


def test_run_workflow__node_fails__happy_path(mock_random_int):
    # GIVEN a workflow that references a try node adorned node with ports
    workflow = TryNodePortsWorkflow()

    # AND the underlying node fails
    mock_random_int.return_value = 75

    # WHEN the workflow is run
    terminal_event = workflow.run()

    # THEN the workflow should complete successfully
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event

    # AND the output should indicate that the error port was invoked
    assert terminal_event.outputs.final_value == "Threshold exceeded"
