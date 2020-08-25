from unittest import TestCase
from uuid import uuid5, NAMESPACE_DNS
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import caches
from django.http.response import HttpResponse
from django.test import RequestFactory
from django.views.generic import View

from .middleware import DropDuplicatedRequests


CACHE_NAME = getattr(settings, "DUPLICATED_REQUESTS_CACHE_NAME", "default")
COOKIE_NAME = getattr(settings, "DUPLICATED_REQUESTS_COOKIE_NAME", "dj-request-id")


class TestDropDuplicatedRequests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DropDuplicatedRequests()

    def tearDown(self):
        cache = caches[CACHE_NAME]
        cache.clear()

    def _call_view_using_middleware(self, method, set_cookie=True, path="/", body={}):
        class TestView(View):
            def get(self, request):
                return HttpResponse()

            put = post = patch = delete = get

        # Get a new request and process it using middleware
        request = getattr(self.factory, method)(path, body)
        if set_cookie:
            request.COOKIES[COOKIE_NAME] = "not-so-unique-id"
        response = self.middleware.process_request(request)

        if response is None:
            response = TestView.as_view()(request)
        return self.middleware.process_response(request, response)

    def test_double_get(self):
        response_1 = self._call_view_using_middleware("get")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("get")
        self.assertEqual(response_2.status_code, 200)

    def test_double_post(self):
        response_1 = self._call_view_using_middleware("post", body={"a": "a"})
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("post", body={"a": "a"})
        self.assertEqual(response_2.status_code, 304)

    def test_double_post_without_cookie(self):
        response_1 = self._call_view_using_middleware("post", False)
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("post", False)
        self.assertEqual(response_2.status_code, 200)

    def test_double_put(self):
        response_1 = self._call_view_using_middleware("put")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put")
        self.assertEqual(response_2.status_code, 304)

    def test_double_patch(self):
        response_1 = self._call_view_using_middleware("patch")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("patch")
        self.assertEqual(response_2.status_code, 304)

    def test_double_delete(self):
        response_1 = self._call_view_using_middleware("delete")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("delete")
        self.assertEqual(response_2.status_code, 304)

    def test_double_requests_different_method(self):
        response_1 = self._call_view_using_middleware("patch")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put")
        self.assertEqual(response_2.status_code, 200)

    def test_double_requests_different_path(self):
        response_1 = self._call_view_using_middleware("put", path="/123")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", path="/456")
        self.assertEqual(response_2.status_code, 200)

    def test_double_requests_same_path(self):
        response_1 = self._call_view_using_middleware("put", path="/123")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", path="/123")
        self.assertEqual(response_2.status_code, 304)

    def test_double_requests_different_get_params(self):
        response_1 = self._call_view_using_middleware("put", path="/?a=123")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", path="/?a=456")
        self.assertEqual(response_2.status_code, 200)

    def test_double_requests_same_get_params(self):
        response_1 = self._call_view_using_middleware("put", path="/?a=123")
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", path="/?a=123")
        self.assertEqual(response_2.status_code, 304)

    def test_double_requests_different_body(self):
        response_1 = self._call_view_using_middleware("put", body={"a": "b"})
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", body={"a": "c"})
        self.assertEqual(response_2.status_code, 200)

    def test_double_requests_same_body(self):
        response_1 = self._call_view_using_middleware("put", body={"a": "b"})
        self.assertEqual(response_1.status_code, 200)
        response_2 = self._call_view_using_middleware("put", body={"a": "b"})
        self.assertEqual(response_2.status_code, 304)

    def test_set_cookie(self):
        response = self._call_view_using_middleware('get')
        self.assertIn(COOKIE_NAME, response.cookies)
