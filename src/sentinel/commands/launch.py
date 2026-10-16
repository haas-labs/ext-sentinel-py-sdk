import pathlib
from argparse import ArgumentParser, Namespace
from typing import List

import rich
from sentinel.commands.common import SentinelCommand
from sentinel.core.v2.dispatcher import Dispatcher
from sentinel.core.v2.settings import Settings
from sentinel.services.service_account import import_service_tokens
from sentinel.utils.logger import logger
from sentinel.utils.settings import IncorrectFileFormat, load_settings


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

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        if args.import_service_tokens:
            logger.info("Importing service account tokens")
            import_service_tokens()

        # Load project settings
        # TODO make loading project settings through helper/utils
        try:
            if args.settings.project is None or not args.settings.project.path.exists():
                logger.error("Cannot detect project directory, missed sentinel.yaml file")
                return

            try:
                settings = load_settings(pathlib.Path().cwd() / "sentinel.yaml")
            except OSError:
                settings = Settings()

            profile_settings = load_settings(path=args.profile, extra_vars=self.extra_vars)
        except IncorrectFileFormat as err:
            logger.error(err)
            return

        settings.project = profile_settings.project
        settings.inputs.extend(profile_settings.inputs)
        settings.outputs.extend(profile_settings.outputs)
        settings.databases.extend(profile_settings.databases)
        settings.sentries.extend(profile_settings.sentries)

        # update input/output/databases ids as configuration itself for sentries
        settings.enrich_sentries()
        settings.cleanup()

        dispatcher = Dispatcher(settings=settings)
        if args.dry_run:
            rich.print_json(settings.model_dump_json())
        dispatcher.run()
