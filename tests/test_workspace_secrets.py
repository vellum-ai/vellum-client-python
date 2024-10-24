# This file was auto-generated by Fern from our API Definition.

from vellum import Vellum
from vellum import AsyncVellum
import typing
from .utilities import validate_response


async def test_retrieve(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "modified": "2024-01-15T09:30:00Z",
        "name": "name",
        "label": "label",
        "secret_type": "USER_DEFINED",
        "variable_type": "STRING",
    }
    expected_types: typing.Any = {
        "id": None,
        "modified": "datetime",
        "name": None,
        "label": None,
        "secret_type": None,
        "variable_type": None,
    }
    response = client.workspace_secrets.retrieve(id="id")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.workspace_secrets.retrieve(id="id")
    validate_response(async_response, expected_response, expected_types)
