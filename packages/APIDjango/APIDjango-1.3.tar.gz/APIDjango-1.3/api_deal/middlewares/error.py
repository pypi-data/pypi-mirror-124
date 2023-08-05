from logging import getLogger
from django.utils.deprecation import MiddlewareMixin

from api_deal.error import SERVER_ERROR
from api_deal.res import ErrorReturn
default_log = getLogger("default")

class MyErrorMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if not hasattr(exception, "errmsg"):
            exception = SERVER_ERROR
            default_log.exception(exception)
        if hasattr(exception, "args") and isinstance(exception.args, tuple) and exception.args:
            errmsg_list = []
            if exception.errmsg:
                errmsg_list.append(exception.errmsg)
            errmsg_list.append(";".join(exception.args))
            exception.errmsg = ":".join(errmsg_list)
        return ErrorReturn(exception)
