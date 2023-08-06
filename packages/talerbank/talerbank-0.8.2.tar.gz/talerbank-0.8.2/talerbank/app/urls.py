#  This file is part of TALER
#  (C) 2014, 2015, 2016 Taler Systems SA
#
#  TALER is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
#
#  TALER is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
#  You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.
#
#  @author Marcello Stanisci
#  @author Florian Dold

from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from . import views

# These paths are part of the GNU Taler wire gatweay API
taler_wire_gateway_patterns = [
    path("<str:acct_id>/", views.twg_base, name="twg-base"),
    path("<str:acct_id>/config", views.twg_config, name="twg-config"),
    path(
        "<str:acct_id>/admin/add-incoming",
        views.twg_add_incoming,
        name="twg-add-incoming",
    ),
    path(
        "<str:acct_id>/history/incoming",
        views.twg_history_incoming,
        name="twg-history-incoming",
    ),
    path(
        "<str:acct_id>/history/outgoing",
        views.twg_history_outgoing,
        name="twg-history-outgoing",
    ),
    path("<str:acct_id>/transfer", views.twg_transfer, name="twg-transfer"),
]


taler_bank_integration_api_patterns = [
    path("api/config", views.api_config, name="api-config"),
    path(
        "api/withdrawal-operation/<str:withdraw_id>",
        views.api_withdraw_operation,
        name="api-withdraw-operation",
    ),
]

# These paths are part of the bank access API
taler_bank_access_api_patterns = [
    path(
        "accounts/<str:acct_id>",
        views.bank_accounts_api_balance,
        name="access-api-balance",
    ),
    path(
        "accounts/<str:acct_id>/withdrawals",
        views.bank_accounts_api_create_withdrawal,
        name="access-api-withdrawal",
    ),
    path(
        "accounts/<str:acct_id>/withdrawals/<str:wid>",
        views.bank_accounts_api_get_withdrawal,
        name="access-api-withdrawal-status",
    ),
    path(
        "accounts/<str:acct_id>/withdrawals/<str:wid>/confirm",
        views.bank_accounts_api_confirm_withdrawal,
        name="access-api-withdrawal-confirm",
    ),
    path(
        "accounts/<str:acct_id>/withdrawals/<str:wid>/abort",
        views.bank_accounts_api_abort_withdrawal,
        name="access-api-withdrawal-abort",
    ),
    path("testing/withdraw", views.withdraw_headless, name="testing-withdraw"),
    path("testing/register", views.register_headless, name="testing-withdraw-register"),
]

urlpatterns = [
    path("", include(taler_bank_integration_api_patterns)),
    path("", include(taler_bank_access_api_patterns)),
    path("taler-wire-gateway/", include(taler_wire_gateway_patterns)),
    path(
        "abort-withdrawal/<str:withdraw_id>",
        views.abort_withdrawal,
        name="abort-withdrawal",
    ),
    path("favicon.ico", views.ignore),
    path("config", views.config_view, name="config"),
    path("history", views.serve_history, name="history"),
    path("payto-transfer", views.payto_transfer, name="payto-transfer"),
]

urlpatterns += i18n_patterns(
    path(
        "confirm-withdrawal/<str:withdraw_id>",
        views.confirm_withdrawal,
        name="withdraw-confirm",
    ),
    path("start-withdrawal", views.start_withdrawal, name="start-withdrawal"),
    path(
        "show-withdrawal/<str:withdraw_id>", views.show_withdrawal, name="withdraw-show"
    ),
    path("", RedirectView.as_view(pattern_name="profile"), name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile_page, name="profile"),
    path("payto-form", views.payto_form, name="payto-form"),
    path("wiretransfer-form", views.wiretransfer_form, name="wiretransfer-form"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=views.TalerAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "public-accounts",
        views.serve_public_accounts,
        name="public-accounts",
    ),
    path(
        "public-accounts/<str:name>",
        views.serve_public_accounts,
        name="public-accounts",
    ),
    path(
        "public-accounts/<str:name>/<int:page>",
        views.serve_public_accounts,
        name="public-accounts",
    ),
)
