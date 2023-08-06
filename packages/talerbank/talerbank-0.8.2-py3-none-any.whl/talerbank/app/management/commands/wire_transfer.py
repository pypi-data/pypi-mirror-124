##
# This file is part of TALER
# (C) 2014, 2015, 2016 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3, or (at your
# option) any later version.
#
# TALER is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>
#
# @author Marcello Stanisci
# @brief CLI utility that issues a wire transfer.

import sys
import logging
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from taler.util.amount import Amount
from ...views import wire_transfer, User
from ...models import BankAccount, BankTransaction

LOGGER = logging.getLogger(__name__)


##
# Django-specific definition to register the CLI utility.
class Command(BaseCommand):
    help = "Wire transfer money and return the transaction id."

    ##
    # Register the command line options of this command.
    #
    # @param self this object.
    # @param parser API used to actually register the option.
    def add_arguments(self, parser):
        parser.add_argument(
            "user",
            type=str,
            metavar="USERNAME",
            help="Which user is performing the wire transfer",
        )
        parser.add_argument(
            "password", type=str, metavar="PASSWORD", help="Performing user's password."
        )
        parser.add_argument(
            "credit-account",
            type=str,
            metavar="CREDIT-ACCOUNT",
            help="Which account will receive money.",
        )
        parser.add_argument(
            "subject",
            type=str,
            metavar="SUBJECT",
            help="SUBJECT will be the wire transfer subject.",
        )
        parser.add_argument(
            "amount",
            type=str,
            metavar="AMOUNT",
            help="Wire transfer's amount, given in the " "CURRENCY:X.Y form.",
        )

    ##
    # This callable gets invoked when the user invokes the
    # CLI utility; it is responsible of making the wire transfer
    # effective.
    #
    # @param self this object.
    # @param args arguments list -- currently unused.
    # @param options options given by the user at the command line.
    def handle(self, *args, **options):
        user = authenticate(username=options["user"], password=options["password"])
        if not user:
            LOGGER.error("Wrong user/password.")
            sys.exit(1)
        try:
            amount = Amount.parse(options["amount"])
        except BadFormatAmount:
            LOGGER.error("Amount's format is wrong: respect C:X.Y.")
            sys.exit(1)

        try:
            credit_account_user = User.objects.get(username=options["credit-account"])
            credit_account = credit_account_user.bankaccount
        except BankAccount.DoesNotExist:
            LOGGER.error("Credit account does not exist.")
            sys.exit(1)

        try:
            transaction = wire_transfer(
                amount, user.bankaccount, credit_account, options["subject"]
            )
            print("Transaction id: " + str(transaction.id))
        except Exception as exc:
            LOGGER.error(exc)
            sys.exit(1)
