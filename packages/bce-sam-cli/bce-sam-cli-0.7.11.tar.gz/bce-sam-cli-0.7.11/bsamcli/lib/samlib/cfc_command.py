"""
Execution of package and deploy command
"""

import logging
import platform
import subprocess
import sys
import time
import base64
import os
import zipfile
import json

from bsamcli.lib.baidubce.services.cfc.cfc_client import CfcClient
from bsamcli.lib.baidubce.bce_client_configuration import BceClientConfiguration
from bsamcli.lib.baidubce.exception import BceServerError
from bsamcli.lib.baidubce.exception import BceHttpClientError

from bsamcli.commands.exceptions import UserException
from bsamcli.local.lambdafn.exceptions import FunctionNotFound
from bsamcli.commands.validate.lib.exceptions import InvalidSamDocumentException
from bsamcli.lib.samlib.cfc_credential_helper import get_credentials, get_region
from bsamcli.lib.samlib.cfc_deploy_conf import get_region_endpoint

from bsamcli.lib.samlib.deploy_context import DeployContext
from bsamcli.lib.samlib.user_exceptions import DeployContextException
from bsamcli.local.docker.cfc_container import Runtime

LOG = logging.getLogger(__name__)
_TEMPLATE_OPTION_DEFAULT_VALUE = "template.yaml"


def execute_pkg_command(function_name=None, template=None):
    try:
        with DeployContext(template_file=template,
                           function_identifier=function_name,
                           ) as context:
            for f in context.all_functions:
                codeuri = warp_codeuri(f)
                zip_up(codeuri, f.name, os.path.dirname(template))
    except FunctionNotFound as ex:
        raise UserException(ex)
    except InvalidSamDocumentException as ex:
        raise UserException(ex)


def execute_deploy_command(function_name=None, region=None, endpoint=None, 
    only_config=None, template=None):
    try:
        client_endpoint = None
        if endpoint is not None:
            client_endpoint = endpoint
        else:
            client_endpoint = get_region_endpoint(region)
        cfc_client = CfcClient(BceClientConfiguration(credentials=get_credentials(), endpoint=client_endpoint))
        
        with DeployContext(template_file=template,
                           function_identifier=function_name,
                           ) as context:
            for function in context.all_functions:
                do_deploy(context, cfc_client, function, only_config, template)
            
            LOG.info('Deploy done.')

    except FunctionNotFound as ex:
        raise UserException(ex)
    except InvalidSamDocumentException as ex:
        raise UserException(ex)

def do_deploy(context, cfc_client, function, only_config, template):
    validate_runtime(function.runtime)
    existed = check_if_exist(cfc_client, function.name)
    zip_dir = os.path.dirname(template)
    base64_file = get_function_base64_file(zip_dir, function.name)

    if existed:
        update_function(cfc_client, function, base64_file, only_config)
        # TODO update triggers when update
    else:
        create_function(cfc_client, function, base64_file)
        create_triggers(cfc_client, function, context)

def check_if_exist(cfc_client, function_name):
    try:
        get_function_response = cfc_client.get_function(function_name)
        LOG.debug("Get function response:%s", get_function_response)
    except (BceServerError, BceHttpClientError):
        LOG.debug("Get function exceptioned")
        return False

    return True


def create_function(cfc_client, function, base64_file):
    try:
        response = cfc_client.create_function(function.name, base64_file, function.properties)
        LOG.debug(response)        
        LOG.info("Function %s created.", function.name)
    except(BceServerError, BceHttpClientError) as e:
        if e.last_error.status_code == 403:
            LOG.error("Probably invalid AK/SK , check out ~/.bce/credential to find out...")
        else:
            raise UserException(e)

def update_function(cfc_client, function, base64_file, only_config):    
    try:
        if not only_config:
            cfc_client.update_function_code(function.name, zip_file=base64_file)
            LOG.info("Function %s code updated." % function.name)
        else:
            LOG.info("Skip update function %s code." % function.name)

        cfc_client.update_function_configuration(function.name,
                                                 function.properties)

        LOG.info("Function %s configuration updated." % function.name)

    except(BceServerError, BceHttpClientError) as e:
        if e.last_error.status_code == 403:
            LOG.info("Probably invalid AK/SK , check out ~/.bce/credential to find out...")
        else:
            raise UserException(str(e))


def get_function_base64_file(zip_dir, function_name):
    zipfile_name = function_name + '.zip'

    zipfile = os.path.join(zip_dir, zipfile_name)

    # 从 template.yaml 所在路径找
    if not os.path.exists(zipfile):
        raise DeployContextException("Zip file not found : {}".format(zipfile))

    with open(zipfile, 'rb') as fp:
        try:
            return base64.b64encode(fp.read()).decode("utf-8")
        except ValueError as ex:
            raise DeployContextException("Failed to convert zipfile to base64: {}".format(str(ex)))


def zip_up(code_uri, zipfile_name, target_dir):
    if code_uri is None:
        raise DeployContextException("Missing the file or the directory to zip up : {} is not valid".format(code_uri))

    target = os.path.join(target_dir, zipfile_name + '.zip')
    z = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)

    if os.path.isfile(code_uri):
        z.write(code_uri, os.path.basename(code_uri))
    else:
        for dirpath, dirnames, filenames in os.walk(code_uri):
            fpath = dirpath.replace(code_uri, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if 'site-packages' in fpath:
                    fpath = fpath.replace('site-packages/','')
                z.write(os.path.join(dirpath, filename), fpath + filename)

    LOG.info('%s zip suceeded!', zipfile_name)
    z.close()


def validate_runtime(func_runtime):
    if not Runtime.has_value(func_runtime):
        raise ValueError("Unsupported CFC runtime {}".format(func_runtime))
    return func_runtime


def create_triggers(cfc_client, function, context):
    func_config = cfc_client.get_function_configuration(function.name)
    LOG.debug("get function ret is: %s", func_config)

    try:
        context.deploy(cfc_client, func_config)
    except(BceServerError, BceHttpClientError) as e:
        raise UserException(str(e))


def warp_codeuri(f):
    LOG.debug("f.runtime is: %s", f.runtime)
    if f.runtime == "dotnetcore2.2":
        new_uri = os.path.join(f.codeuri, "bin", "Release", "netcoreapp2.2", "publish/")
        return new_uri
    return f.codeuri
