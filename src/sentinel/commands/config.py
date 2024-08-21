from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import List

from sentinel.commands.common import SentinelCommand
from sentinel.services.service_account import import_service_tokens
from sentinel.utils.logger import logger


class Action(Enum):
    get = "GET"


class Command(SentinelCommand):
    def description(self) -> str:
        return "Managing Monitoring Configs"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument(
            "--action",
            type=str,
            required=True,
            choices=[a.value.lower() for a in Action],
            help="Config actions",
        )

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        logger.info("Importing service account tokens")
        import_service_tokens()
