#  This file is part of TALER
#  (C) 2014, 2015, 2016 Taler Systems SA
#
#  TALER is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation; either version 3,
#  or (at your option) any later version.
#
#  TALER is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with TALER; see the file COPYING.  If not,
#  see <http://www.gnu.org/licenses/>.
#
#  @author Marcello Stanisci

import json
import time
import uuid
import zlib
import timeit
import logging
import unittest
import base64
from urllib.parse import unquote
from django.db import connection
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from mock import patch, MagicMock
from .models import BankAccount, BankTransaction, TalerWithdrawOperation
from . import urls
from .views import wire_transfer, get_reserve_pub
from taler.util.payto import PaytoParse, PaytoFormatError
from taler.util.amount import (
    Amount,
    SignedAmount,
    CurrencyMismatchError,
    AmountFormatError,
)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.handlers = []
# Logfile opens in 'append' mode.
fileHandler = logging.FileHandler("tests.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(
    logging.Formatter(fmt="%(asctime)-15s %(module)s %(levelname)s %(message)s")
)
LOGGER.addHandler(fileHandler)


def make_auth_line(username, password):
    credentials = "%s:%s" % (username, password)
    b64enc = base64.b64encode(bytes(credentials, "utf-8"))
    header_line = "Basic %s" % b64enc.decode()
    return header_line


def clear_db():
    User.objects.all().delete()
    BankAccount.objects.all().delete()
    BankTransaction.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE app_bankaccount_account_no_seq" " RESTART")
        cursor.execute("ALTER SEQUENCE app_banktransaction_id_seq RESTART")


