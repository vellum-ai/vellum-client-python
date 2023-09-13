# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...types.model_version_compile_prompt_response import ModelVersionCompilePromptResponse
from ...types.model_version_read import ModelVersionRead

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ModelVersionsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def retrieve(self, id: str) -> ModelVersionRead:
        """
        Used to retrieve a model version given its ID.

        Parameters:
            - id: str. A UUID string identifying this model version.
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().default}/", f"v1/model-versions/{id}"),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ModelVersionRead, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def model_version_compile_prompt(
        self, id: str, *, input_values: typing.Dict[str, typing.Any]
    ) -> ModelVersionCompilePromptResponse:
        """
        Compiles the prompt backing the model version using the provided input values.

        Parameters:
            - id: str. A UUID string identifying this model version.

            - input_values: typing.Dict[str, typing.Any]. Key/value pairs for each variable found within the model version's prompt template.
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_environment().default}/", f"v1/model-versions/{id}/compile-prompt"
            ),
            json=jsonable_encoder({"input_values": input_values}),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ModelVersionCompilePromptResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncModelVersionsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def retrieve(self, id: str) -> ModelVersionRead:
        """
        Used to retrieve a model version given its ID.

        Parameters:
            - id: str. A UUID string identifying this model version.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().default}/", f"v1/model-versions/{id}"),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ModelVersionRead, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def model_version_compile_prompt(
        self, id: str, *, input_values: typing.Dict[str, typing.Any]
    ) -> ModelVersionCompilePromptResponse:
        """
        Compiles the prompt backing the model version using the provided input values.

        Parameters:
            - id: str. A UUID string identifying this model version.

            - input_values: typing.Dict[str, typing.Any]. Key/value pairs for each variable found within the model version's prompt template.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_environment().default}/", f"v1/model-versions/{id}/compile-prompt"
            ),
            json=jsonable_encoder({"input_values": input_values}),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ModelVersionCompilePromptResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)