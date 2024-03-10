import sys
import logging
import pathlib
import argparse

from sentinel.version import VERSION

from sentinel.commands.fetch import FetchCommand
from sentinel.commands.launch import LaunchCommand
from sentinel.commands.abi_signatures import AbiSignaturesCommand


logger = logging.getLogger(__name__)


def run_cli_instance():
    """
    Run CLI instance
    """

    # Add current directory to python path
    sys.path.append(str(pathlib.Path.cwd()))

    # Common parser
    parser = argparse.ArgumentParser("sentinel")
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(help="Sentinel Commands")

    # Commands
    LaunchCommand(subparsers).add()
    FetchCommand(subparsers).add()
    AbiSignaturesCommand(subparsers).add()

    # Main
    args = parser.parse_args()

    if not hasattr(args, "handler"):
        parser.print_help()
        return

    args.handler(args)
