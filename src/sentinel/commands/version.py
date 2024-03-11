import json
import argparse

from typing import List

import rich
import sentinel

from sentinel.commands.common import SentinelCommand
from sentinel.utils.version import component_versions


class Command(SentinelCommand):
    def syntax(self) -> str:
        return "[--all]"

    def description(self) -> str:
        return "Print Sentinel version and required libs"

    def add_options(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--all",
            dest="all",
            action="store_true",
            help="also display python/platform/libs info (useful for bug reporting)",
        )
        parser.add_argument(
            "--pretty",
            dest="pretty",
            action="store_true",
            help="Prettify JSON output with version(-s)",
        )

    def run(self, opts: List[str], args: argparse.Namespace) -> None:
        versions = {"sentinel-sdk": sentinel.version.VERSION}
        if args.all:
            versions.update(component_versions())
        if args.pretty:
            rich.print_json(json.dumps(versions))
        else:
            print(json.dumps(versions))
