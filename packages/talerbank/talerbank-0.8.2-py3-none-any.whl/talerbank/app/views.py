##
# This file is part of TALER
# (C) 2014, 2015, 2016, 2020 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version. TALER is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
#  You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>
#
#  @author Marcello Stanisci
#  @author Florian Dold

from functools import wraps
import math
import json
import logging
import hashlib
import random
import re
import time
import base64
import uuid
from urllib.parse import urlparse, parse_qsl
import django.contrib.auth
import django.contrib.auth.views
import django.contrib.auth.forms
from django.db import transaction
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.translation import gettext
from django.views.decorators.http import require_http_methods
from django.urls import reverse, get_script_prefix
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .models import BankAccount, BankTransaction, TalerWithdrawOperation
from taler.util.amount import Amount, SignedAmount
from taler.util.payto import PaytoParse
from taler.util.taler_error_codes import ErrorCode
from http import HTTPStatus

import qrcode
import qrcode.image.svg
import lxml
from .schemas import (
    HistoryParams,
    URLParamValidationError,
    AddIncomingData,
    JSONFieldException,
    InvalidSession,
    WithdrawHeadless,
    WithdrawHeadlessUri,
)

LOGGER = logging.getLogger(__name__)

##
# Constant value for the biggest number the bank handles.
# This value is just equal to the biggest number that JavaScript
# can handle (because of the wallet).
UINT64_MAX = (2 ** 64) - 1

##
# Decorator function that authenticates requests by fetching
# the credentials over the HTTP requests headers.
#
# @param view_func function that will be called after the
#        authentication, and that will usually serve the requested
#        endpoint.
# @return FIXME.
def login_via_headers(view_func):
    def _decorator(request, *args, **kwargs):
        user_account = basic_auth(request)
        if not user_account:
            raise LoginFailed("authentication failed")
        return view_func(request, user_account, *args, **kwargs)

    return wraps(view_func)(_decorator)


