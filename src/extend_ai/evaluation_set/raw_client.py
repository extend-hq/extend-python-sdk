# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.request_options import RequestOptions
from ..core.unchecked_base_model import construct_type
from ..errors.bad_request_error import BadRequestError
from ..errors.not_found_error import NotFoundError
from ..errors.unauthorized_error import UnauthorizedError
from ..types.error import Error
from ..types.max_page_size import MaxPageSize
from ..types.next_page_token import NextPageToken
from ..types.sort_by_enum import SortByEnum
from ..types.sort_dir_enum import SortDirEnum
from .types.evaluation_set_create_response import EvaluationSetCreateResponse
from .types.evaluation_set_get_response import EvaluationSetGetResponse
from .types.evaluation_set_list_response import EvaluationSetListResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawEvaluationSetClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list(
        self,
        *,
        processor_id: typing.Optional[str] = None,
        sort_by: typing.Optional[SortByEnum] = None,
        sort_dir: typing.Optional[SortDirEnum] = None,
        next_page_token: typing.Optional[NextPageToken] = None,
        max_page_size: typing.Optional[MaxPageSize] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[EvaluationSetListResponse]:
        """
        List evaluation sets in your account. You can use the `processorId` parameter to filter evaluation sets by processor.

        This endpoint returns a paginated response. You can use the `nextPageToken` to fetch subsequent results.

        Parameters
        ----------
        processor_id : typing.Optional[str]
            The ID of the processor to filter evaluation sets by.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        sort_by : typing.Optional[SortByEnum]
            Sorts the evaluation sets by the given field.

        sort_dir : typing.Optional[SortDirEnum]
            Sorts the evaluation sets in ascending or descending order. Ascending order means the earliest evaluation set is returned first.

        next_page_token : typing.Optional[NextPageToken]

        max_page_size : typing.Optional[MaxPageSize]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[EvaluationSetListResponse]
            Successfully retrieved evaluation sets
        """
        _response = self._client_wrapper.httpx_client.request(
            "evaluation_sets",
            method="GET",
            params={
                "processorId": processor_id,
                "sortBy": sort_by,
                "sortDir": sort_dir,
                "nextPageToken": next_page_token,
                "maxPageSize": max_page_size,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetListResponse,
                    construct_type(
                        type_=EvaluationSetListResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def create(
        self, *, name: str, description: str, processor_id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[EvaluationSetCreateResponse]:
        """
        Evaluation sets are collections of files and expected outputs that are used to evaluate the performance of a given processor in Extend. This endpoint will create a new evaluation set in Extend, which items can be added to using the [Create Evaluation Set Item](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/create-evaluation-set-item) endpoint.

        Note: it is not necessary to create an evaluation set via API. You can also create an evaluation set via the Extend dashboard and take the ID from there.

        Parameters
        ----------
        name : str
            The name of the evaluation set.

            Example: `"Invoice Processing Test Set"`

        description : str
            A description of what this evaluation set is used for.

            Example: `"Q4 2023 vendor invoices"`

        processor_id : str
            The ID of the processor to create an evaluation set for. Evaluation sets can in theory be run against any processor, but it is required to associate the evaluation set with a primary processor.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[EvaluationSetCreateResponse]
            Successfully created evaluation set
        """
        _response = self._client_wrapper.httpx_client.request(
            "evaluation_sets",
            method="POST",
            json={
                "name": name,
                "description": description,
                "processorId": processor_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetCreateResponse,
                    construct_type(
                        type_=EvaluationSetCreateResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def get(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[EvaluationSetGetResponse]:
        """
        Retrieve a specific evaluation set by ID. This returns an evaluation set object, but does not include the items in the evaluation set. You can use the [List Evaluation Set Items](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/list-evaluation-set-items) endpoint to get the items in an evaluation set.

        Parameters
        ----------
        id : str
            The ID of the evaluation set to retrieve.

            Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[EvaluationSetGetResponse]
            Successfully retrieved evaluation set
        """
        _response = self._client_wrapper.httpx_client.request(
            f"evaluation_sets/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetGetResponse,
                    construct_type(
                        type_=EvaluationSetGetResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)


class AsyncRawEvaluationSetClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list(
        self,
        *,
        processor_id: typing.Optional[str] = None,
        sort_by: typing.Optional[SortByEnum] = None,
        sort_dir: typing.Optional[SortDirEnum] = None,
        next_page_token: typing.Optional[NextPageToken] = None,
        max_page_size: typing.Optional[MaxPageSize] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[EvaluationSetListResponse]:
        """
        List evaluation sets in your account. You can use the `processorId` parameter to filter evaluation sets by processor.

        This endpoint returns a paginated response. You can use the `nextPageToken` to fetch subsequent results.

        Parameters
        ----------
        processor_id : typing.Optional[str]
            The ID of the processor to filter evaluation sets by.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        sort_by : typing.Optional[SortByEnum]
            Sorts the evaluation sets by the given field.

        sort_dir : typing.Optional[SortDirEnum]
            Sorts the evaluation sets in ascending or descending order. Ascending order means the earliest evaluation set is returned first.

        next_page_token : typing.Optional[NextPageToken]

        max_page_size : typing.Optional[MaxPageSize]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[EvaluationSetListResponse]
            Successfully retrieved evaluation sets
        """
        _response = await self._client_wrapper.httpx_client.request(
            "evaluation_sets",
            method="GET",
            params={
                "processorId": processor_id,
                "sortBy": sort_by,
                "sortDir": sort_dir,
                "nextPageToken": next_page_token,
                "maxPageSize": max_page_size,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetListResponse,
                    construct_type(
                        type_=EvaluationSetListResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def create(
        self, *, name: str, description: str, processor_id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[EvaluationSetCreateResponse]:
        """
        Evaluation sets are collections of files and expected outputs that are used to evaluate the performance of a given processor in Extend. This endpoint will create a new evaluation set in Extend, which items can be added to using the [Create Evaluation Set Item](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/create-evaluation-set-item) endpoint.

        Note: it is not necessary to create an evaluation set via API. You can also create an evaluation set via the Extend dashboard and take the ID from there.

        Parameters
        ----------
        name : str
            The name of the evaluation set.

            Example: `"Invoice Processing Test Set"`

        description : str
            A description of what this evaluation set is used for.

            Example: `"Q4 2023 vendor invoices"`

        processor_id : str
            The ID of the processor to create an evaluation set for. Evaluation sets can in theory be run against any processor, but it is required to associate the evaluation set with a primary processor.

            Example: `"dp_Xj8mK2pL9nR4vT7qY5wZ"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[EvaluationSetCreateResponse]
            Successfully created evaluation set
        """
        _response = await self._client_wrapper.httpx_client.request(
            "evaluation_sets",
            method="POST",
            json={
                "name": name,
                "description": description,
                "processorId": processor_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetCreateResponse,
                    construct_type(
                        type_=EvaluationSetCreateResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def get(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[EvaluationSetGetResponse]:
        """
        Retrieve a specific evaluation set by ID. This returns an evaluation set object, but does not include the items in the evaluation set. You can use the [List Evaluation Set Items](https://docs.extend.ai/2025-04-21/developers/api-reference/evaluation-set-endpoints/list-evaluation-set-items) endpoint to get the items in an evaluation set.

        Parameters
        ----------
        id : str
            The ID of the evaluation set to retrieve.

            Example: `"ev_2LcgeY_mp2T5yPaEuq5Lw"`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[EvaluationSetGetResponse]
            Successfully retrieved evaluation set
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"evaluation_sets/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    EvaluationSetGetResponse,
                    construct_type(
                        type_=EvaluationSetGetResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        Error,
                        construct_type(
                            type_=Error,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)
