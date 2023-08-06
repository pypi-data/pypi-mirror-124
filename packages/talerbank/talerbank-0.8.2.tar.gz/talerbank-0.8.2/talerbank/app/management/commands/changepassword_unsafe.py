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
    help = "Add bank accounts."

    def add_arguments(self, parser):
        parser.add_argument(
            "accountname", type=str, help="Login name of the new bank account"
        )
        parser.add_argument(
            "password", type=str, help="New plain text password of the bank account"
        )

    ##
    # Django-specific definition to invoke the account creator
    # @a make_account; it iterates over the list of basic accounts
    # (defined in the settings) and invoke the account creator
    # for each one of them.
    def handle(self, *args, **options):
        accountname = options["accountname"]
        password = options["password"]
        try:
            existing_user = User.objects.get(username=accountname)
            existing_user.set_password(password)
            existing_user.save()
        except User.DoesNotExist:
            print(f"Account {accountname} does not exist")
            sys.exit(1)
        else:
            print(f"Password for {accountname} changed")