def allow_origin_star(view_func):
    def _decorator(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    return wraps(view_func)(_decorator)

##
# Exception raised upon failing login.
#
class LoginFailed(Exception):
    def __init__(self, msg):
        super(LoginFailed, self).__init__(msg)
        self.hint = "Wrong password given"
        self.http_status_code = HTTPStatus.UNAUTHORIZED
        self.taler_error_code = ErrorCode.BANK_LOGIN_FAILED


class InvalidInputData(Exception):
    def __init__(self, msg):
        super(InvalidInputData, self).__init__(msg)
        self.hint = msg  # should mention the picked username
        self.http_status_code = HTTPStatus.BAD_REQUEST
        self.taler_error_code = ErrorCode.BANK_SOFT_EXCEPTION


class UsernameUnavailable(Exception):
    def __init__(self, msg):
        super(UsernameUnavailable, self).__init__(msg)
        self.hint = msg  # should mention the picked username
        self.http_status_code = HTTPStatus.NOT_ACCEPTABLE
        self.taler_error_code = ErrorCode.BANK_SOFT_EXCEPTION


##
# Exception raised when the public history from
# a ordinary user account is tried to be accessed.
class PrivateAccountException(Exception):
    def __init__(self, msg):
        super(PrivateAccountException, self).__init__(msg)
        self.hint = "Cannot show history from private persons accounts"
        self.http_status_code = HTTPStatus.FORBIDDEN


##
# Exception raised when some financial operation goes
# beyond the limit threshold.
class DebitLimitException(Exception):
    def __init__(self, msg):
        super(DebitLimitException, self).__init__(msg)
        self.hint = "Payment aborted for insufficient credit"
        self.http_status_code = HTTPStatus.FORBIDDEN
        self.taler_error_code = ErrorCode.BANK_UNALLOWED_DEBIT


##
# Exception raised when some financial operation is
# attempted and both parties are the same account number.
#
class SameAccountException(Exception):
    def __init__(self, msg):
        super(SameAccountException, self).__init__(msg)
        self.hint = "Cannot send payment to oneself."
        self.http_status_code = HTTPStatus.BAD_REQUEST
        self.taler_error_code = ErrorCode.BANK_SAME_ACCOUNT


class UnhandledException(Exception):
    def __init__(self, msg="Unhandled exception happened!"):
        super(UnhandledException, self).__init__(msg)
        self.hint = msg
        self.http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.taler_error_code = ErrorCode.BANK_UNMANAGED_EXCEPTION


##
# The authentication for users to log in the bank.
#
class TalerAuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autofocus"] = True
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"


##
# Return a empty response.  Used in "/favicon.ico" requests.
#
def ignore(request):
    del request
    return HttpResponse()


##
# Decode body, when it is expected to be UTF-8.
#
# @param request the HTTP request being served.
# @return the body as string.
def decode_body(request):
    return request.body.decode("utf-8")


##
# Get a flag from the session and clear it.
#
# @param request the HTTP request being served.
# @param name name of the session value that should be retrieved.
# @return the value, if found; otherwise False.
def get_session_flag(request, name):
    if name in request.session:
        ret = request.session[name]
        del request.session[name]
        return ret
    return False


##
# A session "hint" is a tuple indicating whether the
# message is for a failure or a success, and containing
# the message itself.
#
# @param request the HTTP request being served.
# @param name hint name
# @return the hint (a "null" one if none was found)
def get_session_hint(request):
    ret = True, ""
    if "hint" in request.session:
        ret = request.session["hint"]
        del request.session["hint"]
    return ret


def set_session_hint(request, success, hint):
    if "hint" in request.session:
        LOGGER.warning("Overriding a non consumed hint")
        del request.session["hint"]
    request.session["hint"] = success, hint


##
# Build the list containing all the predefined accounts; the
# list contains, for example, the exchange, the bank itself, and
# all the public accounts (like GNUnet / Tor / FSF / ..)
def predefined_accounts_list():
    account = 2
    ret = []
    for i in settings.TALER_PREDEFINED_ACCOUNTS[1:]:
        ret.append((account, "%s (#%d)" % (i, account)))
        account += 1
    return ret


##
# Thanks to [1], this class provides a dropdown menu that
# can be used within a <select> element, in a <form>.
# [1] https://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option
class InputDatalist(forms.TextInput):

    ##
    # Constructor function.
    #
    # @param self the object itself.
    # @param datalist a list of admitted values.
    # @param name the name of the value that will be sent
    #        along the POST.
    # @param args positional arguments
    # @param kwargs keyword arguments
    # @return the object
    def __init__(self, datalist, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._datalist = datalist()
        self.attrs.update({"list": "%slist" % name, "pattern": "[1-9]+[0-9]*"})

    ##
    # Method that produces the final HTML from the object itself.
    #
    # @param self the object itself
    # @param name the name of the value that will be sent
    #        along the POST
    # @param value value to be sent along the @a name.
    # @param attrs a dict indicating which HTML attribtues should
    #        be defined in the rendered element.
    # @param renderer render engine (left as None, typically); it
    #        is a class that respects the low-level render API from
    #        Django, see [2]
    # [2] https://docs.djangoproject.com/en/2.1/ref/forms/renderers/#low-level-widget-render-api
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        datalist = '<datalist id="%slist">' % self._name
        for dl_value, dl_text in self._datalist:
            datalist += '<option value="%s">%s</option>' % (dl_value, dl_text)
        datalist += "</datalist>"
        return html + datalist


class PaytoTransferForm(forms.Form):
    address = forms.CharField()


@login_required
def wiretransfer_form(request):
    if request.method == "GET":
        is_success, hint = get_session_hint(request)
        context = dict(
            currency=request.user.bankaccount.balance.amount.currency,
            is_success=is_success,
            hint=hint,
        )
        return render(request, "wiretransfer.html", context)

    # A payment was submitted. 
    try:
        amount = Amount.parse(
            "{}:{}".format(request.POST.get("currency"), request.POST.get("amount")
        ))
    except Exception:
        set_session_hint(request, success=False, hint="Wrong amount specified.")
        return redirect("wiretransfer-form")
    try:
        receiver_user = User.objects.get(username=request.POST.get("receiver"))
    except User.DoesNotExist:
        set_session_hint(request, success=False, hint="Money receiver was not found")
        return redirect("wiretransfer-form")

    try:
        wire_transfer(
            amount,
            request.user.bankaccount,
            receiver_user.bankaccount,
            request.POST.get("subject", "not given")
        )
    except Exception as exception:
        hint = str(exception)
        if hasattr(exception, "hint"):
            hint = exception.hint
        set_session_hint(request, success=False, hint=hint)
        return redirect("wiretransfer-form")

    set_session_hint(request, success=True, hint=gettext("Wire transfer successful!"))
    return redirect("profile")

@login_required
def payto_form(request):
    is_success, hint = get_session_hint(request)
    context = dict(
        currency=request.user.bankaccount.balance.amount.currency,
        is_success=is_success,
        hint=hint,
    )
    return render(request, "payto_wiretransfer.html", context)


##
# This method serves the profile page, which is the main
# page where the user interacts with the bank, and also the
# page that the user gets after a successful login.  It has
# to handle the following cases: (1) the user requests the
# profile page after haing POSTed a wire transfer request.
# (2) The user requests the page after having withdrawn coins,
# that means that a wire transfer has been issued to the exchange.
# In this latter case, the method has to notify the wallet about
# the operation outcome.  (3) Ordinary GET case, where the
# straight page should be returned.
#
# @param request Django-specific HTTP request object.
# @return Django-specific HTTP response object.
@login_required
def profile_page(request):
    is_success, hint = get_session_hint(request)
    context = dict(
        name=request.user.username,
        balance=request.user.bankaccount.balance,
        is_success=is_success,
        hint=hint,
        precision=settings.TALER_DIGITS,
        currency=request.user.bankaccount.balance.amount.currency,
        account_no=request.user.bankaccount.account_no,
        history=extract_history(request.user.bankaccount, -1 * (UINT64_MAX / 2 / 2)),
    )
    if settings.TALER_SUGGESTED_EXCHANGE:
        context["suggested_exchange"] = settings.TALER_SUGGESTED_EXCHANGE

    response = render(request, "profile_page.html", context)
    if "just_withdrawn" in request.session:
        del request.session["just_withdrawn"]
        response["Taler"] = "taler://notify-reserve/"
        response.status_code = HTTPStatus.ACCEPTED
    return response


@login_required
@require_POST
def payto_transfer(request):
    data = PaytoTransferForm(request.POST)
    if not data.is_valid():
        set_session_hint(request, success=False, hint=gettext("Bad form submitted!"))
        return redirect("profile")

    parsed_address = PaytoParse(data.cleaned_data.get("address"))

    try:
        receiver_user = User.objects.get(username=parsed_address.target)
    except User.DoesNotExist:
        set_session_hint(request, success=False, hint="Money receiver was not found")
        return redirect("payto-form")

    wire_transfer(
        parsed_address.amount,
        BankAccount.objects.get(user=request.user),
        BankAccount.objects.get(user=receiver_user),
        parsed_address.message,
    )
    set_session_hint(request, success=True, hint=gettext("Wire transfer successful!"))
    return redirect("profile")


##
# Helper function that hashes its input.  Usually
# used to hash the response to the math CAPTCHA.
#
# @param answer the plain text answer to hash.
# @return the hashed version of @a answer.
def hash_answer(answer):
    hasher = hashlib.new("sha1")
    hasher.update(settings.SECRET_KEY.encode("utf-8"))
    hasher.update(answer.encode("utf-8"))
    return hasher.hexdigest()


##
# Helper function that makes CAPTCHA's question and
# answer pair.
#
# @return the question and (hashed) answer pair.
def make_question():
    num1 = random.randint(1, 10)
    operand = random.choice(("*", "+", "-"))
    num2 = random.randint(1, 10)
    if operand == "*":
        answer = str(num1 * num2)
    elif operand == "-":
        # ensure result is positive
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = str(num1 - num2)
    else:
        answer = str(num1 + num2)
    question = "{} {} {}".format(num1, operand, num2)
    return question, hash_answer(answer)


def get_acct_from_payto(uri_str: str) -> str:
    wire_uri = urlparse(uri_str)
    if wire_uri.scheme != "payto":
        raise Exception("Bad Payto URI: '%s'" % uri_str)
    return wire_uri.path.split("/")[-1]


def get_subject_from_payto(uri_str: str) -> str:
    wire_uri = urlparse(uri_str)
    if wire_uri.scheme != "payto":
        raise Exception("Bad Payto URI: '%s'" % uri_str)
    params = parse_qs(wire_uri.query)
    subject = params.get("subject")
    if not subject:
        raise Exception("Subject not found in Payto URI: '%s'" % uri_str)
    return subject


##
# Class representing the registration form.
class UserReg(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


def internal_register(username, password):
    if not settings.ALLOW_REGISTRATIONS:
        raise Exception("registration not allowed!")

    if User.objects.filter(username=username).exists():
        raise UsernameUnavailable(f"Username {username} is unavailable")

    # Registration goes through.
    with transaction.atomic():
        bank_internal_account = BankAccount.objects.get(account_no=1)

        user = User.objects.create_user(username=username, password=password)
        user_account = BankAccount(user=user)
        user_account.save()

        # Give the user their joining bonus
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 100, 0),
            bank_internal_account,
            user_account,
            "Joining bonus",
        )

    return user


@require_POST
@csrf_exempt
def register_headless(request):
    """
    This method serves the request for programmatically
    registering a user.
    """
    if not settings.ALLOW_REGISTRATIONS:
        return JsonResponse(
            dict(error="registrations are not allowed"), status=HTTPStatus.FORBIDDEN
        )
    username = expect_json_body_str(request, "username")
    password = expect_json_body_str(request, "password")
    try:
        internal_register(username, password)
    except UsernameUnavailable:
        return JsonResponse(
            dict(hint="username unavailable"), status=HTTPStatus.CONFLICT
        )
    except InvalidInputData:
        return HttpResponse(status=HTTPStatus.NOT_ACCEPTABLE)  # WTF? BAD REQUEST?

    return HttpResponse(status=HTTPStatus.OK)


def register(request):
    """
    This method serves the request for registering a user.
    If successful, it redirects the user to their profile page;
    otherwise it will show again the same form (currently, without
    displaying _any_ error/warning message.)
    """
    if not settings.ALLOW_REGISTRATIONS:
        # FIXME: shouldn't be JSON!
        return JsonResponse(
            dict(error="registrations are not allowed"), status=HTTPStatus.FORBIDDEN
        )
    if request.method != "POST":
        return render(request, "register.html")

    # Process POST.

    try:
        input_data = UserReg(request.POST)
        if not input_data.is_valid():
            msg = "Wrong field(s): %s." % ", ".join(input_data.errors.keys())
            raise InvalidInputData(msg)
        username = input_data.cleaned_data["username"]
        password = input_data.cleaned_data["password"]
        user = internal_register(username, password)
    except UsernameUnavailable as e:
        return render(request, "register.html", {"not_available": True})
    except InvalidInputData as e:
        return render(
            request,
            "register.html",
            {
                "wrong": True,
                "hint": gettext("Username or password were incorrect!"),
            },
        )

    except DebitLimitException as e:
        return render(
            request,
            "register.html",
            {"wrong": True, "hint": "Out of business, cannot admit new customers."},
        )

    set_session_hint(request, success=True, hint=gettext("Registration successful!"))

    django.contrib.auth.login(request, user)
    return redirect("profile")


##
# Logs the user out, redirecting it to the bank's homepage.
#
# @param request Django-specific HTTP request object.
# @return Django-specific HTTP response object.
def logout_view(request):
    django.contrib.auth.logout(request)
    return redirect("index")


@require_GET
def config_view(request):
    """
    Config query of the taler bank access api
    """
    return JsonResponse(
        dict(
            version="0:0:0", currency=settings.TALER_CURRENCY, name="taler-bank-access"
        ),
        status=HTTPStatus.OK,
    )


@require_GET
@allow_origin_star
def api_config(request):
    """
    Config query of the taler bank integration api
    """
    return JsonResponse(
        dict(
            version="0:0:0",
            currency=settings.TALER_CURRENCY,
            name="taler-bank-integration",
        ),
        status=HTTPStatus.OK,
    )


def extract_history(account, delta, start=None):
    history = []
    qs = query_history(account, "both", delta, start)
    for item in qs:
        if item.credit_account == account:
            counterpart = item.debit_account
            sign = ""
        else:
            counterpart = item.credit_account
            sign = "-"
        entry = dict(
            row_id=item.id,
            cancelled=item.cancelled,
            sign=sign,
            amount=item.amount.stringify(settings.TALER_DIGITS, pretty=True),
            counterpart=counterpart.account_no,
            counterpart_username=counterpart.user.username,
            subject=item.subject,
            date=item.date.strftime("%d/%m/%y %H:%M %z"),
        )
        history.append(entry)
    return history


##
# Serve the page showing histories from publicly visible accounts.
#
# @param request Django-specific HTTP request object.
# @param name name of the public account to show.
# @param page given that public histories are paginated, this
#        value is the page number to display in the response.
# @return Django-specific HTTP response object.
def serve_public_accounts(request, name=None, page=None):
    try:
        page = abs(int(page))
        if page == 0:
            raise Exception
    except Exception:
        page = 1

    if not name:
        name = settings.TALER_PREDEFINED_ACCOUNTS[0]
    user = User.objects.get(username=name)
    if not user.bankaccount.is_public:
        raise PrivateAccountException(
            "Can't display public history for private account"
        )

    # How many records does a user have.
    num_records = query_history(
        user.bankaccount,
        "both",
        # Note: the parameter below is used for slicing arrays
        # and django/python is not allowing slicing with big numbers.
        UINT64_MAX / 2 / 2,
        0,
    ).count()
    DELTA = 30
    # '//' operator is NO floating point.
    num_pages = max(num_records // DELTA, 1)

    public_accounts = BankAccount.objects.filter(is_public=True)

    # Retrieve DELTA records younger than 'start_row' (included).
    history = extract_history(user.bankaccount, DELTA * page, 0)[
        DELTA * (page - 1) : (DELTA * page)
    ]

    pages = list(range(1, num_pages + 1))

    is_success, hint = get_session_hint(request)
    context = dict(
        is_success=is_success,
        hint=hint,
        current_page=page,
        back=page - 1 if page > 1 else None,
        forth=page + 1 if page < num_pages else None,
        public_accounts=public_accounts,
        selected_account=dict(
            name=name,
            number=user.bankaccount.account_no,
            history=history,
        ),
        pages=pages,
    )
    return render(request, "public_accounts.html", context)


##
# Build the DB query switch based on the "direction" history
# argument given by the user.
#
# @param bank_account bank account of the user requesting history.
# @param direction the "direction" URL parameter given by the user.
#        Note: this values got sanity-checked before this function
#        is called.
def direction_switch(bank_account, direction):
    direction_switch = {
        "both": (Q(debit_account=bank_account) | Q(credit_account=bank_account)),
        "credit": Q(credit_account=bank_account),
        "debit": Q(debit_account=bank_account),
        "cancel+": (Q(credit_account=bank_account) & Q(cancelled=True)),
        "cancel-": (Q(debit_account=bank_account) & Q(cancelled=True)),
    }
    return direction_switch.get(direction)


##
# Main routine querying for histories.
#
# @param bank_account the bank account object whose
#        history is being extracted.
# @param direction takes the following three values,
#        * debit: only entries where the querying user has _paid_
#                 will be returned.
#        * credit: only entries where the querying user _got_
#                  paid will be returned.
#        * both: both of the cases above will be returned.
#        * cancel+: only entries where the querying user cancelled
#                   the _receiving_ of money will be returned.
#        * cancel-: only entries where the querying user cancelled
#                   the _paying_ of money will be returned.
# @param delta how many history entries will be contained in the
#        array.
# @param start any history will be searched starting from this
#        value (which is a row ID), and going to the past or to
#        the future (depending on the user choice).  However, this
#        value itself will not be included in the history.
# @param sign this value ("+"/"-") determines whether the history
#        entries will be younger / older than @a start.
# @param ordering "descending" or anything else (for "ascending").
def query_history(bank_account, direction, delta, start):
    if start is None:
        if delta > 0:
            start = -1
        else:
            start = UINT64_MAX
    if delta < 0:
        sign_filter = Q(id__lt=start)
    else:
        sign_filter = Q(id__gt=start)

    qs = BankTransaction.objects.filter(
        direction_switch(bank_account, direction), sign_filter
    )
    order = "id" if (delta > 0) else "-id"
    return qs.order_by(order)[: abs(delta)]


##
# Build response object for /history.
#
# @param qs the query set for a history request.
# @param cancelled controls whether we omit/show
#        cancelled transactions.
# @param user_account bank account of the user who
#        asked for the history.
# @return the history object as specified in the
#         API reference documentation.
def build_history_response(qs, cancelled, user_account):
    history = []
    for entry in qs:
        counterpart = entry.credit_account.account_no
        sign_ = "-"
        if entry.cancelled and cancelled == "omit":
            continue
        if entry.credit_account.account_no == user_account.bankaccount.account_no:
            counterpart = entry.debit_account.account_no
            sign_ = "+"
        cancel = "cancel" if entry.cancelled else ""
        sign_ = cancel + sign_
        history.append(
            dict(
                counterpart=counterpart,
                amount=entry.amount.stringify(),
                sign=sign_,
                wt_subject=entry.subject,
                row_id=entry.id,
                date=dict(t_ms=int(entry.date.timestamp()) * 1000),
            )
        )
    return history


##
# Serve a request of /history.
#
# @param request Django-specific HTTP request.
# @param user_account the account whose history should be gotten.
# @return Django-specific HTTP response object.
@require_GET
@login_via_headers
def serve_history(request, user_account):
    args = HistoryParams(request.GET.dict())
    qs = query_history(
        user_account.bankaccount,
        args.get("direction"),
        args.get("delta"),
        args.get("start", None),
    )

    history = build_history_response(qs, args.get("cancelled", "show"), user_account)

    return JsonResponse(dict(data=history), status=HTTPStatus.OK)


def expect_json_body_str(request, param_name):
    body = json.loads(request.body)  # FIXME: cache!
    val = body.get(param_name)
    if not isinstance(val, str):
        # FIXME: throw right exception to be handled by middleware
        raise Exception(f"expected string for {param_name}")
    return val


def expect_json_body_amount(request, param_name):
    body = json.loads(request.body)  # FIXME: cache!
    val = body.get(param_name)
    if not isinstance(val, str):
        # FIXME: throw right exception to be handled by middleware
        raise Exception(f"expected string for {param_name}")
    return Amount.parse(val)


def expect_param_str(request, param_name):
    val = request.GET[param_name]
    if not isinstance(val, str):
        # FIXME: throw right exception to be handled by middleware
        raise Exception(f"expected string for {param_name}")
    return val


def expect_param_amount(request, param_name):
    val = request.GET[param_name]
    if not isinstance(val, str):
        # FIXME: throw right exception to be handled by middleware
        raise Exception(f"expected string for {param_name}")
    return Amount.parse(val)


@require_GET
def twg_base(request, acct_id):
    """
    This endpoint is used by the exchange test cases to
    check if the account is up, should not normally be used
    for anything else.
    """
    return JsonResponse(dict(), status=HTTPStatus.OK)


@require_GET
def twg_config(request, acct_id):
    """
    This endpoint is used by the exchange test cases to
    check if the account is up, should not normally be used
    for anything else.
    """
    return JsonResponse(
        dict(
            version="0:0:0",
            name="taler-wire-gateway",
            currency=settings.TALER_CURRENCY,
        ),
        status=HTTPStatus.OK,
    )


@csrf_exempt
@require_POST
@login_via_headers
def twg_add_incoming(request, user_account, acct_id):
    """
    Transfer money from a user's bank account to the exchange
    for testing purposes.
    """
    exchange_account = user_account.bankaccount

    if acct_id != user_account.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )

    reserve_pub = expect_json_body_str(request, "reserve_pub")
    debit_account_payto = expect_json_body_str(request, "debit_account")
    amount = expect_json_body_amount(request, "amount")

    debit_account_name = get_acct_from_payto(debit_account_payto)
    LOGGER.info(
        f"adding incoming balance to exchange ({acct_id}) from account {debit_account_payto} ({debit_account_name})"
    )
    debit_user = User.objects.get(username=debit_account_name)
    debit_account = BankAccount.objects.get(user=debit_user)
    subject = f"{reserve_pub}"

    # check if currency is acceptable
    if amount.currency != settings.TALER_CURRENCY:
        return JsonResponse(
            {
                "code": 30, # TALER_EC_BANK_DUPLICATE_RESERVE_PUB_SUBJECT
                "hint": "The specified currency is not supported."
            },
            status=HTTPStatus.CONFLICT
        )

    # check if reserve pub exists already.
    try:
        BankTransaction.objects.get(subject=subject)

    except BankTransaction.DoesNotExist:

        wtrans = wire_transfer(
            amount,
            debit_account,
            exchange_account,
            subject)

        return JsonResponse(
            {
                "row_id": wtrans.id,
                "timestamp": dict(t_ms=(int(wtrans.date.timestamp()) * 1000)),
            }
        )
    # Here means this public key was used already: must fail.
    return JsonResponse(
        {
            "code": 5114, # TALER_EC_BANK_DUPLICATE_RESERVE_PUB_SUBJECT
            "hint": "The reserve public cannot be used multiple times."
        },
        status=HTTPStatus.CONFLICT
    )

@csrf_exempt
@require_POST
@login_via_headers
def twg_transfer(request, user_account, acct_id):
    """
    Transfer money from the exchange to a merchant account.
    """

    exchange_account = user_account.bankaccount

    if acct_id != user_account.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )

    request_uid = expect_json_body_str(request, "request_uid")
    wtid = expect_json_body_str(request, "wtid")
    amount = expect_json_body_amount(request, "amount")
    exchange_base_url = expect_json_body_str(request, "exchange_base_url")
    credit_account_payto = expect_json_body_str(request, "credit_account")

    credit_account_name = get_acct_from_payto(credit_account_payto)
    try:
        credit_user = User.objects.get(username=credit_account_name)
    except User.DoesNotExist:
        LOGGER.error(f"credit account '{credit_account_name}' does not exist")
        # FIXME: use EC from taler-util library
        return JsonResponse(
            dict(
                code=ErrorCode.BANK_UNKNOWN_ACCOUNT,
                error="credit account does not exist",
            ),
            status=404,
        )
    credit_account = BankAccount.objects.get(user=credit_user)

    subject = f"{wtid} {exchange_base_url}"

    wtrans = wire_transfer(
        amount, exchange_account, credit_account, subject, request_uid
    )

    return JsonResponse(
        {
            "row_id": wtrans.id,
            "timestamp": dict(t_ms=(int(wtrans.date.timestamp()) * 1000)),
        }
    )


