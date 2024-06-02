import pathlib
from argparse import ArgumentParser, Namespace
from typing import List

import rich
from sentinel.commands.common import SentinelCommand
from sentinel.core.v2.dispatcher import Dispatcher as DispatcherV2
from sentinel.dispatcher import Dispatcher
from sentinel.project import SentinelProject
from sentinel.services.service_account import import_service_tokens
from sentinel.utils.logger import logger
from sentinel.utils.settings import IncorrectFileFormat


class Command(SentinelCommand):
    def description(self) -> str:
        return "Launch sentinel process(-es)"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument("--profile", type=pathlib.Path, required=True, help="Sentinel Process Profile")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run in dry-run mode w/o real processing, just profile validation and printing out",
        )
        parser.add_argument("--import-service-tokens", action="store_true", help="Import service tokens before launch")
        parser.add_argument("--beta", action="store_true", help="Use beta features")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        if args.import_service_tokens:
            logger.info("Importing service account tokens")
            import_service_tokens()

        try:
            if args.settings.project is None or not args.settings.project.path.exists():
                logger.error("Cannot detect project directory, missed sentinel.yalm file")
                return

            settings = SentinelProject().parse(path=args.profile, extra_vars=self.extra_vars)
            if args.beta:
                dispatcher = DispatcherV2(settings=settings)
            else:
                dispatcher = Dispatcher(settings)
            if args.dry_run:
                rich.print_json(settings.model_dump_json())
            dispatcher.run()
        except IncorrectFileFormat as err:
            logger.error(err)
