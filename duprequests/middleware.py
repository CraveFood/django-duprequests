
from uuid import uuid4

from django.conf import settings
from django.core.cache import caches
from django.http.response import HttpResponseNotModified

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:   # pragma: nocover
    MiddlewareMixin = object

CACHE_NAME = getattr(settings, 'DUPLICATED_REQUESTS_CACHE_NAME', 'default')
CACHE_TIMEOUT = getattr(settings, 'DUPLICATED_REQUESTS_CACHE_TIMEOUT', 5)
COOKIE_NAME = getattr(settings, 'DUPLICATED_REQUESTS_COOKIE_NAME',
                      'dj-request-id')
COOKIE_PREFIX = getattr(settings, 'DUPLICATED_REQUESTS_COOKIE_PREFIX',
                        'request-id-')


class DropDuplicatedRequests(MiddlewareMixin):
    """Middleware that drops requests made in quick succession.

    Uses Django's caching system to check/save each request."""

    def process_request(self, request):
        if not request.method.lower() in ('post', 'put', 'delete', 'patch'):
            return

        cache_key = request.COOKIES.get(COOKIE_NAME)
        if not cache_key:
            return

        cache = caches[CACHE_NAME]
        if cache_key in cache:
            return HttpResponseNotModified()
        cache.set(cache_key, True, CACHE_TIMEOUT)

    def process_response(self, request, response):
        response.set_cookie(COOKIE_NAME, COOKIE_PREFIX + uuid4().hex)
        return response
