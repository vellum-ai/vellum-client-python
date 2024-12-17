from vellum import SearchResponse, SearchResult, SearchResultDocument

from tests.workflows.basic_search_node.workflow import BasicSearchWorkflow, Inputs


def test_run_workflow__happy_path(vellum_client):
    """Confirm that we can successfully invoke a Workflow with a single Search Node"""

    # GIVEN a workflow that's set up run a Search Node
    workflow = BasicSearchWorkflow()

    # AND a Search request that will return a 200 ok resposne
    search_response = SearchResponse(
        results=[
            SearchResult(
                text="Search query", score="0.0", keywords=["keywords"], document=SearchResultDocument(label="label")
            )
        ]
    )

    vellum_client.search.return_value = search_response

    # WHEN we run the workflow
    terminal_event = workflow.run(inputs=Inputs(query="Search query"))

    # THEN the workflow should have completed successfully
    assert terminal_event.name == "workflow.execution.fulfilled"

    # AND the outputs should be as expected
    assert terminal_event.outputs.text == "Search query"
