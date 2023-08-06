"""
CLI command for "package" command
"""

import click

from bsamcli.cli.main import pass_context, common_options
from bsamcli.commands.local.cli_common.options import template_common_option
from bsamcli.lib.samlib.cfc_command import execute_pkg_command


SHORT_HELP = "Package an CFC application."


# @click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.command("package", short_help=SHORT_HELP, 
    context_settings={"ignore_unknown_options": True, "help_option_names": [u'-h', u'--help']})#http://click.pocoo.org/5/api/#click.Context.ignore_unknown_options
@click.argument('function-name', required=False, default=None)
@template_common_option
@common_options
@pass_context
def cli(ctx, function_name, template):

    # All logic must be implemented in the ``do_cli`` method. This helps with easy unit testing

    do_cli(function_name, template)  # pragma: no cover


def do_cli(function_name, template):
    execute_pkg_command(function_name, template)
