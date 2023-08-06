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
#  @file CLI tool to manage all the bank's tasks.

import argparse
import django
import sys
import os
import os.path
import site
import logging
import inspect
import click

from taler.util.talerconfig import TalerConfig
from django.core.management import call_command

SITE_PACKAGES = os.path.abspath(os.path.dirname(__file__) + "/..")

LOGGER = logging.getLogger(__name__)

# No perfect match to our logging format, but good enough ...
UWSGI_LOGFMT = "%(ltime) %(proto) %(method) %(uri) %(proto) => %(status)"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "talerbank.settings")

# Argument to tell uWSGI to load the python plugin.
# This hack is required, because on systems where the plugin is statically linked,
# loading it causes an error.
arg_load_python = "--if-not-plugin python --plugins python --endif".split(" ")


@click.group(help="Manager script of Taler bank.")
@click.pass_context
@click.option(
    "--http-port",
    help="Set HTTP as the serving protocol (taking precedence over the config.), and set the port.",
    type=int,
)
@click.option("-c", "--config", help="Path to the config file.")
@click.option("--with-db", help="Database connection string.")
def cli(ctx, http_port, config, with_db):
    if with_db:
        os.environ.setdefault("TALER_BANK_ALTDB", with_db)
    if config:
        os.environ["TALER_CONFIG_FILE"] = config

    ctx.obj = dict(http_port=http_port, config=config)


@cli.command(help="Serve the bank")
@click.pass_obj
def serve(obj):
    # if --http-port option is found, then serve via HTTP.
    # Otherwise serve on whatever protocol is specified in the config.
    serve = "http"
    if not obj["http_port"]:
        TC = TalerConfig.from_file(os.environ.get("TALER_CONFIG_FILE"))
        serve = TC["bank"]["serve"].value_string(required=True).lower()

    if serve == "http":
        return handle_serve_http(obj["http_port"])
    handle_serve_uwsgi()


@cli.command(
    name="django",
    help="Invoke 'django' sub-commands",
    context_settings=dict(ignore_unknown_options=True),
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def handle_django(args):
    django.setup()
    # always run 'migrate' first, in case a virgin db is being used.
    call_command("migrate")
    django_index = sys.argv.index("django")
    from django.core.management import execute_from_command_line

    execute_from_command_line([sys.argv[0] + " django"] + sys.argv[django_index + 1 :])


def handle_serve_http(port):
    import django

    django.setup()
    print("migrating")
    call_command("migrate")
    print("providing accounts")
    call_command("provide_accounts")
    print("checking")
    call_command("check")
    if port is None:
        TC = TalerConfig.from_file(os.environ.get("TALER_CONFIG_FILE"))
        port = TC["bank"]["http_port"].value_int(required=True)

    httpspec = ":%d" % (port,)
    params = [
        "uwsgi",
        "uwsgi",
        *arg_load_python,
        "--static-map",
        "/static=%s/talerbank/app/static" % SITE_PACKAGES,
        "--die-on-term",
        "--no-orphans",
        "--master",
        "--http",
        httpspec,
        "--log-format",
        UWSGI_LOGFMT,
        "--module",
        "talerbank.wsgi",
    ]
    os.execlp(*params)


def handle_serve_uwsgi():
    django.setup()
    call_command("migrate")
    call_command("provide_accounts")
    call_command("check")
    TC = TalerConfig.from_file(os.environ.get("TALER_CONFIG_FILE"))
    serve_uwsgi = TC["bank"]["uwsgi_serve"].value_string(required=True).lower()
    params = [
        "uwsgi",
        "uwsgi",
        *arg_load_python,
        "--static-map",
        "/static=%s/talerbank/app/static" % SITE_PACKAGES,
        "--die-on-term",
        "--no-orphans",
        "--master",
        "--log-format",
        UWSGI_LOGFMT,
        "--module",
        "talerbank.wsgi",
    ]
    if serve_uwsgi == "tcp":
        port = TC["bank"]["uwsgi_port"].value_int(required=True)
        spec = ":%d" % (port,)
        params.extend(["--socket", spec])
    else:
        spec = TC["bank"]["uwsgi_unixpath"].value_filename(required=True)
        mode = TC["bank"]["uwsgi_unixpath_mode"].value_filename(required=True)
        params.extend(["--socket", spec])
        params.extend(["--chmod-socket=" + mode])
        try:
            os.makedirs(os.path.dirname(spec), exist_ok=True)
        except FileNotFoundError:
            print(f"{spec} is not a valid file path.")
            sys.exit(1)
    logging.info("launching uwsgi with argv %s", params[1:])
    os.execlp(*params)


@cli.command(help="Print config values.")
def config():
    TC = TalerConfig.from_file(os.environ.get("TALER_CONFIG_FILE"))
    TC.dump()

def run():
    cli()

if __name__ == "__main__":
    cli()
