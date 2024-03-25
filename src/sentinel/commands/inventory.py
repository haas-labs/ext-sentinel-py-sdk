import os
import logging

from typing import List
from argparse import ArgumentParser, Namespace

from sentinel.inventory import Inventory
from sentinel.models.project import ComponentType
from sentinel.commands.common import SentinelCommand
from sentinel.utils.settings import load_extra_vars

logger = logging.getLogger(__name__)


class Command(SentinelCommand):
    def description(self) -> str:
        return "Sentinel Inventory"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        component_types = [str(ct) for ct in list(ComponentType)]
        parser.add_argument(
            "--type",
            metavar="TYPE",
            type=ComponentType,
            choices=list(ComponentType),
            help=f"Component type, supported: {', '.join(component_types)}",
        )

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        if args.settings.project is None or not args.settings.project.path.exists():
            logger.error("Cannot detect project directory, missed sentinel.yalm file")
            return

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v
                
        if args.type:
            inventory = Inventory(settings=args.settings)
            inventory.scan(ctype=args.type)

