##
# This file is part of TALER
# (C) 2017 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3, or (at your option) any later version.
#
# TALER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with TALER; see the file COPYING.  If not,
# see <http://www.gnu.org/licenses/>
#
#  @author Florian Dold
#  @brief Extends the Jinja2 API with custom functions.

import os
import math
import json
from urllib.parse import urlparse
from django.urls import reverse, get_script_prefix
from django.conf import settings
from jinja2 import Environment
from django.utils.translation import gettext
import markupsafe


##
# Check if a URL is absolute or not.
#
# @param urloc the URL to check.
# @return True if the URL is absolute, False otherwise.
def is_absolute(urloc):
    return bool(urlparse(urloc).netloc)


##
# Join URL components held in a list, taking care
# of not having double slashes in the result.
#
# @param parts list of URL components.
# @return the string made of the joined components
def join_urlparts(*parts):
    ret = ""
    part = 0
    while part < len(parts):
        buf = parts[part]
        part += 1
        if ret.endswith("/"):
            buf = buf.lstrip("/")
        elif ret and not buf.startswith("/"):
            buf = "/" + buf
        ret += buf
    return ret


##
# Prefixes the argument with the location for static content.
#
# @param urloc the URL portion that should be prefixed; in
#        other words, this will be in final position in the
#        produced result.
# @return the URL that picks @a urloc from the location for
#         static content.
def static(urloc):
    if is_absolute(urloc):
        return urloc
    return join_urlparts(get_script_prefix(), settings.STATIC_URL, urloc)


##
# Helper function that fetches a value from the settings.
#
# @param name the name to lookup in the settings.
# @return @a name's value as defined in the settings, or
#         a empty string otherwise.
def settings_value(name):
    return getattr(settings, name, "")


##
# Fetch the URL given its "name".
#
# @param url_name URL's name as defined in urlargs.py
# @param kwargs key-value list that will be appended
#        to the URL as the parameter=value pairs.
def url(url_name, *args, **kwargs):
    # strangely, Django's 'reverse' function
    # takes a named parameter 'kwargs' instead
    # of real kwargs.
    return reverse(url_name, args=args, kwargs=kwargs)


##
# Helper function that reads a value from the environment.
#
# @param name env value to read
# @return the value, or None if not found.
def env_get(name, default=None):
    return os.environ.get(name, default)


##
# Jinja2 specific function used to activate the definitions
# of this module.
#
# @param options opaque argument (?) given from the caller.
# @return Jinja2-specific object that contains the new definitions.
def is_valid_amount(amount):
    if math.isnan(amount.value):
        return False
    return True


def tojson(x):
    """Convert object to json"""
    return json.dumps(x)


##
# Stringifies amount.
#
# @param amount amount object.
# @return amount pretty string.
def amount_stringify(amount):
    return amount.stringify(settings.TALER_DIGITS, pretty=True)


def get_locale(url):
    parts = url.split('/', 2)
    if (2 >= len(parts)):
        # Totally unexpected path format, do not localize
        return "en"
    lang = parts[1]
    return lang


all_languages = {
    "en": "English&nbsp;[en]",
    "ar": "Arabic&nbsp;[ar]",
    "zh_Hant": "Chinese&nbsp;[zh]",
    "fr": "French&nbsp;[fr]",
    "de": "German&nbsp;[de]",
    "hi": "Hindi&nbsp;[hi]",
    "it": "Italian&nbsp;[it]",
    "ja": "Japanese&nbsp;[ja]",
    "ko": "Korean&nbsp;[ko]",
    "pt": "Portuguese&nbsp;[pt]",
    "pt_BR": "Portuguese (Brazil)&nbsp;[pt_BR]",
    "ru": "Russian&nbsp;[ru]",
    "es": "Spanish&nbsp;[es]",
    "sv": "Swedish&nbsp;[sv]",
    "tr": "Turkish&nbsp;[tr]",
}


def context_processor(request):
    def getlang():
        return get_locale(request.path)

    return dict(getlang=getlang)


def environment(**options):
    env = Environment(**options)

    gettext_markup = lambda *args, **kwargs: markupsafe.Markup(
        gettext(*args, **kwargs)
    )

    env.globals.update({
        "static": static,
        "url": url,
        "settings_value": settings_value,
        "env": env_get,
        "is_valid_amount": is_valid_amount,
        "amount_stringify": amount_stringify,
        "tojson": tojson,
        "_": gettext_markup,
        "gettext": gettext_markup,
        "get_locale": get_locale,
        "getactive": lambda: "bank",
        "all_languages": all_languages,
    })
    return env