def get_plain_host(request):
    h = request.META.get("HTTP_HOST", "localhost")
    # remove port
    return h.split(":")[0]


def get_payto_from_account(request, acct):
    h = get_plain_host(request)
    return f"payto://x-taler-bank/{h}/{acct.user.username}"


def get_reserve_pub(subject):
    # obey to regex: \\b[a-z0-9A-Z]{52}\\b
    regex = re.compile(r"\b[a-z0-9A-Z]{52}\b")
    ret = regex.search(subject)
    if ret:
        return ret.group(0)
    return None


@require_GET
@login_via_headers
def twg_history_incoming(request, user_account, acct_id):
    history = []
    delta = int(request.GET["delta"])
    start_str = request.GET.get("start")
    if start_str is None:
        start = None
    else:
        start = int(start_str)
    qs = query_history(
        user_account.bankaccount,
        "credit",
        delta,
        start,
    )
    for item in qs:
        rp = get_reserve_pub(item.subject)
        if rp is None:
            continue
        history.append(
            dict(
                row_id=item.id,
                amount=item.amount.stringify(settings.TALER_DIGITS),
                date=dict(t_ms=(int(item.date.timestamp()) * 1000)),
                reserve_pub=rp,
                credit_account=get_payto_from_account(request, item.credit_account),
                debit_account=get_payto_from_account(request, item.debit_account),
            )
        )
    return JsonResponse(dict(incoming_transactions=history), status=HTTPStatus.OK)


