##
# This file is part of TALER
# (C) 2014, 2015, 2016, 2020 Taler Systems SA
#
#  TALER is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
#
#  TALER is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>
#
#  @author Marcello Stanisci
#  @brief definitions of JSON schemas for validating data

import json
from django.conf import settings
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator
from urllib.parse import urlparse
from taler.util.taler_error_codes import ErrorCode
from http import HTTPStatus

##
# Constant value for the biggest number the bank handles.
# This value is just equal to the biggest number that JavaScript
# can handle (because of the wallet).
# FIXME: also defined in views.py.  Need a common.py to contain
# such definitions ?
UINT64_MAX = (2 ** 64) - 1

##
# Pattern for amounts, plain RegEx.
AMOUNT_REGEX = "^[A-Za-z0-9_-]+:([0-9]+)\.?([0-9]+)?$"


##
# Exception class to be raised when a expected URL parameter
# is not found.
class InvalidSession(ValueError):
    ##
    # Init method.
    #
    # @param self the object itself.
    # @param http_status_code the HTTP response code to return
    #        to the caller (client).
    def __init__(self, http_status_code):
        self.hint = "Landed on a broken session"
        self.http_status_code = http_status_code
        super().__init__()


class InternalServerError(Exception):
    def __init__(self, hint):
        self.hint = hint
        self.http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.taler_error_code = ErrorCode.INTERNAL_LOGIC_ERROR


##
# Exception class to be raised when a JSON
# object does not respect a specification.
class JSONFieldException(ValueError):

    ##
    # Init method.
    #
    # @param self the object itself.
    # @param error object containing the hint, as created by
    #        the Form API.
    # @param http_status_code the HTTP response code to return
    #        to the caller (client).
    def __init__(self, error, http_status_code):
        for k, errors in error.as_data().items():
            messages = [", ".join(error.messages) for error in errors]
            line = f"{k}: " + "".join(messages)
        super(JSONFieldException, self).__init__(line)
        self.hint = line
        self.http_status_code = http_status_code
        self.taler_error_code = TalerErrorCode.BANK_JSON_INVALID


##
# Exception class to be raised when at least one expected URL
# parameter is either not found or malformed.
class URLParamValidationError(ValueError):
    ##
    # Init method.
    #
    # @param self the object itself.
    # @param error object containing the hint.
    # @param http_status_code the HTTP response code to return
    #        to the caller (client).
    def __init__(self, error, http_status_code):
        self.hint = json.stringify(error.as_json())
        self.http_status_code = http_status_code
        self.taler_error_code = ErrorCode.BANK_PARAMETER_MISSING_OR_INVALID
        super().__init__()


class AuthForm(forms.Form):
    type = forms.CharField(
        validators=[
            RegexValidator("^basic$", message="Only 'basic' method provided for now")
        ]
    )

    data = forms.Field(required=False)


class AuthField(forms.Field):
    ##
    # No need to touch the input.  Dict is good
    # and gets validated by the "validate()" method.
    def to_python(self, value):
        return value

    ##
    # Validate input.
    def validate(self, value):
        af = AuthForm(value)
        if not af.is_valid():
            raise ValidationError(json.dumps(af.errors.as_json()))


##
# Common logic to inherit from all the other validators
class BankValidator:
    def __init__(self, validator, data):
        self.validation_result = validator(data)
        if not self.validation_result.is_valid():
            raise JSONFieldException(
                self.validation_result.errors, HTTPStatus.BAD_REQUEST
            )

    def get(self, name, default=None):
        ret = self.validation_result.cleaned_data.get(name)
        if not ret:
            return default
        return ret


class AddIncomingData(BankValidator):
    def __init__(self, data):
        super(AddIncomingData, self).__init__(self.InnerValidator, data)

    class InnerValidator(forms.Form):
        amount = forms.CharField(
            validators=[
                RegexValidator(
                    AMOUNT_REGEX, message="Format CURRENCY:X[.Y] not respected"
                )
            ]
        )
        subject = forms.CharField()
        credit_account = forms.IntegerField(min_value=1)
        exchange_url = forms.URLField()


##
# Subset of /history and /history-range input.
class HistoryParamsBase(forms.Form):
    cancelled = forms.CharField(
        required=False,
        empty_value="show",
        validators=[
            RegexValidator("^(omit|show)$", message="Only 'omit' or 'show' are valid")
        ],
    )

    ordering = forms.CharField(
        required=False,
        empty_value="descending",
        validators=[
            RegexValidator(
                "^(ascending|descending)$",
                message="Only 'ascending' or 'descending' are valid",
            )
        ],
    )

    direction = forms.CharField(
        validators=[
            RegexValidator(
                "^(debit|credit|both|cancel\+|cancel-)$",
                message="Only: debit/credit/both/cancel+/cancel-",
            )
        ]
    )

    # FIXME: adjust min/max values.
    account_number = forms.IntegerField(required=False)


class HistoryParams(BankValidator):
    def __init__(self, data):
        super(HistoryParams, self).__init__(self.InnerValidator, data)

    class InnerValidator(HistoryParamsBase):
        # FIXME: adjust min/max values.
        delta = forms.IntegerField()
        start = forms.IntegerField(required=False)


class PaytoField(forms.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_python(self, value):
        return value

    def validate(self, value):

        # The request misses this, default exchange
        # will be used.  NOTE: experience showed that the
        # "required=False" argument given when init the object
        # does NOT prevent this function from being called!
        if not value:
            return
        wire_uri = urlparse(value)
        if "payto" != wire_uri.scheme:
            raise ValidationError("URL is not 'payto'")


class WithdrawHeadless(BankValidator):
    def __init__(self, data):
        super(WithdrawHeadless, self).__init__(self.InnerValidator, data)

    class InnerValidator(forms.Form):
        amount = forms.CharField(
            validators=[
                RegexValidator(
                    AMOUNT_REGEX, message="Format CURRENCY:X[.Y] not respected"
                )
            ]
        )
        reserve_pub = forms.CharField(required=True)
        exchange_payto_uri = PaytoField(required=True)


class WithdrawHeadlessUri(BankValidator):
    def __init__(self, data):
        super(WithdrawHeadlessUri, self).__init__(self.InnerValidator, data)

    class InnerValidator(forms.Form):
        amount = forms.CharField(
            validators=[
                RegexValidator(
                    AMOUNT_REGEX, message="Format CURRENCY:X[.Y] not respected"
                )
            ]
        )
