import os
import logging
import pathlib

from typing import List
from argparse import ArgumentParser, Namespace

from sentinel.inventory import Inventory
from sentinel.project import load_project_settings
from sentinel.commands.common import SentinelCommand
from sentinel.utils.settings import load_extra_vars
from sentinel.models.component import ComponentType


logger = logging.getLogger(__name__)


class Command(SentinelCommand):
    def description(self) -> str:
        return "Sentinel Inventory"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument(
            "--scan", type=pathlib.Path, metavar="PATH", dest="scan_path", help="Search components in the path"
        )

        component_types = [str(ct) for ct in list(ComponentType)]
        parser.add_argument(
            "--type",
            metavar="TYPE",
            type=ComponentType,
            choices=list(ComponentType),
            help=f"Component type, supported: {', '.join(component_types)}",
        )

        parser.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v

        if args.scan_path:
            logger.info(f"Scanning sentinel components in {args.scan_path}")
            self.scan(args.scan_path, ctype=args.type)

    def scan(self, path: pathlib.Path, ctype: ComponentType) -> None:
        """
        Scan components in the path
        """
        if ctype is None:
            logger.error("Missed --type parameter")
            return

        inventory = Inventory()
        inventory.scan(path, ctype=ctype)