@require_GET
@login_via_headers
def twg_history_outgoing(request, user_account, acct_id):
    history = []
    delta = int(request.GET["delta"])
    start_str = request.GET.get("start")
    if start_str is None:
        start = None
    else:
        start = int(start_str)
    qs = query_history(
        user_account.bankaccount,
        "debit",
        delta,
        start,
    )
    for item in qs:
        # FIXME: proper parsing, more structure in subject
        wtid, exchange_base_url = item.subject.split(" ")
        history.append(
            dict(
                row_id=item.id,
                amount=item.amount.stringify(settings.TALER_DIGITS),
                date=dict(t_ms=(int(item.date.timestamp()) * 1000)),
                wtid=wtid,
                exchange_base_url=exchange_base_url,
                credit_account=get_payto_from_account(request, item.credit_account),
                debit_account=get_payto_from_account(request, item.debit_account),
            )
        )
    return JsonResponse(dict(outgoing_transactions=history), status=HTTPStatus.OK)


##
# Implements the HTTP basic auth schema.
#
# @param request Django-specific HTTP request object.
# @return Django-specific "authentication object".
def basic_auth(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")

    if not auth_header:
        raise LoginFailed("missing Authorization header")

    tokens = auth_header.split(" ")
    if len(tokens) != 2:
        raise LoginFailed("invalid Authorization header")

    # decode the base64 content.
    if tokens[0] != "Basic":
        raise LoginFailed("Not supporting '%s' authorization method" % tokens[0])

    username, password = base64.b64decode(tokens[1]).decode("utf-8").split(":")
    return django.contrib.auth.authenticate(username=username, password=password)


def make_taler_withdraw_uri(request, withdraw_id):
    if request.is_secure():
        proto_extra = ""
    else:
        proto_extra = "+http"
    pfx = get_script_prefix().strip("/")
    if len(pfx) == 0:
        pfx_components = []
    else:
        pfx_components = pfx.split("/")
    host = request.get_host()
    p = "/".join([host] + pfx_components + ["api"] + [str(withdraw_id)])
    return f"taler{proto_extra}://withdraw/{p}"


@login_via_headers
@csrf_exempt
@require_POST
def withdraw_headless(request, user):
    """
    Serves a headless withdrawal request for the Taler protocol.
    """
    data = WithdrawHeadless(json.loads(decode_body(request)))
    h = get_plain_host(request)
    sender_payto = f"payto://x-taler-bank/{h}/{user.username}"
    ret_obj = {"sender_wire_details": sender_payto}

    exchange_payto = data.get("exchange_payto_uri")
    if not exchange_payto:
        return JsonResponse(
            dict(hint="exchange_payto_uri missig"), status=HTTPStatus.BAD_REQUEST
        )
    exchange_account_name = get_acct_from_payto(exchange_payto)
    try:
        exchange_user = User.objects.get(username=exchange_account_name)
    except User.DoesNotExist:
        return JsonResponse(
            dict(hint="exchange bank account does not exist"),
            status=HTTPStatus.NOT_FOUND,
        )
    exchange_bankaccount = exchange_user.bankaccount
    wire_transfer(
        Amount.parse(data.get("amount")),
        user.bankaccount,
        exchange_bankaccount,
        data.get("reserve_pub"),
    )

    return JsonResponse(ret_obj)


@csrf_exempt
@allow_origin_star
def api_withdraw_operation(request, withdraw_id):
    """
    Endpoint used by the browser and wallet to check withdraw status and
    put in the exchange info.
    """
    try:
        op = TalerWithdrawOperation.objects.get(withdraw_id=withdraw_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            dict(error="withdraw operation does not exist"), status=HTTPStatus.NOT_FOUND
        )

    if request.method == "POST":
        data = json.loads(decode_body(request))
        exchange_payto_uri = data.get("selected_exchange")
        try:
            exchange_account_name = get_acct_from_payto(exchange_payto_uri)
        except:
            return JsonResponse(
                dict(error="exchange payto URI malformed"),
                status=HTTPStatus.BAD_REQUEST,
            )
        try:
            exchange_user = User.objects.get(username=exchange_account_name)
        except User.DoesNotExist:
            return JsonResponse(
                dict(
                    code=ErrorCode.BANK_UNKNOWN_ACCOUNT,
                    hint="bank account in payto URI unknown",
                ),
                status=HTTPStatus.NOT_FOUND
            )
        exchange_account = exchange_user.bankaccount
        selected_reserve_pub = data.get("reserve_pub")
        if not isinstance(selected_reserve_pub, str):
            return JsonResponse(
                dict(error="reserve_pub must be a string"),
                status=HTTPStatus.BAD_REQUEST,
            )
        if op.selection_done:
            if (
                op.selected_exchange_account != exchange_account
                or op.selected_reserve_pub != selected_reserve_pub
            ):
                return JsonResponse(
                    dict(
                        code=ErrorCode.BANK_WITHDRAWAL_OPERATION_RESERVE_SELECTION_CONFLICT,
                        hint="selection of withdraw parameters already done",
                    ),
                    status=HTTPStatus.CONFLICT,
                )
        else:
            with transaction.atomic():
                op.selected_exchange_account = exchange_account
                op.selected_reserve_pub = selected_reserve_pub
                if op.confirmation_done and not op.selection_done:
                    # Confirmation already happened, we still need to transfer funds!
                    wire_transfer(
                        op.amount,
                        op.withdraw_account,
                        op.selected_exchange_account,
                        op.selected_reserve_pub,
                    )
                op.selection_done = True
                op.save()
        return JsonResponse(
            dict(
                transfer_done=op.confirmation_done,
                confirm_transfer_url=request.build_absolute_uri(
                    reverse("withdraw-confirm", args=(withdraw_id,))
                ),
            )
        )
    elif request.method == "GET":
        host = request.get_host()
        return JsonResponse(
            dict(
                selection_done=op.selection_done,
                transfer_done=op.confirmation_done,
                aborted=op.aborted,
                amount=op.amount.stringify(),
                wire_types=["x-taler-bank"],
                sender_wire=f"payto://x-taler-bank/{host}/{op.withdraw_account.user.username}",
                suggested_exchange=settings.TALER_SUGGESTED_EXCHANGE,
                confirm_transfer_url=request.build_absolute_uri(
                    reverse("withdraw-confirm", args=(withdraw_id,))
                ),
            )
        )
    else:
        return JsonResponse(
            dict(error="only GET and POST are allowed"),
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )


@login_required
@require_POST
def start_withdrawal(request):
    """
    Serve a Taler withdrawal request; takes the amount chosen
    by the user, and builds a response to trigger the wallet into
    the withdrawal protocol
    """
    user_account = BankAccount.objects.get(user=request.user)
    amount_num_str = request.POST.get("withdraw-amount")
    amount = Amount.parse(f"{settings.TALER_CURRENCY}:{amount_num_str}")
    withdraw_amount = SignedAmount(True, amount)
    debt_threshold = SignedAmount.parse(settings.TALER_MAX_DEBT)
    user_balance = user_account.balance
    if user_balance - withdraw_amount < -debt_threshold:
        raise DebitLimitException(
            f"Aborting payment initiated by '{user_account.user.username}', debit limit {debt_threshold} crossed."
        )
    op = TalerWithdrawOperation(amount=amount, withdraw_account=user_account)
    op.save()
    return redirect("withdraw-show", withdraw_id=op.withdraw_id)


def get_qrcode_svg(data):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, image_factory=factory)
    el = img.get_image()
    el.attrib["style"] = "shape-rendering: crispedges;"
    return lxml.etree.tostring(el).decode("utf-8")


