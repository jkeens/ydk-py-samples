#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Execute RPC for model ietf-netconf-monitoring.

usage: nc-execute-ietf-netconf-monitoring-22-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import ExecutorService
from ydk.providers import NetconfServiceProvider
from ydk.models.ietf import ietf_netconf_monitoring \
    as ietf_netconf_monitoring
import logging


def prepare_get_schema_rpc(get_schema_rpc):
    """Add RPC input data to get_schema_rpc object."""
    get_schema_rpc.input.identifier = "openconfig-interfaces"
    get_schema_rpc.input.version = "2015-11-20"


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create executor service
    executor = ExecutorService()

    get_schema_rpc = ietf_netconf_monitoring.GetSchemaRpc()  # create object
    prepare_get_schema_rpc(get_schema_rpc)  # add RPC input

    # execute RPC on NETCONF device
    print(executor.execute_rpc(provider, get_schema_rpc))

    provider.close()
    exit()
# End of script
