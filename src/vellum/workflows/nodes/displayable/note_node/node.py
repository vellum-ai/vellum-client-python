from vellum.workflows.nodes.bases import BaseNode


class NoteNode(BaseNode):
    """
    A no-op Node purely used to display a note in the Vellum UI.
    """

    def run(self) -> BaseNode.Outputs:
        raise RuntimeError("NoteNode should never be run")
