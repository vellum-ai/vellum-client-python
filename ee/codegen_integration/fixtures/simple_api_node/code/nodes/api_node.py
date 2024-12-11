from vellum.workflows.constants import APIRequestMethod
from vellum.workflows.nodes.displayable import APINode
from vellum.workflows.references import VellumSecretReference


class ApiNode(APINode):
    url = "https://www.testing.com"
    method = APIRequestMethod.POST
    json = '"hii"'
    headers = {
        "test": VellumSecretReference("cecd16a2-4de5-444d-acff-37a5c400600c"),
        "nom": VellumSecretReference("cecd16a2-4de5-444d-acff-37a5c400600c"),
    }
    api_key_header_key = "908e1fb5-bcba-4388-ae1d-a53d256eda97"
    authorization_type = None
    api_key_header_value = None
    bearer_token_value = None