class WireGatewayTestCase(TestCase):
    def setUp(self):
        clear_db()
        exchange = User.objects.create_user(username="RandomExchange", password="XYZ")
        exchange.save()
        customer = User.objects.create_user(username="RandomCustomer", password="ABC")
        customer.save()
        exchange_bank_account = BankAccount(
            user=exchange,
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        exchange_bank_account.save()
        customer_bank_account = BankAccount(
            user=customer,
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        customer_bank_account.save()
        self.client = Client()

    def test_all(self):
        r = self.client.post(
            reverse("twg-add-incoming", kwargs=dict(acct_id="RandomExchange")),
            HTTP_AUTHORIZATION=make_auth_line("RandomExchange", "XYZ"),
            content_type="application/json",
            data=dict(
                amount=f"{settings.TALER_CURRENCY}:10",
                reserve_pub="FXWC2JHBY8B0XE2MMGAJ9TGPY307TN12HVEKYSTN6HE3GTHTF8XG",
                debit_account="payto://x-taler-bank/localhost/RandomCustomer",
            ),
        )
        self.assertEqual(r.status_code, 200)

        # Test incoming transfers of Exchange.
        r = self.client.get(
            reverse("twg-history-incoming", kwargs=dict(acct_id="RandomExchange")),
            dict(delta=5),
            HTTP_AUTHORIZATION=make_auth_line("RandomExchange", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)

        # Test outgoing transfers of the Exchange.
        r = self.client.post(
            reverse("twg-transfer", kwargs=dict(acct_id="RandomExchange")),
            HTTP_AUTHORIZATION=make_auth_line("RandomExchange", "XYZ"),
            content_type="application/json",
            data=dict(
                request_uid="0",
                amount=f"{settings.TALER_CURRENCY}:3",
                exchange_base_url="mock",
                wtid="123",
                credit_account="payto://x-taler-bank/localhost/RandomCustomer",
            ),
        )
        r = self.client.get(
            reverse("twg-history-outgoing", kwargs=dict(acct_id="RandomExchange")),
            dict(delta=5),
            HTTP_AUTHORIZATION=make_auth_line("RandomExchange", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)


class IntegrationApiTestCase(TestCase):
    def setUp(self):
        clear_db()

        self.exchange = User.objects.create_user(
            username="RandomExchange", password="XYZ"
        )
        self.exchange.save()
        self.exchange_bank_account = BankAccount(
            user=self.exchange,
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        self.exchange_bank_account.save()

        self.user = User.objects.create_user(username="RandomUser", password="XYZ")
        self.user.save()
        self.user_bank_account = BankAccount(
            user=self.user,
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        self.user_bank_account.save()
        self.client = Client()

    def test_config(self):
        c = Client()
        r = c.get("/config")
        self.assertEqual(r.status_code, 200)

    def test_withdraw(self):
        operation = TalerWithdrawOperation(
            amount=Amount(settings.TALER_CURRENCY, 100, 0),
            withdraw_account=self.user_bank_account,
        )
        operation.save()
        r = self.client.post(
            reverse(
                "api-withdraw-operation", kwargs=dict(withdraw_id=operation.withdraw_id)
            ),
            data=dict(
                reserve_pub="reserve-public-key",
                selected_exchange=f"payto://x-taler-bank/localhost/RandomExchange",
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)


class AccessApiWithdrawTestCase(TestCase):
    def setUp(self):
        clear_db()
        self.user = User.objects.create_user(username="RandomUser", password="XYZ")
        self.user.save()
        self.user_bank_account = BankAccount(
            user=self.user,
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        self.user_bank_account.save()
        self.client = Client()

    def create_withdrawal(self):
        r = self.client.post(
            reverse("access-api-withdrawal", kwargs=dict(acct_id="RandomUser")),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
            content_type="application/json",
            data=dict(amount=f"{settings.TALER_CURRENCY}:5"),
        )
        self.assertEqual(r.status_code, 200)
        data = r.content.decode("utf-8")
        data_dict = json.loads(data)
        withdrawal_id = data_dict.get("withdrawal_id")
        self.assertTrue(withdrawal_id)
        return withdrawal_id

    def test_accees_withdraw_create(self):
        self.create_withdrawal()

    def test_accees_withdraw_status(self):
        withdrawal_id = self.create_withdrawal()
        r = self.client.get(
            reverse(
                "access-api-withdrawal-status",
                kwargs=dict(acct_id="RandomUser", wid=withdrawal_id),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)

    def test_accees_withdraw_abort(self):
        withdrawal_id = self.create_withdrawal()
        r = self.client.post(
            reverse(
                "access-api-withdrawal-abort",
                kwargs=dict(acct_id="RandomUser", wid=withdrawal_id),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)

    def test_accees_withdraw_confirm(self):
        withdrawal_id = self.create_withdrawal()
        r = self.client.post(
            reverse(
                "access-api-withdrawal-confirm",
                kwargs=dict(acct_id="RandomUser", wid=withdrawal_id),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)

    def test_accees_withdraw_abort_then_confirm(self):
        withdrawal_id = self.create_withdrawal()
        r = self.client.post(
            reverse(
                "access-api-withdrawal-abort",
                kwargs=dict(acct_id="RandomUser", wid=withdrawal_id),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)
        r = self.client.post(
            reverse(
                "access-api-withdrawal-confirm",
                kwargs=dict(acct_id="RandomUser", wid=withdrawal_id),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 409)

    def test_integration_api_withdraw_status(self):
        wid = self.create_withdrawal()
        r = self.client.get(
            reverse(
                "access-api-withdrawal-status",
                kwargs=dict(acct_id="RandomUser", wid=wid),
            ),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)

    def test_integration_api_withdraw_confirm(self):
        wid = self.create_withdrawal()
        r = self.client.post(
            reverse(
                "access-api-withdrawal-confirm",
                kwargs=dict(acct_id="RandomUser", wid=wid),
            ),
            data=dict(
                reserve_pub="FXWC2JHBY8B0XE2MMGAJ9TGPY307TN12HVEKYSTN6HE3GTHTF8XG",
                selected_exchange="payto://x-taler-bank/localhost/RandomUser",
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)


class AccessApiBalanceTestCase(TestCase):
    def setUp(self):
        clear_db()
        self.user = User.objects.create_user(username="RandomUser", password="XYZ")
        self.user.save()
        self.user_bank_account = BankAccount(user=self.user)
        self.user_bank_account.save()

    def test_balance(self):
        c = Client()
        r = c.get(
            reverse("access-api-balance", kwargs=dict(acct_id="RandomUser")),
            HTTP_AUTHORIZATION=make_auth_line("RandomUser", "XYZ"),
        )
        self.assertEqual(r.status_code, 200)


class AccessApiTestingRegistrationTestCase(TestCase):
    def setUp(self):
        clear_db()
        self.user = User.objects.create_user(username="Bank", password="Bank")
        self.user.save()
        self.user_bank_account = BankAccount(user=self.user)
        self.user_bank_account.save()

    def test_testing_registration(self):
        c = Client()
        r = c.post(
            reverse("testing-withdraw-register"),
            data=dict(username="x", password="y"),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)


class ReservePubExtractionTestCase(TestCase):
    def test_extraction(self):
        self.assertTrue(
            get_reserve_pub("0T096A11M57GWGG0P6ZM9Z8G5829BFJFH2AN9R5T80FJ931DX7GG")
        )
        self.assertTrue(
            get_reserve_pub(
                "0T096A11M57GWGG0P6ZM9Z8G5829BFJFH2AN9R5T80FJ931DX7GG other data"
            )
        )
        self.assertFalse(get_reserve_pub("not a reserve public key"))


class PaytoParseTestCase(TestCase):
    def test_payto_wrong_protocol(self):
        self.assertRaises(PaytoFormatError, PaytoParse, "http://foo/bar")
    def test_payto_with_port_number(self):
        parsed = PaytoParse("payto://iban/localhost:1234/account")
        self.assertEqual(parsed.bank, "localhost:1234")
    def test_minimal(self):
        parsed = PaytoParse("payto://x-taler-bank/bank-hostname/Taler")
    def test_payto_malformed(self):
        self.assertRaises(PaytoFormatError, PaytoParse, "payto:foo/bar")
    def test_payto_noamount(self):
        parsed = PaytoParse(
            "payto://x-taler-bank/bank.int.taler.net/Exchange?message=0T096A11M57GWGG0P6ZM9Z8G5829BFJFH2AN9R5T80FJ931DX7GG"
        )
    def test_payto_parse(self):
        parsed = PaytoParse(
            "payto://x-taler-bank/bank.int.taler.net/Exchange?message=0T096A11M57GWGG0P6ZM9Z8G5829BFJFH2AN9R5T80FJ931DX7GG&amount=EUR:1"
        )
        self.assertEqual("Exchange", parsed.target)
        self.assertEqual("0T096A11M57GWGG0P6ZM9Z8G5829BFJFH2AN9R5T80FJ931DX7GG", parsed.message)
        self.assertEqual(parsed.amount.value, 1)
        self.assertEqual(parsed.amount.fraction, 0)
        self.assertEqual(parsed.amount.currency, "EUR")
        self.assertEqual(parsed.authority, "x-taler-bank")
        self.assertEqual(parsed.bank, "bank.int.taler.net")


class PublicAccountsTestCase(TestCase):
    def setUp(self):
        clear_db()
        self.user = User.objects.create_user(username="Bank", password="Bank")
        self.user.save()

        self.user_bank_account = BankAccount(
            account_no=100, is_public=True, user=self.user
        )

        self.user_bank_account.save()

    def test_public_accounts(self):
        self.assertTrue(User.objects.get(username="Bank"))

        response = self.client.get(reverse("public-accounts", urlconf=urls))


class WithdrawTestCase(TestCase):
    def setUp(self):
        self.user_bank_account = BankAccount(
            user=User.objects.create_user(
                username="test_user", password="test_password"
            ),
            account_no=100,
        )
        self.user_bank_account.save()

        self.exchange_bank_account = BankAccount(
            user=User.objects.create_user(username="test_exchange", password=""),
            account_no=99,
        )
        self.exchange_bank_account.save()
        self.client = Client()

    @patch("talerbank.app.views.wire_transfer")
    @patch("hashlib.new")
    @patch("time.time")
    @unittest.skip("skip outdated test case")
    def test_withdraw(self, mocked_time, mocked_hashlib, mocked_wire_transfer):
        amount = Amount(settings.TALER_CURRENCY, 0, 1)
        params = {
            "amount_value": str(amount.value),
            "amount_fraction": str(amount.fraction),
            "amount_currency": amount.currency,
            "reserve_pub": "UVZ789",
            "exchange": "https://exchange.example.com/",
            "exchange_wire_details": "payto://x-taler-bank/bank.example/99",
        }
        self.client.login(username="test_user", password="test_password")

        response = self.client.get(reverse("pin-question", urlconf=urls), params)
        self.assertEqual(response.status_code, 200)
        # We mock hashlib in order to fake the CAPTCHA.
        hasher = MagicMock()
        hasher.hexdigest = MagicMock()
        hasher.hexdigest.return_value = "0"
        mocked_hashlib.return_value = hasher
        mocked_time.return_value = 0

        response = self.client.post(
            reverse("withdraw-confirm", urlconf=urls), {"pin_1": "0"}
        )

        args, kwargs = mocked_wire_transfer.call_args
        del kwargs
        self.assertTrue(
            args[0].dump() == amount.dump()
            and self.user_bank_account in args
            and "UVZ789" in args
            and self.exchange_bank_account in args
        )

    def tearDown(self):
        clear_db()


class RegisterTestCase(TestCase):
    """User registration"""

    def setUp(self):
        clear_db()
        BankAccount(user=User.objects.create_user(username="Bank")).save()

    def tearDown(self):
        clear_db()

    def test_register(self):
        setattr(settings, "ALLOW_REGISTRATIONS", True)
        client = Client()
        response = client.post(
            reverse("register", urlconf=urls),
            {"username": "test_register", "password": "test_register"},
            follow=True,
        )
        self.assertIn(("/en/profile", 302), response.redirect_chain)
        # this assertion tests "/profile""s view
        self.assertEqual(200, response.status_code)

    def test_register_headless(self):
        setattr(settings, "ALLOW_REGISTRATIONS", True)
        client = Client()

        # Normal case.
        response = client.post(
            reverse("testing-withdraw-register", urlconf=urls),
            content_type="application/json",
            data={"username": "test_register_headless", "password": "password*+#@"},
        )
        self.assertEqual(200, response.status_code)

        # Double-check account creation.
        self.assertTrue(
            self.client.login(
                username="test_register_headless", password="password*+#@"
            )
        )

        # Try registering unavailable username.
        response = client.post(
            reverse("testing-withdraw-register", urlconf=urls),
            content_type="application/json",
            data={"username": "test_register_headless", "password": "password"},
        )
        self.assertEqual(409, response.status_code)

        # NOTE: Django 2.2.2 allows ANY character!  Is this normal?
        response = client.post(
            reverse("testing-withdraw-register", urlconf=urls),
            content_type="application/json",
            data={"username": "'''+++;;;'''", "password": "password2"},
        )
        self.assertEqual(200, response.status_code)


class LoginTestCase(TestCase):
    """User login"""

    def setUp(self):
        BankAccount(
            user=User.objects.create_user(
                username="test_user", password="test_password"
            )
        ).save()
        self.client = Client()

    def tearDown(self):
        clear_db()

    def test_login(self):
        self.assertTrue(
            self.client.login(username="test_user", password="test_password")
        )
        self.assertFalse(
            self.client.login(username="test_user", password="test_passwordii")
        )

    def test_failing_login(self):
        response = self.client.get(
            reverse("history", urlconf=urls),
            {"auth": "basic"},
            HTTP_AUTHORIZATION=make_auth_line("Wrong", "Credentials"),
        )
        data = response.content.decode("utf-8")
        self.assertEqual(401, response.status_code)


class AddIncomingTestCase(TestCase):
    """Test money transfer's API"""

    def setUp(self):
        BankAccount(
            user=User.objects.create_user(
                username="bank_user", password="bank_password"
            )
        ).save()
        BankAccount(
            user=User.objects.create_user(
                username="user_user", password="user_password"
            )
        ).save()

    def tearDown(self):
        clear_db()

    def test_add_incoming(self):
        client = Client()
        request_body = dict(
            reserve_pub="TESTWTID",
            amount=f"{settings.TALER_CURRENCY}:1.0",
            debit_account="payto://x-taler-bank/bank_user",
        )
        response = client.post(
            reverse("twg-add-incoming", urlconf=urls, args=["user_user"]),
            data=json.dumps(request_body),
            content_type="application/json",
            follow=True,
            HTTP_AUTHORIZATION=make_auth_line("user_user", "user_password"),
        )
        self.assertEqual(200, response.status_code)


class CustomDoesNotExistTestCase(TestCase):
    def test_bankaccount_doesnotexist(self):
        with self.assertRaises(BankAccount.DoesNotExist):
            BankAccount.objects.get(account_no=1000)
        with self.assertRaises(BankTransaction.DoesNotExist):
            BankTransaction.objects.get(subject="1000")


class HistoryTestCase(TestCase):
    def setUp(self):
        clear_db()
        debit_account = BankAccount(
            user=User.objects.create_user(username="User", password="Password"),
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 100, 0)),
        )
        debit_account.save()
        credit_account = BankAccount(
            user=User.objects.create_user(username="User0", password="Password0")
        )
        credit_account.save()
        for subject in ("a", "b", "c", "d", "e", "f", "g", "h", "i"):
            wire_transfer(
                Amount(settings.TALER_CURRENCY, 1, 0),
                debit_account,
                credit_account,
                subject,
            )

    def tearDown(self):
        clear_db()

    def test_history(self):
        def histquery(**urlargs):
            response = self.client.get(
                reverse("history", urlconf=urls),
                urlargs,
                HTTP_AUTHORIZATION=make_auth_line("User", "Password"),
            )
            return response

        # test query #1
        r = histquery(delta="-4", direction="both")
        rd = json.loads(r.content)
        self.assertEqual(r.status_code, 200)

        # test query #2
        r = histquery(delta="+1", start="5", direction="both")
        self.assertEqual(r.status_code, 200)
        rd = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(rd["data"][0]["row_id"], 6)

        # test query #3
        r = histquery(delta="+1", start="2", direction="both")
        self.assertEqual(r.status_code, 200)
        rd = json.loads(r.content)
        self.assertEqual(rd["data"][0]["wt_subject"], "c")

        # test query #4
        r = histquery(delta="-1", start="2", direction="both")
        self.assertEqual(r.status_code, 200)
        rd = json.loads(r.content)
        self.assertEqual(rd["data"][0]["wt_subject"], "a")

        # test query #5
        r = histquery(delta="1", start="11", direction="both")
        self.assertEqual(r.status_code, 200)
        rd = json.loads(r.content)
        self.assertEqual(len(rd["data"]), 0)


class DBCustomColumnTestCase(TestCase):
    def setUp(self):
        BankAccount(user=User.objects.create_user(username="U")).save()

    def tearDown(self):
        clear_db()

    def test_exists(self):
        user_bankaccount = BankAccount.objects.get(user=User.objects.get(username="U"))
        self.assertTrue(isinstance(user_bankaccount.balance, SignedAmount))


## This tests whether a bank account goes debit and then goes >=0
## again
class DebitTestCase(TestCase):
    def setUp(self):
        BankAccount(user=User.objects.create_user(username="U")).save()
        BankAccount(user=User.objects.create_user(username="U0")).save()

    def tearDown(self):
        clear_db()

    def test_green(self):
        user_bankaccount = BankAccount.objects.get(user=User.objects.get(username="U"))
        self.assertTrue(user_bankaccount.balance.is_zero())

    def test_red(self):
        user_bankaccount = BankAccount.objects.get(user=User.objects.get(username="U"))
        user_bankaccount0 = BankAccount.objects.get(
            user=User.objects.get(username="U0")
        )

        wire_transfer(
            Amount(settings.TALER_CURRENCY, 10, 0),
            user_bankaccount0,
            user_bankaccount,
            "Go green",
        )

        wire_transfer(
            Amount(settings.TALER_CURRENCY, 11, 0),
            user_bankaccount,
            user_bankaccount0,
            "Go red",
        )

        amt_one = SignedAmount.parse(f"{settings.TALER_CURRENCY}:1")

        self.assertEqual(user_bankaccount.balance, -amt_one)
        self.assertEqual(user_bankaccount0.balance, amt_one)


class MeasureHistory(TestCase):
    def setUp(self):
        self.user_bankaccount0 = BankAccount(
            user=User.objects.create_user(username="U0"),
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 3000, 0)),
        )
        self.user_bankaccount0.save()

        user_bankaccount = BankAccount(user=User.objects.create_user(username="U"))
        user_bankaccount.save()

        self.ntransfers = 1000

        # Make sure logging level is WARNING, otherwise the loop
        # will overwhelm the console.
        for i in range(self.ntransfers):
            del i  # to pacify PEP checkers
            wire_transfer(
                Amount(settings.TALER_CURRENCY, 1, 0),
                self.user_bankaccount0,
                user_bankaccount,
                "bulk",
            )

    def tearDown(self):
        clear_db()

    def test_extract_history(self):

        # Measure the time extract_history() needs to retrieve
        # ~ntransfers records.
        timer = timeit.Timer(
            stmt="extract_history(self.user_bankaccount0, False)",
            setup="from talerbank.app.views import extract_history",
            globals=locals(),
        )
        total_time = timer.timeit(number=1)
        allowed_time_per_record = 0.003
        self.assertLess(total_time, self.ntransfers * allowed_time_per_record)


class BalanceTestCase(TestCase):
    def setUp(self):
        self.the_bank = BankAccount(
            user=User.objects.create_user(username="U0", password="U0PASS"),
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 3, 0)),
        )
        self.the_bank.save()

        user = BankAccount(
            user=User.objects.create_user(username="U"),
            balance=SignedAmount(True, Amount(settings.TALER_CURRENCY, 10, 0)),
        )
        user.save()

        # bank: 3, user: 10 (START).

        # bank: 2, user: 11
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 1, 0), self.the_bank, user, "mock"
        )

        # bank: 4, user: 9
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 2, 0), user, self.the_bank, "mock"
        )

        # bank: -1, user: 14
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 5, 0), self.the_bank, user, "mock"
        )

        # bank: 7, user: 6 (END)
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 8, 0), user, self.the_bank, "mock"
        )

        # bank: -3, user: 16 (END)
        wire_transfer(
            Amount(settings.TALER_CURRENCY, 10, 0), self.the_bank, user, "mock"
        )

        self.client = Client()

    def tearDown(self):
        clear_db()

    def test_balance(self):
        self.client.login(username="U0", password="U0PASS")
        response = self.client.get(
            reverse("history", urlconf=urls),
            {"delta": -30, "direction": "both", "account_number": 55},
            HTTP_AUTHORIZATION=make_auth_line("U0", "U0PASS"),
        )
        data = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        entries = json.loads(data)

        acc_bal = SignedAmount(True, Amount(settings.TALER_CURRENCY, 10, 0))

        for entry in reversed(entries["data"]):
            if entry["sign"] == "-":
                acc_bal += SignedAmount.parse(entry["amount"])
            if entry["sign"] == "+":
                acc_bal -= SignedAmount.parse(entry["amount"])

        expected_amount = SignedAmount.parse(f"{settings.TALER_CURRENCY}:16.0")
        self.assertEqual(acc_bal, expected_amount)
