# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx
import pydantic

from ...core.api_error import ApiError
from ...core.jsonable_encoder import jsonable_encoder
from ...core.remove_none_from_headers import remove_none_from_headers
from ...environment import VellumEnvironment
from ...errors.conflict_error import ConflictError
from ...types.provider_enum import ProviderEnum
from ...types.register_prompt_error_response import RegisterPromptErrorResponse
from ...types.register_prompt_model_parameters_request import RegisterPromptModelParametersRequest
from ...types.register_prompt_prompt_info_request import RegisterPromptPromptInfoRequest
from ...types.register_prompt_response import RegisterPromptResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RegisteredPromptsClient:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key

    def register_prompt(
        self,
        *,
        label: str,
        name: str,
        prompt: RegisterPromptPromptInfoRequest,
        provider: ProviderEnum,
        model: str,
        parameters: RegisterPromptModelParametersRequest,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> RegisterPromptResponse:
        _request: typing.Dict[str, typing.Any] = {
            "label": label,
            "name": name,
            "prompt": prompt,
            "provider": provider,
            "model": model,
            "parameters": parameters,
        }
        if meta is not OMIT:
            _request["meta"] = meta
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.default}/", "v1/registered-prompts/register"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RegisterPromptResponse, _response.json())  # type: ignore
        if _response.status_code == 409:
            raise ConflictError(pydantic.parse_obj_as(RegisterPromptErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncRegisteredPromptsClient:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key

    async def register_prompt(
        self,
        *,
        label: str,
        name: str,
        prompt: RegisterPromptPromptInfoRequest,
        provider: ProviderEnum,
        model: str,
        parameters: RegisterPromptModelParametersRequest,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> RegisterPromptResponse:
        _request: typing.Dict[str, typing.Any] = {
            "label": label,
            "name": name,
            "prompt": prompt,
            "provider": provider,
            "model": model,
            "parameters": parameters,
        }
        if meta is not OMIT:
            _request["meta"] = meta
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.default}/", "v1/registered-prompts/register"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RegisterPromptResponse, _response.json())  # type: ignore
        if _response.status_code == 409:
            raise ConflictError(pydantic.parse_obj_as(RegisterPromptErrorResponse, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
