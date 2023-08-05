from typing import Optional, Sequence, List
import os
import argparse
import json
import sys
from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Depends, Security, Request
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader
from fastapi.responses import Response
from starlette import status
import uuid
import inspect
import logging
import uvicorn

from suzieq.sqobjects import get_sqobject
from suzieq.utils import (load_sq_config, get_sq_install_dir, get_log_params,
                          sq_get_config_file)

API_KEY_NAME = 'access_token'

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def check_config_file():
    if not getattr(app, 'cfg_file', None):
        print('missing config file')
        sys.exit(1)


# Changing the default URLs to help with reverse proxy stuff as described
# in issue #381 (https://github.com/netenglabs/suzieq/issues/381)
app = FastAPI(on_startup=[check_config_file],
              openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc")


def app_init(cfg_file):
    '''This is the actual API initilaizer'''
    global app

    app.cfg_file = cfg_file

    return app


def get_configured_api_key():
    cfg = load_sq_config(config_file=app.cfg_file)
    try:
        api_key = cfg['rest']['API_KEY']
    except KeyError:
        print('missing API_KEY in config file')
        sys.exit(1)

    return api_key


async def get_api_key(api_key_query: str = Security(api_key_query),
                      api_key_header: str = Security(api_key_header)):

    api_key = get_configured_api_key()
    if api_key_query == api_key:
        return api_key_query
    elif api_key_header == api_key:
        return api_key_header
    else:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


def get_cert_files(cfg):
    sqdir = get_sq_install_dir()
    ssl_certfile = cfg.get('rest', {}) \
                      .get('rest-certfile', f'{sqdir}/config/etc/cert.pem')

    ssl_keyfile = cfg.get('rest', {}) \
                     .get('rest-keyfile', f'{sqdir}/config/etc/key.pem')

    if not os.path.isfile(ssl_certfile):
        print(f"ERROR: Missing certificate file: {ssl_certfile}")
        sys.exit(1)

    if not os.path.isfile(ssl_keyfile):
        print(f"ERROR: Missing certificate file: {ssl_keyfile}")
        sys.exit(1)

    return ssl_keyfile,  ssl_certfile


def get_log_config_level(cfg):

    logfile, loglevel, logsize, log_stdout = get_log_params(
        'rest', cfg, '/tmp/sq-rest-server.log')

    log_config = uvicorn.config.LOGGING_CONFIG
    if logfile and not log_stdout:
        log_config['handlers']['access']['filename'] = logfile
        log_config['handlers']['access']['class'] = 'logging.handlers.RotatingFileHandler'
        log_config['handlers']['access']['maxBytes'] = logsize
        log_config['handlers']['access']['backupCount'] = 2

        log_config['handlers']['default']['class'] = 'logging.handlers.RotatingFileHandler'
        log_config['handlers']['default']['maxBytes'] = logsize
        log_config['handlers']['default']['backupCount'] = 2
        log_config['handlers']['default']['filename'] = logfile

        if 'stream' in log_config['handlers']['default']:
            del log_config['handlers']['default']['stream']
            del log_config['handlers']['access']['stream']

    return log_config, loglevel


def rest_main(*args) -> None:
    """The main function for the REST server

    Args:
        config_file (str): The suzieq config file
        no_https (bool): If true, disable https
    """

    if not args:
        args = sys.argv

    parser = argparse.ArgumentParser(args)
    parser.add_argument(
        "-c",
        "--config",
        type=str, help="alternate config file",
        default=None
    )
    parser.add_argument(
        "--no-https",
        help="Turn off HTTPS",
        default=False, action='store_true',
    )
    userargs = parser.parse_args()

    config_file = sq_get_config_file(userargs.config)
    app = app_init(config_file)
    cfg = load_sq_config(config_file=config_file)
    try:
        api_key = cfg['rest']['API_KEY']
    except KeyError:
        print('missing API_KEY in config file')
        exit(1)

    logcfg, loglevel = get_log_config_level(cfg)

    no_https = cfg.get('rest', {}).get('no-https', False) or userargs.no_https

    srvr_addr = cfg.get('rest', {}).get('address', '127.0.0.1')
    srvr_port = cfg.get('rest', {}).get('port', 8000)

    if no_https:
        uvicorn.run(app, host=srvr_addr, port=srvr_port,
                    )
    else:
        ssl_keyfile, ssl_certfile = get_cert_files(cfg)
        uvicorn.run(app, host=srvr_addr, port=srvr_port,
                    ssl_keyfile=ssl_keyfile,
                    ssl_certfile=ssl_certfile)


"""
each of these read functions behaves the same, it gets the arguments
puts them into dicts and passes them to sqobjects

assume that all API functions are named read_*
"""


class CommonVerbs(str, Enum):
    show = "show"
    summarize = "summarize"
    unique = "unique"
    top = "top"


class RouteVerbs(str, Enum):
    show = "show"
    summarize = "summarize"
    unique = "unique"
    lpm = "lpm"
    top = "top"


class TableVerbs(str, Enum):
    show = "show"
    summarize = "summarize"
    unique = "unique"
    top = "top"
    describe = "describe"


class DeviceStatus(str, Enum):
    alive = "alive"
    dead = "dead"
    neverpoll = "neverpoll"


class BgpStateValues(str, Enum):
    ESTABLISHED = "Established"
    NOTESTD = "NotEstd"


class IfStateValues(str, Enum):
    UP = "up"
    DOWN = "down"
    ERRDISABLED = "errDisabled"
    NOTCONNECTED = "notConnected"


class OspfStateValues(str, Enum):
    FULL = "full"
    PASSIVE = "passive"
    OTHER = "other"


class ViewValues(str, Enum):
    latest = "latest"
    all = "all"
    changes = "changes"


class AssertStatusValues(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    ALL = "all"


class InventoryStatusValues(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"


# The logic in the code below is that you have a common function to
# split the common arguments across all the functions, and split the
# object-specific arguments in the object function itself.
@app.get("/api/v1/{rest_of_path:path}", deprecated=True)
async def deprecated_function(request: Request, rest_of_path: str):
    return([{'error': 'v1 is deprecated, use API version v2'}])


@app.get("/api/v2/address/{verb}")
async def query_address(verb: CommonVerbs, request: Request,
                        token: str = Depends(get_api_key),
                        format: str = None,
                        hostname: List[str] = Query(None),
                        start_time: str = "", end_time: str = "",
                        view: ViewValues = "latest",
                        namespace: List[str] = Query(None),
                        columns: List[str] = Query(default=["default"]),
                        address: List[str] = Query(None),
                        ipvers: str = None, what: str = None,
                        vrf: str = None, query_str: str = None,
                        ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/arpnd/{verb}")
async def query_arpnd(verb: CommonVerbs, request: Request,
                      token: str = Depends(get_api_key),
                      format: str = None,
                      hostname: List[str] = Query(None),
                      start_time: str = "", end_time: str = "",
                      view: ViewValues = "latest",
                      namespace: List[str] = Query(None),
                      columns: List[str] = Query(default=["default"]),
                      ipAddress: List[str] = Query(None),
                      macaddr: List[str] = Query(None),
                      oif: List[str] = Query(None),
                      query_str: str = None, what: str = None,
                      ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/bgp/assert")
async def query_bgp_assert(request: Request,
                           token: str = Depends(get_api_key),
                           format: str = None,
                           hostname: List[str] = Query(None),
                           start_time: str = "", end_time: str = "",
                           view: ViewValues = "latest",
                           namespace: List[str] = Query(None),
                           columns: List[str] = Query(default=["default"]),
                           vrf: List[str] = Query(None),
                           status: AssertStatusValues = Query(None),
                           query_str: str = None,
                           ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "assert", request, locals())


@ app.get("/api/v2/bgp/{verb}")
async def query_bgp(verb: CommonVerbs, request: Request,
                    token: str = Depends(get_api_key),
                    format: str = None,
                    hostname: List[str] = Query(None),
                    start_time: str = "", end_time: str = "",
                    view: ViewValues = "latest",
                    namespace: List[str] = Query(None),
                    columns: List[str] = Query(default=["default"]),
                    peer: List[str] = Query(None),
                    state: BgpStateValues = Query(None),
                    vrf: List[str] = Query(None),
                    asn: List[str] = Query(None),
                    status: AssertStatusValues = Query(None),
                    query_str: str = None, what: str = None,
                    ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/device/{verb}")
async def query_device(verb: CommonVerbs, request: Request,
                       token: str = Depends(get_api_key),
                       format: str = None,
                       hostname: List[str] = Query(None),
                       start_time: str = "", end_time: str = "",
                       view: ViewValues = "latest",
                       namespace: List[str] = Query(None),
                       columns: List[str] = Query(default=["default"]),
                       query_str: str = None,
                       os: List[str] = Query(None),
                       vendor: List[str] = Query(None),
                       model: List[str] = Query(None),
                       version: str = "", what: str = None,
                       status: List[DeviceStatus] = Query(None),
                       ):
    function_name = inspect.currentframe().f_code.co_name
    if status:
        status = [x.value for x in status]  # convert enum to string
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/devconfig/{verb}")
async def query_devconfig(verb: CommonVerbs, request: Request,
                          token: str = Depends(get_api_key),
                          format: str = None,
                          hostname: List[str] = Query(None),
                          start_time: str = "", end_time: str = "",
                          view: ViewValues = "latest",
                          namespace: List[str] = Query(None),
                          columns: List[str] = Query(default=["default"]),
                          query_str: str = None,
                          ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/evpnVni/assert")
async def query_evpnVni_assert(request: Request,
                               token: str = Depends(get_api_key),
                               format: str = None,
                               hostname: List[str] = Query(None),
                               start_time: str = "", end_time: str = "",
                               view: ViewValues = "latest",
                               namespace: List[str] = Query(None),
                               columns: List[str] = Query(default=["default"]),
                               status: AssertStatusValues = None,
                               query_str: str = None, 
                               ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "assert", request, locals())


@ app.get("/api/v2/evpnVni/{verb}")
async def query_evpnVni(verb: CommonVerbs, request: Request,
                        token: str = Depends(get_api_key),
                        format: str = None,
                        hostname: List[str] = Query(None),
                        start_time: str = "", end_time: str = "",
                        view: ViewValues = "latest",
                        namespace: List[str] = Query(None),
                        columns: List[str] = Query(default=["default"]),
                        vni: List[str] = Query(None),
                        priVtepIp: List[str] = Query(None),
                        status: AssertStatusValues = None,
                        query_str: str = None, what: str = None,
                        ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/fs/{verb}")
async def query_fs(verb: CommonVerbs, request: Request,
                   token: str = Depends(get_api_key),
                   format: str = None,
                   hostname: List[str] = Query(None),
                   start_time: str = "", end_time: str = "",
                   view: ViewValues = "latest",
                   namespace: List[str] = Query(None),
                   columns: List[str] = Query(default=["default"]),
                   mountPoint: List[str] = Query(None), what: str = None,
                   usedPercent: str = None, query_str: str = None,
                   ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/interface/assert")
async def query_interface_assert(request: Request,
                                 token: str = Depends(get_api_key),
                                 format: str = None,
                                 hostname: List[str] = Query(None),
                                 start_time: str = "", end_time: str = "",
                                 view: ViewValues = "latest",
                                 namespace: List[str] = Query(None),
                                 columns: List[str] = Query(default=["default"]),
                                 ifname: List[str] = Query(None),
                                 what: str = None,
                                 matchval: int = Query(None, alias="value"),
                                 status: AssertStatusValues = Query(None),
                                 ignore_missing_peer: bool = Query(False),
                                 query_str: str = None,
                                 ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "assert", request, locals())


@ app.get("/api/v2/interface/{verb}")
async def query_interface(verb: CommonVerbs, request: Request,
                          token: str = Depends(get_api_key),
                          format: str = None,
                          hostname: List[str] = Query(None),
                          start_time: str = "", end_time: str = "",
                          view: ViewValues = "latest",
                          namespace: List[str] = Query(None),
                          columns: List[str] = Query(default=["default"]),
                          ifname: List[str] = Query(None),
                          state: IfStateValues = Query(None),
                          type: List[str] = Query(None),
                          what: str = None, vrf: List[str] = Query(None),
                          master: List[str] = Query(None),
                          mtu: List[str] = Query(None),
                          ifindex: List[str] = Query(None),
                          matchval: int = Query(None, alias="value"),
                          status: AssertStatusValues = Query(None),
                          ignore_missing_peer: bool = Query(False),
                          query_str: str = None,
                          ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@app.get("/api/v2/inventory/{verb}")
async def query_inventory(verb: CommonVerbs, request: Request,
                          token: str = Depends(get_api_key),
                          format: str = None,
                          hostname: List[str] = Query(None),
                          start_time: str = "", end_time: str = "",
                          view: ViewValues = "latest",
                          namespace: List[str] = Query(None),
                          columns: List[str] = Query(default=["default"]),
                          query_str: str = None,
                          type: List[str] = Query(None),
                          serial: List[str] = Query(None),
                          model: List[str] = Query(None),
                          vendor: List[str] = Query(None), what: str = None,
                          status: InventoryStatusValues = Query(None),
                          ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/lldp/{verb}")
async def query_lldp(verb: CommonVerbs, request: Request,
                     token: str = Depends(get_api_key),
                     format: str = None,
                     hostname: List[str] = Query(None),
                     start_time: str = "", end_time: str = "",
                     view: ViewValues = "latest",
                     namespace: List[str] = Query(None),
                     columns: List[str] = Query(default=["default"]),
                     ifname: List[str] = Query(None),
                     query_str: str = None, what: str = None,
                     ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/mac/{verb}")
async def query_mac(verb: CommonVerbs, request: Request,
                    token: str = Depends(get_api_key),
                    format: str = None,
                    hostname: List[str] = Query(None),
                    start_time: str = "", end_time: str = "",
                    view: ViewValues = "latest",
                    namespace: List[str] = Query(None),
                    columns: List[str] = Query(default=["default"]),
                    bd: str = None,
                    localOnly: str = None,
                    macaddr: List[str] = Query(None),
                    remoteVtepIp: List[str] = Query(None),
                    vlan: List[str] = Query(None),
                    query_str: str = None, what: str = None,
                    moveCount: str = None,
                    ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/mlag/{verb}")
async def query_mlag(verb: CommonVerbs, request: Request,
                     token: str = Depends(get_api_key),
                     format: str = None,
                     hostname: List[str] = Query(None),
                     start_time: str = "", end_time: str = "",
                     view: ViewValues = "latest",
                     namespace: List[str] = Query(None),
                     columns: List[str] = Query(default=["default"]),
                     query_str: str = None, what: str = None,
                     ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@app.get("/api/v2/network/find")
async def query_network_find(request: Request,
                             token: str = Depends(get_api_key),
                             format: str = None,
                             columns: List[str] = Query(default=["default"]),
                             namespace: List[str] = Query(None),
                             hostname: List[str] = Query(None),
                             start_time: str = "", end_time: str = "",
                             view: ViewValues = "latest",
                             address: str = "", vlan: str = '', vrf: str = '',
                             resolve_bond: bool = False,
                             asn: str = '',
                             query_str: str = None,
                             ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "find", request, locals())


@app.get("/api/v2/network/{verb}")
async def query_network(verb: CommonVerbs, request: Request,
                        token: str = Depends(get_api_key),
                        format: str = None,
                        columns: List[str] = Query(default=["default"]),
                        namespace: List[str] = Query(None),
                        hostname: List[str] = Query(None),
                        start_time: str = "", end_time: str = "",
                        version: str = "",
                        view: ViewValues = "latest",
                        model: List[str] = Query(None),
                        vendor: List[str] = Query(None),
                        os: List[str] = Query(None),
                        query_str: str = None, what: str = None,
                        ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/ospf/assert")
async def query_ospf_assert(request: Request,
                            token: str = Depends(get_api_key),
                            format: str = None,
                            hostname: List[str] = Query(None),
                            start_time: str = "", end_time: str = "",
                            view: ViewValues = "latest",
                            namespace: List[str] = Query(None),
                            columns: List[str] = Query(default=["default"]),
                            vrf: List[str] = Query(None),
                            status: AssertStatusValues = None,
                            query_str: str = None,
                            ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "assert", request, locals())


@ app.get("/api/v2/ospf/{verb}")
async def query_ospf(verb: CommonVerbs, request: Request,
                     token: str = Depends(get_api_key),
                     format: str = None,
                     hostname: List[str] = Query(None),
                     start_time: str = "", end_time: str = "",
                     view: ViewValues = "latest",
                     namespace: List[str] = Query(None),
                     columns: List[str] = Query(default=["default"]),
                     ifname: List[str] = Query(None),
                     state: OspfStateValues = Query(None),
                     vrf: List[str] = Query(None),
                     status: AssertStatusValues = None,
                     query_str: str = None, what: str = None,
                     ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/path/{verb}")
async def query_path(verb: CommonVerbs, request: Request,
                     token: str = Depends(get_api_key),
                     format: str = None,
                     hostname: List[str] = Query(None),
                     start_time: str = "", end_time: str = "",
                     view: ViewValues = "latest",
                     namespace: List[str] = Query(None),
                     columns: List[str] = Query(default=["default"]),
                     vrf: str = None,
                     dest: str = None,
                     source: str = Query(None, alias="src"),
                     query_str: str = None, what: str = None,
                     ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/route/{verb}")
async def query_route(verb: RouteVerbs, request: Request,
                      token: str = Depends(get_api_key),
                      format: str = None,
                      hostname: List[str] = Query(None),
                      start_time: str = "", end_time: str = "",
                      view: ViewValues = "latest",
                      namespace: List[str] = Query(None),
                      columns: List[str] = Query(default=["default"]),
                      prefix: List[str] = Query(None),
                      vrf: List[str] = Query(None),
                      protocol: List[str] = Query(None),
                      prefixlen: str = None, ipvers: str = None,
                      add_filter: str = None, address: str = None,
                      query_str: str = None, what: str = None,
                      ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/sqPoller/{verb}")
async def query_sqPoller(verb: CommonVerbs, request: Request,
                         token: str = Depends(get_api_key),
                         format: str = None,
                         hostname: List[str] = Query(None),
                         start_time: str = "", end_time: str = "",
                         view: ViewValues = "latest",
                         namespace: List[str] = Query(None),
                         columns: List[str] = Query(default=["default"]),
                         service: str = None,
                         status: AssertStatusValues = Query(None),
                         query_str: str = None, what: str = None,
                         ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/topology/summarize")
async def query_topology_summarize(request: Request,
                                   token: str = Depends(get_api_key),
                                   format: str = None,
                                   hostname: List[str] = Query(None),
                                   start_time: str = "", end_time: str = "",
                                   view: ViewValues = "latest",
                                   namespace: List[str] = Query(None),
                                   columns: List[str] = Query(default=["default"]),
                                   via: List[str] = Query(None),
                                   query_str: str = None,
                                   ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, "summarize", request, locals())


@ app.get("/api/v2/topology/{verb}")
async def query_topology(verb: CommonVerbs, request: Request,
                         token: str = Depends(get_api_key),
                         format: str = None,
                         hostname: List[str] = Query(None),
                         start_time: str = "", end_time: str = "",
                         view: ViewValues = "latest",
                         namespace: List[str] = Query(None),
                         columns: List[str] = Query(default=["default"]),
                         polled: str = None,
                         via: List[str] = Query(None),
                         ifname: List[str] = Query(None),
                         peerHostname: List[str] = Query(None),
                         query_str: str = None, what: str = None,
                         ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/vlan/{verb}")
async def query_vlan(verb: CommonVerbs, request: Request,
                     token: str = Depends(get_api_key),
                     format: str = None,
                     hostname: List[str] = Query(None),
                     start_time: str = "", end_time: str = "",
                     view: ViewValues = "latest",
                     namespace: List[str] = Query(None),
                     columns: List[str] = Query(default=["default"]),
                     vlan: List[str] = Query(None),
                     state: str = None,
                     vlanName: List[str] = Query(None),
                     query_str: str = None, what: str = None,
                     ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


@ app.get("/api/v2/table/{verb}")
async def query_table(verb: TableVerbs, request: Request,
                      token: str = Depends(get_api_key),
                      format: str = None,
                      hostname: List[str] = Query(None),
                      start_time: str = "", end_time: str = "",
                      view: ViewValues = "latest", namespace: List[str] = Query(None),
                      columns: List[str] = Query(default=["default"]),
                      query_str: str = None
                      ):
    function_name = inspect.currentframe().f_code.co_name
    return read_shared(function_name, verb, request, locals())


def read_shared(function_name, verb, request, local_variables=None):
    """all the shared code for each of thse read functions"""

    command = function_name.split('_')[1]  # assumes fn name is query_<command>
    command_args, verb_args = create_filters(function_name, command, request,
                                             local_variables)

    verb = cleanup_verb(verb)

    columns = local_variables.get('columns', None)
    format = local_variables.get('format', None)
    ret, svc_inst = run_command_verb(
        command, verb, command_args, verb_args, columns, format)

    return ret


def create_filters(function_name, command, request, local_vars):
    command_args = {}
    verb_args = {}
    remove_args = ['verb', 'token', 'format', 'request', 'access_token']
    all_cmd_args = ['namespace', 'hostname',
                    'start_time', 'end_time', 'view', 'columns', 'format']
    both_verb_and_command = ['namespace', 'hostname', ]
    alias_args = {'src': 'source'}
    def_val_args = {
        'namespace': [],
        'hostname': [],
    }

    query_ks = request.query_params
    for arg in query_ks.keys():
        if arg in remove_args:
            continue
        if arg in alias_args:
            tryarg = alias_args[arg]
        else:
            tryarg = arg
        if arg in all_cmd_args:
            if query_ks.get(arg) is not None:
                command_args[tryarg] = local_vars.get(tryarg, None)
                if arg in both_verb_and_command:
                    verb_args[tryarg] = command_args[arg]
        else:
            if query_ks.get(arg) is not None:
                verb_args[tryarg] = local_vars.get(tryarg, None)

    return command_args, verb_args


def cleanup_verb(verb):
    if verb == 'show':
        verb = 'get'
    if verb == 'assert':
        verb = 'aver'
    return verb


def create_command_args(hostname='', start_time='', end_time='', view='latest',
                        namespace='', columns='default'):
    command_args = {'hostname': hostname,
                    'start_time': start_time,
                    'end_time': end_time,
                    'view': view,
                    'namespace': namespace,
                    'columns': columns}
    return command_args


def get_svc(command):
    """based on the command, find the module and service that the command is in
    return the service
    """
    command_name = command

    svc = get_sqobject(command_name)
    return svc


def run_command_verb(command, verb, command_args, verb_args, columns=['default'], format=None):
    """
    Runs the command and verb with the command_args and verb_args as dictionaries

    HTTP Return Codes
        404 -- Missing command or argument (including missing valid path)
        405 -- Missing or incorrect query parameters
        422 -- FastAPI validation errors
        500 -- Exceptions
    """
    svc = get_svc(command)
    try:
        svc_inst = svc(**command_args, config_file=app.cfg_file)
        df = getattr(svc_inst, verb)(**verb_args)

    except AttributeError as err:
        return_error(
            404, f"{verb} not supported for {command} or missing arguement: {err}")

    except NotImplementedError as err:
        return_error(404, f"{verb} not supported for {command}: {err}")

    except TypeError as err:
        return_error(405, f"bad keyword/filter for {command} {verb}: {err}")

    except ValueError as err:
        return_error(405, f"bad keyword/filter for {command} {verb}: {err}")

    except Exception as err:
        return_error(
            500, f"exceptional exception {verb} for {command} of type {type(err)}: {err}")

    if df.columns.to_list() == ['error']:
        return_error(
            405, f"bad keyword/filter for {command} {verb}: {df['error'][0]}")

    if columns != ['default'] and columns != ['*'] and columns is not None:
        df = df[columns]

    if format == 'markdown':
        # have to return a Reponse so that it won't turn the markdown into JSON
        return Response(content=df.to_markdown()), svc_inst

    if verb == 'summarize':
        json_orient = 'columns'
    else:
        json_orient = 'records'
    return json.loads(df.to_json(orient=json_orient)), svc_inst


def return_error(code: int, msg: str):
    u = uuid.uuid1()
    msg = f"{msg} id={u}"
    logger = logging.getLogger('uvicorn')
    logger.info(msg)
    raise HTTPException(status_code=code, detail=msg)


@ app.get("/api/v2/{command}", include_in_schema=False)
def missing_verb(command):
    return_error(
        404, f'{command} command missing a verb. for example '
        f'/api/v2/{command}/show')


@ app.get("/", include_in_schema=False)
def bad_path():
    return_error(
        404, "bad path. Try something like '/api/v2/device/show' or '/api/docs'")
