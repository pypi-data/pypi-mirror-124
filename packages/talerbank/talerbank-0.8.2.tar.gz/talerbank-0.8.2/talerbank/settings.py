"""
Django settings for talerbank.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import base64
import logging
import os
import re
import sys
import urllib.parse
from taler.util.talerconfig import TalerConfig, ConfigurationError

LOGGER = logging.getLogger(__name__)

LOGGER.info(
    "DJANGO_SETTINGS_MODULE: %s" % os.environ.get("DJANGO_SETTINGS_MODULE")
)

TC = TalerConfig.from_file(os.environ.get("TALER_CONFIG_FILE"))

# Build paths inside the project like this:
# os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

SECRET_KEY = os.environ.get("TALER_BANK_SECRET_KEY", None)

if not SECRET_KEY:
    LOGGER.info(
        "secret key not configured in"
        " TALER_BANK_SECRET_KEY env variable,"
        " generating random secret"
    )
    SECRET_KEY = base64.b64encode(os.urandom(32)).decode("utf-8")

# SECURITY WARNING: don't run with debug turned on in production!

if "demo" == os.environ.get("TALER_ENV_NAME"):
    DEBUG = False
else:
    DEBUG = True

ADMIN_ENABLED = False

ALLOWED_HOSTS = ["*"]

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "index"

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "talerbank.app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "talerbank.app.middleware.ExceptionMiddleware",
    "talerbank.app.middleware.DecompressionMiddleware",
]

TEMPLATES = [{
    "BACKEND":
    "django.template.backends.jinja2.Jinja2",
    "DIRS": [
        os.path.join(BASE_DIR, "talerbank/app/templates"),
    ],
    "OPTIONS": {
        "environment": "talerbank.jinja2.environment",
        "context_processors": ["talerbank.jinja2.context_processor"],
    },
}]

# Disable those, since they don't work with
# jinja2 anyways.
TEMPLATE_CONTEXT_PROCESSORS = []

WSGI_APPLICATION = "talerbank.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {}

DBNAME = TC.value_string("bank", "database", required=True)
DBNAME = os.environ.get("TALER_BANK_ALTDB", DBNAME)

# Tells Django to add a BigAutoField column to every table that
# doesn't have a primary key explicitly defined.  Such column will
# then be the primary key.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DBNAME:
    raise Exception("DB not specified (neither in config or as" "cli argument)")

LOGGER.info("dbname: %s" % DBNAME)

CHECK_DBSTRING_FORMAT = re.search(
    r"[a-z]+:///[a-z]+([\?][a-z]+=[a-z/]+)?", DBNAME
)
if not CHECK_DBSTRING_FORMAT:
    LOGGER.error(
        "Bad db string given '%s', respect the format"
        "'dbtype:///dbname'" % DBNAME
    )
    sys.exit(2)

DBCONFIG = {}
# Maybe trust the parsing from urlparse?
DB_URL = urllib.parse.urlparse(DBNAME)

if DB_URL.scheme not in ("postgres") or DB_URL.scheme == "":
    LOGGER.error("DB '%s' is not supported" % DB_URL.scheme)
    sys.exit(1)
if DB_URL.scheme == "postgres":
    DBCONFIG["ENGINE"] = "django.db.backends.postgresql_psycopg2"
    DBCONFIG["NAME"] = DB_URL.path.lstrip("/")

if not DB_URL.netloc:
    P = urllib.parse.parse_qs(DB_URL.query)
    if ("host" not in P) or P["host"] == "":
        HOST = None
    else:
        HOST = P["host"][0]
else:
    HOST = DB_URL.netloc

if HOST:
    DBCONFIG["HOST"] = HOST  # Sockets directory.

DATABASES["default"] = DBCONFIG

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation"
        ".NumericPasswordValidator"
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "talerbank/app/static"),
]

STATIC_ROOT = None
ROOT_URLCONF = "talerbank.urls"

try:
    TALER_CURRENCY = TC.value_string("taler", "currency", required=True)
except ConfigurationError as exc:
    LOGGER.error(exc)
    sys.exit(3)

TALER_MAX_DEBT = TC.value_string(
    "bank", "MAX_DEBT", default="%s:50.0" % TALER_CURRENCY
)
TALER_MAX_DEBT_BANK = TC.value_string(
    "bank", "MAX_DEBT_BANK", default="%s:0.0" % TALER_CURRENCY
)

TALER_DIGITS = TC.value_int("bank", "NDIGITS", default=2)
# Order matters
TALER_PREDEFINED_ACCOUNTS = [
    "Bank",
    "Exchange",
    "blog",
    "Tor",
    "GNUnet",
    "Taler",
    "FSF",
    "Tutorial",
    "Survey",
]
TALER_EXPECTS_DONATIONS = ["Tor", "GNUnet", "Taler", "FSF"]
TALER_SUGGESTED_EXCHANGE = TC.value_string("bank", "suggested_exchange")
TALER_SUGGESTED_EXCHANGE_PAYTO = TC.value_string(
    "bank", "suggested_exchange_payto"
)

_allow_reg = TC.value_string("bank", "ALLOW_REGISTRATIONS", default="no")

if _allow_reg.lower() == "yes":
    ALLOW_REGISTRATIONS = True
else:
    ALLOW_REGISTRATIONS = False

_show_freeform_withdrawal = TC.value_string(
    "bank", "SHOW_FREEFORM_WITHDRAWAL", default="no"
)
if _show_freeform_withdrawal.lower() == "yes":
    SHOW_FREEFORM_WITHDRAWAL = True
else:
    SHOW_FREEFORM_WITHDRAWAL = False
