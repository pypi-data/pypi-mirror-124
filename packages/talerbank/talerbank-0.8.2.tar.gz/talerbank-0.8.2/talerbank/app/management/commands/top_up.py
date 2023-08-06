##
# This file is part of TALER
# (C) 2014, 2015, 2106 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3,
# or (at your option) any later version.
#
# TALER is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not,
# see <http://www.gnu.org/licenses/>
#
# @author Marcello Stanisci
# @author Florian Dold
# @brief Create the basic accounts to make the demo bank work.

import sys
import logging
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError, OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import BankAccount
from ...views import wire_transfer
from taler.util.amount import Amount
import getpass
import uuid

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Add money to a bank account (and debit the bank's account)."

    def add_arguments(self, parser):
        parser.add_argument(
            "user",
            type=str,
            metavar="USERNAME",
            help="User that is getting credited with the top-up",
        )
        parser.add_argument(
            "amount",
            type=str,
            metavar="AMOUNT",
            help="Wire transfer's amount, given in the " "CURRENCY:X.Y form.",
        )

    ##
    # Django-specific definition to invoke the account creator
    # @a make_account; it iterates over the list of basic accounts
    # (defined in the settings) and invoke the account creator
    # for each one of them.
    def handle(self, *args, **options):
        user = User.objects.get(username=options["user"])
        # Take the money from the bank's account
        try:
            debit_account = BankAccount.objects.get(
                account_no=1,
            )
        except BankAccount.DoesNotExist:
            LOGGER.error("Debit account (bank's own account) does not exist.")
            sys.exit(1)
        try:
            amount = Amount.parse(options["amount"])
        except BadFormatAmount:
            LOGGER.error("Amount's format is wrong: respect C:X.Y.")
            sys.exit(1)
        try:
            transaction = wire_transfer(
                amount, debit_account, user.bankaccount, "manual top-up by admin"
            )
            print("Transaction id: " + str(transaction.id))
        except Exception as exc:
            LOGGER.error(exc)
            sys.exit(1)