@login_required
@require_GET
def show_withdrawal(request, withdraw_id):
    op = TalerWithdrawOperation.objects.get(withdraw_id=withdraw_id)
    if op.selection_done:
        return redirect("withdraw-confirm", withdraw_id=op.withdraw_id)
    taler_withdraw_uri = make_taler_withdraw_uri(request, op.withdraw_id)
    qrcode_svg = get_qrcode_svg(taler_withdraw_uri)
    context = dict(
        taler_withdraw_uri=taler_withdraw_uri,
        qrcode_svg=qrcode_svg,
        withdraw_check_url=reverse(
            "api-withdraw-operation", kwargs=dict(withdraw_id=op.withdraw_id)
        ),
    )
    resp = render(request, "withdraw_show.html", context, status=402)
    resp["Taler"] = taler_withdraw_uri
    return resp


@login_required
@require_http_methods(["GET", "POST"])
def confirm_withdrawal(request, withdraw_id):
    op = TalerWithdrawOperation.objects.get(withdraw_id=withdraw_id)
    if not op.selection_done:
        raise Exception("invalid state (withdrawal parameter selection not done)")
    if op.confirmation_done:
        return redirect("profile")
    if request.method == "POST":
        hashed_attempt = hash_answer(request.POST.get("pin_0", ""))
        hashed_solution = request.POST.get("pin_1", "")
        if hashed_attempt != hashed_solution:
            LOGGER.warning(
                "Wrong CAPTCHA answer: %s vs %s",
                type(hashed_attempt),
                type(request.POST.get("pin_1")),
            )
            set_session_hint(
                request, success=False, hint=gettext("Wrong CAPTCHA answer.")
            )
            return redirect("withdraw-confirm", withdraw_id=withdraw_id)
        op.confirmation_done = True
        op.save()
        wire_transfer(
            op.amount,
            BankAccount.objects.get(user=request.user),
            op.selected_exchange_account,
            op.selected_reserve_pub,
        )
        set_session_hint(request, success=True, hint=gettext("Withdrawal successful!"))
        request.session["just_withdrawn"] = True
        return redirect("profile")

    if request.method == "GET":
        question, hashed_answer = make_question()
        is_success, hint = get_session_hint(request)
        context = dict(
            question=question,
            hashed_answer=hashed_answer,
            withdraw_id=withdraw_id,
            account_id=request.user.get_username(),
            amount=op.amount.stringify(settings.TALER_DIGITS),
            exchange=op.selected_exchange_account.user,
            is_success=is_success,
            hint=hint,
        )
        return render(request, "withdraw_confirm.html", context)
    raise Exception("not reached")


