from tests.workflows.run_from_node.workflow import NextNode, RunFromNodeWorkflow, StartNode
from vellum.workflows.state.base import BaseState, StateMeta


def test_run_workflow__happy_path():
    # GIVEN a workflow that we expect to run from the middle of
    workflow = RunFromNodeWorkflow()

    # WHEN the workflow is run
    terminal_event = workflow.run(
        entrypoint_nodes=[NextNode],
        state=BaseState(
            meta=StateMeta(
                node_outputs={
                    StartNode.Outputs.next_value: 42,
                },
            )
        ),
    )

    # THEN the workflow should be fulfilled
    assert terminal_event.name == "workflow.execution.fulfilled"

    # AND the final value should be dependent on the intermediate State value
    assert terminal_event.outputs == {"final_value": 43}
