"""
CLI command for "deploy" command
"""

import click

from bsamcli.cli.main import pass_context, common_options
from bsamcli.commands.local.cli_common.options import template_common_option
from bsamcli.lib.samlib.cfc_command import execute_deploy_command
from bsamcli.lib.samlib.cfc_deploy_conf import SUPPORTED_REGION


SHORT_HELP = "Deploy an CFC application"
@click.command("deploy", short_help=SHORT_HELP, context_settings={"ignore_unknown_options": True, "help_option_names": [u'-h', u'--help']})
@click.option('-r', "--region", type=click.Choice(SUPPORTED_REGION), help="Specify the region you want to deploy.")
@click.option("-e", "--endpoint", help="Deploy function to your custom service endpoint.")
@click.option("-c", "--only-config", is_flag=True, help="Only update function and trigger configurations.")
@click.argument('function-name', required=False, default=None)
@common_options
@template_common_option
@pass_context
def cli(ctx, function_name, region, endpoint, only_config, template):

    # All logic must be implemented in the ``do_cli`` method. This helps with easy unit testing

    do_cli(function_name, region, endpoint, only_config, template)  # pragma: no cover


def do_cli(function_name, region, endpoint, only_config, template):
    execute_deploy_command(function_name=function_name, region=region, endpoint=endpoint, 
        only_config=only_config, template=template)
