from vellum.workflows.nodes.displayable import TemplatingNode
from vellum.workflows.state import BaseState

from .faa_document_store import FAADocumentStore


class FormattedSearchResults(TemplatingNode[BaseState, str]):
    template = "{% for result in results -%}\nPolicy {{ result.document.label }}:\n------\n{{ result.text }}\n{% if not loop.last %}\n\n#####\n\n{% endif %}\n{% endfor %}"
    inputs = {"results": FAADocumentStore.Outputs.results}
