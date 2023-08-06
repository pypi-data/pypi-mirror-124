##
# This file is part of TALER
#  (C) 2014, 2015, 2016 Taler Systems SA
#
#  TALER is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version. TALER is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with TALER; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>
#
#  @author Marcello Stanisci
#  @author Florian Dold

import uuid
from typing import Any, Tuple
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from taler.util.amount import Amount, SignedAmount, CurrencyMismatchError


def get_zero_amount() -> Amount:
    """
    Helper function that instantiates a zero-valued Amount
    object in the currency that the bank runs on.
    """
    return Amount(settings.TALER_CURRENCY, 0, 0)


def get_zero_signed_amount() -> SignedAmount:
    """
    Helper function that instantiates a zero-valued SignedAmount
    object in the currency that the bank runs on.
    """
    return SignedAmount(True, get_zero_amount())


class SignedAmountField(models.Field):
    """Custom implementation of the SignedAmount class as a database type."""

    description = "Signed amount object in Taler style"

    def db_type(self, connection: Any) -> str:
        """
        Return the database type of the serialized amount.
        """
        return "varchar"

    def get_prep_value(self, value: SignedAmount) -> str:
        """
        Stringifies the Amount object to feed the DB connector.
        """
        c = value.amount.currency
        if settings.TALER_CURRENCY != c:
            raise CurrencyMismatchError(settings.TALER_CURRENCY, c)
        return value.stringify()

    @staticmethod
    def from_db_value(value: str, *args) -> Amount:
        """
        Parse the stringified Amount back to Python.

        Parameters
        ----------
        value : str
            Serialized amount coming from the database.
            (String in the usual CURRENCY:X.Y format)
        args : any
            Unused
        """
        del args  # pacify PEP checkers
        return SignedAmount.parse(value)

    def to_python(self, value: Any) -> Amount:
        """
        Parse the stringified Amount back to Python. FIXME:
        why this serializer consider _more_ cases respect to the
        one above ('from_db_value')?

        Parameters
        ----------
        value: serialized amount coming from the database

        """

        if isinstance(value, SignedAmount):
            return value
        try:
            return SignedAmount.parse(value)
        except BadFormatAmount:
            raise ValidationError(
                "Invalid input for a signed amount string: %s" % value
            )


class AmountField(models.Field):
    """Custom implementation of the Amount class as a database type."""

    description = "Amount object in Taler style"

    def db_type(self, connection: Any) -> str:
        """
        Return the database type of the serialized amount.
        """
        return "varchar"

    def get_prep_value(self, value: Amount) -> str:
        """
        Stringifies the Amount object to feed the DB connector.
        """
        if settings.TALER_CURRENCY != value.currency:
            raise CurrencyMismatchError(settings.TALER_CURRENCY, value.currency)
        return value.stringify()

    @staticmethod
    def from_db_value(value: str, *args) -> Amount:
        """
        Parse the stringified Amount back to Python.

        Parameters
        ----------
        value : str
            Serialized amount coming from the database.
            (String in the usual CURRENCY:X.Y format)
        args : any
            Unused
        """
        del args  # pacify PEP checkers
        return Amount.parse(value)

    def to_python(self, value: Any) -> Amount:
        """
        Parse the stringified Amount back to Python. FIXME:
        why this serializer consider _more_ cases respect to the
        one above ('from_db_value')?

        Parameters
        ----------
        value: serialized amount coming from the database

        """

        if isinstance(value, Amount):
            return value
        try:
            return Amount.parse(value)
        except BadFormatAmount:
            raise ValidationError("Invalid input for an amount string: %s" % value)


def join_dict(**inputDict):
    return ", ".join(["%s==%s" % (key, value) for (key, value) in inputDict.items()])


class BankAccount(models.Model):
    """
    The class representing a bank account.
    """

    is_public = models.BooleanField(default=False)
    account_no = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = SignedAmountField(default=get_zero_signed_amount)


class BankTransaction(models.Model):
    """
    The class representing a bank transaction.
    """

    amount = AmountField(default=False)
    debit_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="debit_account",
    )
    credit_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="credit_account",
    )
    subject = models.CharField(default="(no subject given)", max_length=200)
    date = models.DateTimeField(auto_now=True, db_index=True)
    cancelled = models.BooleanField(default=False)
    request_uid = models.CharField(max_length=128, unique=True)


class TalerWithdrawOperation(models.Model):
    withdraw_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = AmountField(default=False)
    withdraw_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="withdraw_account",
    )
    selection_done = models.BooleanField(default=False)
    confirmation_done = models.BooleanField(default=False)
    aborted = models.BooleanField(default=False)
    selected_exchange_account = models.ForeignKey(
        BankAccount,
        null=True,
        on_delete=models.CASCADE,
        related_name="selected_exchange_account",
    )
    selected_reserve_pub = models.TextField(null=True)
