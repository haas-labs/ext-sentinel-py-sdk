
import logging
import argparse

from sentinel.commands.fetch import FetchCommand
from sentinel.commands.mixers import MixersCommand
from sentinel.commands.launch import LaunchCommand
from sentinel.commands.chainlist import ChainListCommand
from sentinel.commands.abi_signatures import AbiSignaturesCommand
# from sentinel.commands.monitored_contracts import MonitoredContractsCommand

logger = logging.getLogger(__name__)

# Exit codes
EXITCODE_MISSED_REQUIRED_ARGUMENTS = 1
EXITCODE_INTERRUPTED_BY_USER = 2


def run_cli_instance():
    '''
    Run CLI instance
    '''
    # Common parser
    parser = argparse.ArgumentParser('sentinel')
    subparsers = parser.add_subparsers(help='Sentinel Commands')

    # Commands
    LaunchCommand(subparsers).add()
    FetchCommand(subparsers).add()
    ChainListCommand(subparsers).add()
    MixersCommand(subparsers).add()
    AbiSignaturesCommand(subparsers).add()
    # MonitoredContractsCommand(subparsers).add()
    
    # Main
    args = parser.parse_args()

    if not hasattr(args, 'handler'):
        parser.print_help()
        return

    args.handler(args)