def wire_transfer(amount, debit_account, credit_account, subject, request_uid=None):
    """
    Make a wire transfer between two accounts of this demo bank.
    """
    if debit_account.pk == credit_account.pk:
        LOGGER.error("Debit and credit account are the same!")
        raise SameAccountException()

    if request_uid is None:
        request_uid = str(uuid.uuid4())
        pass
    else:
        # check for existing transfer
        try:
            etx = BankTransaction.objects.get(request_uid=request_uid)
        except BankTransaction.DoesNotExist:
            # We're good, no existing transaction with the same request_uid exists
            pass
        else:
            if (
                etx.amount != amount
                or etx.debit_account != debit_account
                or etx.credit_account != debit_account
                or etx.subject != subject
            ):
                return JsonResponse(
                    data=dict(
                        hint="conflicting transfer with same request_uid exists",
                        ec=ErrorCode.BANK_WITHDRAWAL_OPERATION_RESERVE_SELECTION_CONFLICT,
                    ),
                    status=HTTPStatus.CONFLICT,
                )

    LOGGER.info(
        "transferring %s => %s, %s, %s"
        % (
            debit_account.user.username,
            credit_account.user.username,
            amount.stringify(),
            subject,
        )
    )

    transaction_item = BankTransaction(
        amount=amount,
        credit_account=credit_account,
        debit_account=debit_account,
        subject=subject,
        request_uid=request_uid,
    )

    if debit_account.user.username == "Bank":
        threshold = -SignedAmount.parse(settings.TALER_MAX_DEBT_BANK)
    else:
        threshold = -SignedAmount.parse(settings.TALER_MAX_DEBT)

    if debit_account.balance - SignedAmount(True, amount) < threshold:
        raise DebitLimitException(
            f"Aborting payment initiated by '{debit_account.user.username}', debit limit {threshold} crossed."
        )

    debit_account.balance -= SignedAmount(True, amount)
    credit_account.balance += SignedAmount(True, amount)

    with transaction.atomic():
        debit_account.save()
        credit_account.save()
        transaction_item.save()

    return transaction_item


