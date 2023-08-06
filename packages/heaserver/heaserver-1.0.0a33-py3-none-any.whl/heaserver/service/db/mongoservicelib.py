import logging

from ..appproperty import HEA_DB
from .. import response
from ..heaobjectsupport import new_heaobject
from ..aiohttp import StreamReaderWrapper
from heaobject.error import DeserializeException
from aiohttp.web import Request, Response
from typing import Type, IO, Optional
from heaobject.root import HEAObject


async def get(request: Request, collection: str) -> Response:
    """
    Gets the HEA object with the specified id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :return: a Response with the requested HEA object or Not Found.
    """
    result = await request.app[HEA_DB].get(request, collection, var_parts='id')
    return await response.get(request, result)


async def get_content(request: Request, collection: str) -> Response:
    """
    Gets the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :return: a Response with the requested HEA object or Not Found.
    """
    out = await request.app[HEA_DB].get_content(request, collection, var_parts='id')
    if out is not None:
        return await response.get_streaming(request, StreamReaderWrapper(out), 'text/plain')
    else:
        return response.status_not_found()


async def get_by_name(request: Request, collection: str) -> Response:
    """
    Gets the HEA object with the specified name.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :return: a Response with the requested HEA object or Not Found.
    """
    result = await request.app[HEA_DB].get(request, collection, var_parts='name')
    return await response.get(request, result)


async def get_all(request: Request, collection: str) -> Response:
    """
    Gets all HEA objects.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :return: a Response with a list of HEA object dicts.
    """
    result = await request.app[HEA_DB].get_all(request, collection)
    return await response.get_all(request, result)


async def opener(request: Request, collection: str) -> Response:
    """
    Gets choices for opening an HEA desktop object's content.

    :param request: the HTTP request. Required. If an Accepts header is provided, MIME types that do not support links
    will be ignored.
    :param collection: the Mongo collection name. Required.
    :return: a Response object with status code 300, and a body containing the HEA desktop object and links
    representing possible choices for opening the HEA desktop object; or Not Found.
    """
    result = await request.app[HEA_DB].get(request, collection, var_parts='id')
    return await response.get_multiple_choices(request, result)


async def post(request: Request, collection: str, type_: Type[HEAObject], default_content: Optional[IO] = None) -> Response:
    """
    Posts the provided HEA object.

    :param request: the HTTP request.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param default_content: an optional blank document or other default content as a file-like object. This must be not-None
    for any microservices that manage content.
    :return: a Response object with a status of Created and the object's URI in the
    """
    try:
        obj = await new_heaobject(request, type_)
        result = await request.app[HEA_DB].post(request, obj, collection, default_content)
        return await response.post(request, result, collection)
    except DeserializeException:
        return response.status_bad_request()


async def put(request: Request, collection: str, type_: Type[HEAObject]) -> Response:
    """
    Updates the HEA object with the specified id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :return: a Response object with a status of No Content or Not Found.
    """
    try:
        obj = await new_heaobject(request, type_)
        if request.match_info['id'] != obj.id:
            return response.status_bad_request()
        result = await request.app[HEA_DB].put(request, obj, collection)
        return await response.put(result.matched_count if result else False)
    except DeserializeException:
        return response.status_bad_request()


async def put_content(request: Request, collection: str, type_: Type[HEAObject]) -> Response:
    """
    Updates the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :return: a Response object with a status of No Content or Not Found.
    """
    try:
        result = await request.app[HEA_DB].put_content(request, collection)
        return await response.put(result)
    except DeserializeException:
        return response.status_bad_request()


async def delete(request: Request, collection: str) -> Response:
    """
    Deletes the HEA object with the specified id and any associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :return: No Content or Not Found.
    """
    result = await request.app[HEA_DB].delete(request, collection)
    return await response.delete(result.deleted_count if result else False)
