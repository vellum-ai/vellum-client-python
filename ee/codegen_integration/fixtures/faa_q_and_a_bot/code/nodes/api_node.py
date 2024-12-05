from codegen_integration.fixtures.faa_q_and_a_bot.code import TemplatingNode

from vellum.workflows.constants import APIRequestMethod, AuthorizationType
from vellum.workflows.nodes.displayable import APINode as BaseAPINode
from vellum.workflows.references import VellumSecretReference


class APINode(BaseAPINode):
    url = TemplatingNode.Outputs.result  #type: ignore
    method = APIRequestMethod.GET
    json = None
    headers = {}
    api_key_header_key = "bcf3aac0-536e-42d5-b666-22cfe40eae98"
    authorization_type = AuthorizationType.API_KEY
    api_key_header_value = VellumSecretReference("cfafa394-efd8-4dbe-bada-3fb5f998bb97")
    bearer_token_value = None
