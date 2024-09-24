# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...types.prompt_request_input_request import PromptRequestInputRequest
from ...types.vellum_variable_request import VellumVariableRequest
from ...types.prompt_parameters_request import PromptParametersRequest
from ...types.prompt_block_request import PromptBlockRequest
from ...types.ad_hoc_expand_meta_request import AdHocExpandMetaRequest
from ...core.request_options import RequestOptions
from ...types.ad_hoc_execute_prompt_event import AdHocExecutePromptEvent
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.pydantic_utilities import parse_obj_as
import json
from ...errors.bad_request_error import BadRequestError
from ...errors.forbidden_error import ForbiddenError
from ...errors.internal_server_error import InternalServerError
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AdHocClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def adhoc_execute_prompt_stream(
        self,
        *,
        ml_model: str,
        input_values: typing.Sequence[PromptRequestInputRequest],
        input_variables: typing.Sequence[VellumVariableRequest],
        parameters: PromptParametersRequest,
        blocks: typing.Sequence[PromptBlockRequest],
        expand_meta: typing.Optional[AdHocExpandMetaRequest] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[AdHocExecutePromptEvent]:
        """
        An internal-only endpoint that's subject to breaking changes without notice. Not intended for public use.

        Parameters
        ----------
        ml_model : str

        input_values : typing.Sequence[PromptRequestInputRequest]

        input_variables : typing.Sequence[VellumVariableRequest]

        parameters : PromptParametersRequest

        blocks : typing.Sequence[PromptBlockRequest]

        expand_meta : typing.Optional[AdHocExpandMetaRequest]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[AdHocExecutePromptEvent]


        Examples
        --------
        from vellum import (
            AdHocExpandMetaRequest,
            EphemeralPromptCacheConfigRequest,
            JinjaPromptBlockPropertiesRequest,
            JinjaPromptBlockRequest,
            PromptParametersRequest,
            PromptRequestStringInputRequest,
            Vellum,
            VellumVariableRequest,
        )

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        response = client.ad_hoc.adhoc_execute_prompt_stream(
            ml_model="string",
            input_values=[
                PromptRequestStringInputRequest(
                    key="string",
                    value="string",
                )
            ],
            input_variables=[
                VellumVariableRequest(
                    id="string",
                    key="string",
                    type="STRING",
                )
            ],
            parameters=PromptParametersRequest(
                stop=["string"],
                temperature=1.1,
                max_tokens=1,
                top_p=1.1,
                top_k=1,
                frequency_penalty=1.1,
                presence_penalty=1.1,
                logit_bias={"string": {"key": "value"}},
                custom_parameters={"string": {"key": "value"}},
            ),
            blocks=[
                JinjaPromptBlockRequest(
                    properties=JinjaPromptBlockPropertiesRequest(
                        template="string",
                        template_type="STRING",
                    ),
                    id="string",
                    state="ENABLED",
                    cache_config=EphemeralPromptCacheConfigRequest(
                        type={"key": "value"},
                    ),
                )
            ],
            expand_meta=AdHocExpandMetaRequest(
                cost=True,
                model_name=True,
                usage=True,
                finish_reason=True,
            ),
        )
        for chunk in response:
            yield chunk
        """
        with self._client_wrapper.httpx_client.stream(
            "v1/ad-hoc/execute-prompt-stream",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "ml_model": ml_model,
                "input_values": convert_and_respect_annotation_metadata(
                    object_=input_values, annotation=typing.Sequence[PromptRequestInputRequest], direction="write"
                ),
                "input_variables": convert_and_respect_annotation_metadata(
                    object_=input_variables, annotation=typing.Sequence[VellumVariableRequest], direction="write"
                ),
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PromptParametersRequest, direction="write"
                ),
                "blocks": convert_and_respect_annotation_metadata(
                    object_=blocks, annotation=typing.Sequence[PromptBlockRequest], direction="write"
                ),
                "expand_meta": convert_and_respect_annotation_metadata(
                    object_=expand_meta, annotation=AdHocExpandMetaRequest, direction="write"
                ),
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    for _text in _response.iter_lines():
                        try:
                            if len(_text) == 0:
                                continue
                            yield typing.cast(
                                AdHocExecutePromptEvent,
                                parse_obj_as(
                                    type_=AdHocExecutePromptEvent,  # type: ignore
                                    object_=json.loads(_text),
                                ),
                            )
                        except:
                            pass
                    return
                _response.read()
                if _response.status_code == 400:
                    raise BadRequestError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                if _response.status_code == 403:
                    raise ForbiddenError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                if _response.status_code == 500:
                    raise InternalServerError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncAdHocClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def adhoc_execute_prompt_stream(
        self,
        *,
        ml_model: str,
        input_values: typing.Sequence[PromptRequestInputRequest],
        input_variables: typing.Sequence[VellumVariableRequest],
        parameters: PromptParametersRequest,
        blocks: typing.Sequence[PromptBlockRequest],
        expand_meta: typing.Optional[AdHocExpandMetaRequest] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[AdHocExecutePromptEvent]:
        """
        An internal-only endpoint that's subject to breaking changes without notice. Not intended for public use.

        Parameters
        ----------
        ml_model : str

        input_values : typing.Sequence[PromptRequestInputRequest]

        input_variables : typing.Sequence[VellumVariableRequest]

        parameters : PromptParametersRequest

        blocks : typing.Sequence[PromptBlockRequest]

        expand_meta : typing.Optional[AdHocExpandMetaRequest]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[AdHocExecutePromptEvent]


        Examples
        --------
        import asyncio

        from vellum import (
            AdHocExpandMetaRequest,
            AsyncVellum,
            EphemeralPromptCacheConfigRequest,
            JinjaPromptBlockPropertiesRequest,
            JinjaPromptBlockRequest,
            PromptParametersRequest,
            PromptRequestStringInputRequest,
            VellumVariableRequest,
        )

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            response = await client.ad_hoc.adhoc_execute_prompt_stream(
                ml_model="string",
                input_values=[
                    PromptRequestStringInputRequest(
                        key="string",
                        value="string",
                    )
                ],
                input_variables=[
                    VellumVariableRequest(
                        id="string",
                        key="string",
                        type="STRING",
                    )
                ],
                parameters=PromptParametersRequest(
                    stop=["string"],
                    temperature=1.1,
                    max_tokens=1,
                    top_p=1.1,
                    top_k=1,
                    frequency_penalty=1.1,
                    presence_penalty=1.1,
                    logit_bias={"string": {"key": "value"}},
                    custom_parameters={"string": {"key": "value"}},
                ),
                blocks=[
                    JinjaPromptBlockRequest(
                        properties=JinjaPromptBlockPropertiesRequest(
                            template="string",
                            template_type="STRING",
                        ),
                        id="string",
                        state="ENABLED",
                        cache_config=EphemeralPromptCacheConfigRequest(
                            type={"key": "value"},
                        ),
                    )
                ],
                expand_meta=AdHocExpandMetaRequest(
                    cost=True,
                    model_name=True,
                    usage=True,
                    finish_reason=True,
                ),
            )
            async for chunk in response:
                yield chunk


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            "v1/ad-hoc/execute-prompt-stream",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "ml_model": ml_model,
                "input_values": convert_and_respect_annotation_metadata(
                    object_=input_values, annotation=typing.Sequence[PromptRequestInputRequest], direction="write"
                ),
                "input_variables": convert_and_respect_annotation_metadata(
                    object_=input_variables, annotation=typing.Sequence[VellumVariableRequest], direction="write"
                ),
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PromptParametersRequest, direction="write"
                ),
                "blocks": convert_and_respect_annotation_metadata(
                    object_=blocks, annotation=typing.Sequence[PromptBlockRequest], direction="write"
                ),
                "expand_meta": convert_and_respect_annotation_metadata(
                    object_=expand_meta, annotation=AdHocExpandMetaRequest, direction="write"
                ),
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    async for _text in _response.aiter_lines():
                        try:
                            if len(_text) == 0:
                                continue
                            yield typing.cast(
                                AdHocExecutePromptEvent,
                                parse_obj_as(
                                    type_=AdHocExecutePromptEvent,  # type: ignore
                                    object_=json.loads(_text),
                                ),
                            )
                        except:
                            pass
                    return
                await _response.aread()
                if _response.status_code == 400:
                    raise BadRequestError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                if _response.status_code == 403:
                    raise ForbiddenError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                if _response.status_code == 500:
                    raise InternalServerError(
                        typing.cast(
                            typing.Optional[typing.Any],
                            parse_obj_as(
                                type_=typing.Optional[typing.Any],  # type: ignore
                                object_=_response.json(),
                            ),
                        )
                    )
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)