@csrf_exempt
@require_GET
@login_via_headers
def bank_accounts_api_balance(request, user_account, acct_id):
    """
    Query the balance for an account.
    """
    acct = user_account.bankaccount

    if acct_id != user_account.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )

    return JsonResponse(
        dict(
            balance=dict(
                amount=acct.balance.amount.stringify(),
                credit_debit_indicator=(
                    "credit" if acct.balance.is_positive else "debit"
                ),
            )
        )
    )


@csrf_exempt
@require_POST
@login_via_headers
def bank_accounts_api_create_withdrawal(request, user, acct_id):
    user_account = BankAccount.objects.get(user=user)

    if acct_id != user_account.user.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )

    data = WithdrawHeadlessUri(json.loads(decode_body(request)))
    amount = Amount.parse(data.get("amount"))
    withdraw_amount = SignedAmount(True, amount)
    debt_threshold = SignedAmount.parse(settings.TALER_MAX_DEBT)
    user_balance = user_account.balance
    if user_balance - withdraw_amount < -debt_threshold:
        raise DebitLimitException(
            f"Aborting payment initiated by '{user_account.user.username}', debit limit {debt_threshold} crossed."
        )
    op = TalerWithdrawOperation(amount=amount, withdraw_account=user_account)
    op.save()
    taler_withdraw_uri = make_taler_withdraw_uri(request, op.withdraw_id)
    return JsonResponse(
        {"taler_withdraw_uri": taler_withdraw_uri, "withdrawal_id": op.withdraw_id}
    )


