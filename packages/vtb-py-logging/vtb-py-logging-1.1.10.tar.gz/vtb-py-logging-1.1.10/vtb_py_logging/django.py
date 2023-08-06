from vtb_py_logging.log_extra import push_extra
from vtb_py_logging.request_id import RequestId
from django.conf import settings


def request_id_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            request_id = RequestId.make(prefix=settings.REQUEST_ID_PREFIX)
        push_extra(request_id=request_id)
        return get_response(request)

    return middleware
