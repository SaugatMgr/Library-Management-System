from threading import local

_thread_locals = local()


def get_current_request():
    """
    Gets the current HttpRequest object from the thread local storage
    """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """
    Gets current user from the current request if there exists else None
    """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadMiddleware:
    """
    Adds the current HttpRequest object to thread local storage
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response