@csrf_exempt
@require_GET
@login_via_headers
def bank_accounts_api_get_withdrawal(request, user, acct_id, wid):
    user_account = BankAccount.objects.get(user=user)
    if acct_id != user_account.user.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )
    op = TalerWithdrawOperation.objects.get(withdraw_id=wid)
    selected_exchange_account = None
    if op.selected_exchange_account:
        selected_exchange_account = op.selected_exchange_account.user.username
    return JsonResponse(
        {
            "amount": op.amount.stringify(),
            "selection_done": op.selection_done,
            "confirmation_done": op.confirmation_done,
            "selected_reserve_pub": op.selected_reserve_pub,
            "selected_exchange_account": selected_exchange_account,
            "aborted": op.aborted,
        }
    )


def withdraw_abort_internal(wid):
    op = TalerWithdrawOperation.objects.get(withdraw_id=wid)
    if op.confirmation_done:
        return dict(status=HTTPStauts.CONFLICT, hint="can't abort confirmed withdrawal")
    op.aborted = True
    op.save()
    return dict(status=HTTPStatus.OK, hint="withdraw successfully aborted")


@require_POST
@login_required
def abort_withdrawal(request, withdraw_id):
    internal_status = withdraw_abort_internal(withdraw_id)
    set_session_hint(
        request,
        success=internal_status["status"] == HTTPStatus.OK,
        hint=internal_status["hint"],
    )
    return redirect("profile")


@csrf_exempt
@require_POST
@login_via_headers
def bank_accounts_api_abort_withdrawal(request, user, acct_id, wid):
    user_account = BankAccount.objects.get(user=user)
    if acct_id != user_account.user.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )
    internal_status = withdraw_abort_internal(wid)
    return JsonResponse(
        dict(hint=internal_status["hint"]), status=internal_status["status"]
    )


@csrf_exempt
@require_POST
@login_via_headers
def bank_accounts_api_confirm_withdrawal(request, user, acct_id, wid):
    user_account = BankAccount.objects.get(user=user)
    if acct_id != user_account.user.username:
        # FIXME: respond nicely
        raise Exception(
            f"credentials do not match URL ('{acct_id}' vs '{user_account.username}')"
        )
    op = TalerWithdrawOperation.objects.get(withdraw_id=wid)
    if op.confirmation_done:
        return JsonResponse(dict(), status=HTTPStatus.OK)
    if op.aborted:
        return JsonResponse(
            dict(hint="can't confirm aborted withdrawal"), status=HTTPStatus.CONFLICT
        )

    with transaction.atomic():
        if op.selection_done:
            wire_transfer(
                op.amount,
                user_account,
                op.selected_exchange_account,
                op.selected_reserve_pub,
            )
        op.confirmation_done = True
        op.save()
    return JsonResponse(dict(), status=HTTPStatus.OK)
