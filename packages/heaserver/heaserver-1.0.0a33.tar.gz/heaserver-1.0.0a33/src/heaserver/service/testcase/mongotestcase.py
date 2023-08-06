"""
Sets up a testing environment for testing HEA services, including mock modules and classes. To use this module, do the
following in order:
1) Import this module before importing anything else to insure that all mocks are are used in subsequently imported
modules.
2) Import the service to be tested.
3) Call the get_test_case_cls with the fixtures to use in the unit tests.
4) Create subclasses of the returned unit test class to implement actual test cases. The mixin module in this package
contains implementations of unit tests to run for testing GET, POST, PUT and DELETE. Add these mixins as superclasses
of your test cases.
"""

from aiohttp.test_utils import AioHTTPTestCase, TestServer
from aiohttp.web import Application
from copy import deepcopy
import pytest
import abc
from yarl import URL
from typing import Dict, Any, Union, Optional


class MongoTestCase(abc.ABC, AioHTTPTestCase):
    """
    Abstract test case class for testing a mongodb-based service.
    """

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def __init__(self, href: Union[URL, str],
                 wstl_package: str,
                 coll: str,
                 body_post: Optional[Dict[str, Dict[str, Any]]] = None,
                 body_put: Optional[Dict[str, Dict[str, Any]]] = None,
                 expected_all: Optional[Dict[str, Any]] = None,
                 expected_one: Optional[Dict[str, Any]] = None,
                 expected_one_wstl: Optional[Dict[str, Any]] = None,
                 expected_all_wstl: Optional[Dict[str, Any]] = None,
                 expected_one_duplicate_form: Optional[Dict[str, Any]] = None,
                 expected_opener: Optional[Union[str, URL]] = None,
                 expected_opener_body: Optional[Dict[str, Any]] = None,
                 content: Optional[Dict[str, Dict[str, bytes]]] = None,
                 content_type: Optional[str] = None,
                 methodName: str = 'runTest',
                 port: Optional[int] = None) -> None:
        """
        Initializes a test case.

        :param href: the resource being tested. Required.
        :param wstl_package: the name of the package containing the wstl data package. Required.
        :param coll: the MongoDB collection (required).
        :param body_post: JSON dict for data to be posted.
        :param body_put: JSON dict for data to be put. If None, the value of body_post will be used for PUTs.
        :param expected_all: The expected JSON dict for GET-all calls.
        :param expected_one: The expected JSON dict for GET calls. If None, the value of expected_all will be used.
        :param expected_one_wstl: The expected JSON dict for GET calls that return the
        application/vnd.wstl+json mime type.
        :param expected_all_wstl: The expected JSON dict for GET-all calls that return the
        application/vnd.wstl+json mime type.
        :param expected_one_duplicate_form: The expected JSON dict for GET calls that return the
        object's duplicate form.
        :param expected_opener: The expected URL of the resource that does the opening.
        :param expected_opener_body: The expected JSON dict for GET calls for an HEA desktop object's opener choices.
        :param content: data to insert into GridFS (optional), as a collection string -> HEA Object id -> content as a
        bytes, bytearray, or array.array object.
        :param content_type: the MIME type of the content (optional).
        :param methodName: the name of the method to test.
        :param port: the port number to run aiohttp. If None, a random available port will be chosen.
        """
        super().__init__(methodName=methodName)
        self._coll = coll
        self._href = URL(href)
        self._body_post = body_post
        self._body_put = body_put
        self._expected_all = expected_all
        self._expected_one = expected_one
        self._expected_one_wstl = expected_one_wstl
        self._expected_all_wstl = expected_all_wstl
        self._expected_one_duplicate_form = expected_one_duplicate_form
        self._expected_opener = expected_opener
        self._expected_opener_body = expected_opener_body
        self._wstl_package = wstl_package
        self._content = deepcopy(content)
        self._content_type = content_type
        self.maxDiff = None
        self.__port = port

    @abc.abstractmethod
    async def get_application(self) -> Application:
        pass

    async def get_server(self, app: Application) -> TestServer:
        """
        Overrides this method to allow setting a fixed port for running aiohttp. If no port was specified in the
        constructor, a random port will be selected.

        :param app: the aiohttp application.
        :return: a new aiohttp TestServer instance.
        """
        if self.__port:
            return TestServer(app, port=self.__port)
        else:
            return TestServer(app)
