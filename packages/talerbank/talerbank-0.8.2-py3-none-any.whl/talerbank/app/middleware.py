import traceback
import logging
import zlib
from . import urls
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import BankAccount, BankTransaction
from .views import (
    DebitLimitException,
    SameAccountException,
    LoginFailed,
    UnhandledException,
    set_session_hint,
)

from .schemas import JSONFieldException, URLParamValidationError, InvalidSession

from taler.util.amount import CurrencyMismatchError, AmountFormatError
from taler.util.taler_error_codes import ErrorCode
from http import HTTPStatus

LOGGER = logging.getLogger()


##
# Class decompressing requests.
class DecompressionMiddleware:

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param get_response a Django-provided callable that calls
    #        whatever comes next in the chain: a further middleware
    #        or the view itself (please refer to the official
    #        documentation for more details).
    def __init__(self, get_response):
        self.get_response = get_response

    ##
    # This function is transparently invoked by Django when
    # a request traverses the chain made of middleware classes
    # and the view itself as the last element in the chain.
    #
    # Here happens the decompression.
    #
    # @param self this class.
    # @param request Django-specific request object (of the same
    #        type that is handed to views).
    # @return Django-specific response object.
    def __call__(self, request):
        if "deflate" == request.META.get("HTTP_CONTENT_ENCODING"):
            request._body = zlib.decompress(request.body)

        return self.get_response(request)


class ExceptionMiddleware:
    """
    Middleware for handling exceptions not caught directly
    by the application logic.
    """

    def __init__(self, get_response):
        """
        # Init constructor.
        #
        # @param self the object itself.
        # @param get_response a Django-provided callable that calls
        #        whatever comes next in the chain: a further middleware
        #        or the view itself (please refer to the official
        #        documentation for more details).
        """
        self.get_response = get_response

        # Map between endpoints and Web pages to render
        # after the exception gets managed.
        self.render = {
            reverse("profile", urlconf=urls): "profile",
            reverse("register", urlconf=urls): "index",
            reverse("public-accounts", urlconf=urls): "index",
        }

    def __call__(self, request):
        """
        This function is transparently invoked by Django when
        a request traverses the chain made of middleware classes
        and the view itself as the last element in the chain.
        """
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        Main logic for processing the exception.  It checks
        if the exception captured can be managed, and does it
        if so.  Otherwise, it lets the native handler operate.
        """
        LOGGER.error(f"Error: {exception}, while serving {request.get_full_path()}")

        if hasattr(exception, "taler_error_code"):
            render_to = self.render.get(request.path)
            if not render_to:
                response = JsonResponse(
                    dict(code=exception.taler_error_code.value, error=exception.hint),
                    status=exception.http_status_code,
                )
                response["Access-Control-Allow-Origin"] = "*"
                return response
            set_session_hint(request, success=False, hint=exception.hint)
            return redirect(render_to)
        else:
            LOGGER.error(f"Stack trace: {traceback.format_exc()}")
            return JsonResponse(
                dict(
                    code=ErrorCode.BANK_UNMANAGED_EXCEPTION,
                    hint="unexpected exception",
                    exception=str(exception),
                ),
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
