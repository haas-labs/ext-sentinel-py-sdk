import json
import argparse

from typing import List

import sentinel

from sentinel.commands.common import SentinelCommand
from sentinel.utils.version import component_versions


class Command(SentinelCommand):
    def syntax(self) -> str:
        return "[-v]"

    def description(self) -> str:
        return "Print Sentinel version and required libs"

    def add_options(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--all",
            dest="all",
            action="store_true",
            help="also display python/platform/libs info (useful for bug reporting)",
        )

    def run(self, opts: List[str], args: argparse.Namespace) -> None:
        if args.all:
            versions = component_versions()
            print(json.dumps(versions))
        else:
            print(json.dumps({"Sentinel": sentinel.version.VERSION}))
