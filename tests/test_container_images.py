# This file was auto-generated by Fern from our API Definition.

from vellum import Vellum
from vellum import AsyncVellum
import typing
from .utilities import validate_response


async def test_list_(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "count": 123,
        "next": "http://api.example.org/accounts/?offset=400&limit=100",
        "previous": "http://api.example.org/accounts/?offset=200&limit=100",
        "results": [
            {
                "id": "id",
                "name": "name",
                "visibility": "DEFAULT",
                "created": "2024-01-15T09:30:00Z",
                "modified": "2024-01-15T09:30:00Z",
                "repository": "repository",
                "sha": "sha",
                "tags": ["tags"],
            }
        ],
    }
    expected_types: typing.Any = {
        "count": "integer",
        "next": None,
        "previous": None,
        "results": (
            "list",
            {
                0: {
                    "id": None,
                    "name": None,
                    "visibility": None,
                    "created": "datetime",
                    "modified": "datetime",
                    "repository": None,
                    "sha": None,
                    "tags": ("list", {0: None}),
                }
            },
        ),
    }
    response = client.container_images.list()
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.container_images.list()
    validate_response(async_response, expected_response, expected_types)


async def test_retrieve(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "name": "name",
        "visibility": "DEFAULT",
        "created": "2024-01-15T09:30:00Z",
        "modified": "2024-01-15T09:30:00Z",
        "repository": "repository",
        "sha": "sha",
        "tags": ["tags"],
    }
    expected_types: typing.Any = {
        "id": None,
        "name": None,
        "visibility": None,
        "created": "datetime",
        "modified": "datetime",
        "repository": None,
        "sha": None,
        "tags": ("list", {0: None}),
    }
    response = client.container_images.retrieve(id="id")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.container_images.retrieve(id="id")
    validate_response(async_response, expected_response, expected_types)


async def test_push_container_image(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "name": "name",
        "visibility": "DEFAULT",
        "created": "2024-01-15T09:30:00Z",
        "modified": "2024-01-15T09:30:00Z",
        "repository": "repository",
        "sha": "sha",
        "tags": ["tags"],
    }
    expected_types: typing.Any = {
        "id": None,
        "name": None,
        "visibility": None,
        "created": "datetime",
        "modified": "datetime",
        "repository": None,
        "sha": None,
        "tags": ("list", {0: None}),
    }
    response = client.container_images.push_container_image(name="name", sha="sha", tags=["tags"])
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.container_images.push_container_image(name="name", sha="sha", tags=["tags"])
    validate_response(async_response, expected_response, expected_types)
