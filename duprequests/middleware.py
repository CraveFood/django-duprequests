from uuid import uuid4, uuid5, NAMESPACE_DNS
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import caches
from django.http.response import HttpResponseNotModified


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # pragma: nocover
    MiddlewareMixin = object

CACHE_NAME = getattr(settings, "DUPLICATED_REQUESTS_CACHE_NAME", "default")
CACHE_TIMEOUT = getattr(settings, "DUPLICATED_REQUESTS_CACHE_TIMEOUT", 5)
COOKIE_NAME = getattr(settings, "DUPLICATED_REQUESTS_COOKIE_NAME", "dj-request-id")
COOKIE_PREFIX = getattr(settings, "DUPLICATED_REQUESTS_COOKIE_PREFIX", "request-id-")


class DropDuplicatedRequests(MiddlewareMixin):
    """
    Middleware that drops requests made in quick succession.
    Uses Django's caching system to check/save each request.
    """

    def _get_request_hash(self, request):
        """
        Generates a unique key based on request path, method, body and arguments
        """
        hash_value = uuid5(
            NAMESPACE_DNS,
            request.path_info
            + "--"
            + request.method.lower()
            + "--"
            + urlencode(request.GET)
            + "--"
            + request.body.decode("utf-8"),
        ).node
        return str(hash_value)

    def process_request(self, request):
        """
        Stores a unique key per request in the cache, if it already exists, returns 304
        """
        if not request.method.lower() in ("post", "put", "delete", "patch"):
            return

        cookie_value = request.COOKIES.get(COOKIE_NAME)
        if not cookie_value:
            return

        cache_key = cookie_value + self._get_request_hash(request)

        cache = caches[CACHE_NAME]
        if cache_key in cache:
            return HttpResponseNotModified()
        cache.set(cache_key, True, CACHE_TIMEOUT)

    def process_response(self, request, response):
        """
        Sends a cookie with a unique hash to identify requests that are the same
        but from different sources
        """
        response.set_cookie(COOKIE_NAME, COOKIE_PREFIX + uuid4().hex)
        return response
