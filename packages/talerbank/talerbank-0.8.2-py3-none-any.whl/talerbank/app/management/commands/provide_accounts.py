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
import uuid

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


##
# Create a new bank account.
#
# @param username the username to associate to this account.
def make_account(username):
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        LOGGER.info("Creating account for '%s'", username)
        BankAccount(
            user=User.objects.create_user(
                username=username, password=str(uuid.uuid4())
            ),
            is_public=True,
        ).save()

    except (OperationalError, ProgrammingError):
        LOGGER.error(
            "db does not exist, or the project"
            " is not migrated.  Try 'taler-bank-manage"
            " django migrate' in the latter case.",
            stack_info=False,
            exc_info=True,
        )
        sys.exit(1)


##
# Django-specific definition to register this command.
class Command(BaseCommand):
    help = "Provide initial user accounts"

    ##
    # Django-specific definition to invoke the account creator
    # @a make_account; it iterates over the list of basic accounts
    # (defined in the settings) and invoke the account creator
    # for each one of them.
    def handle(self, *args, **options):
        for username in settings.TALER_PREDEFINED_ACCOUNTS:
            make_account(username)
