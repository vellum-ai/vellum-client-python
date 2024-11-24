import os
import tempfile
from uuid import uuid4

from tests.workflows.emit_node_loop.workflow import EmitNodeLoopWorkflow, Inputs


def test_workflow__happy_path():
    """
    This test ensures that State Forking (nodes receiving their own copy of State) works in a loop,
    for use cases that include emitting data from a node within a loop.
    """

    # GIVEN a workflow with a loop that emits data
    workflow = EmitNodeLoopWorkflow()

    # AND we have an external data source set up
    root_dir = os.path.join(tempfile.gettempdir(), str(uuid4()))
    os.makedirs(root_dir, exist_ok=True)

    # WHEN the workflow is run
    inputs = Inputs(file_path=os.path.join(root_dir, "emit_node_loop.txt"))
    terminal_event = workflow.run(inputs=inputs)

    # THEN the workflow should complete successfully
    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.file_path == inputs.file_path
    assert terminal_event.outputs.count == 4

    # AND the external data source should contain the expected data
    # TODO: Resolve descriptors within event.outputs
    # https://app.shortcut.com/vellum/story/4936
    with open(terminal_event.outputs.file_path) as f:  # type: ignore[call-overload]
        emitted_events = f.readlines()
        assert set(emitted_events) == {"Hello: 1\n", "Hello: 2\n", "Hello: 3\n"}
