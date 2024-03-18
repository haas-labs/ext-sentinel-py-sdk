import os
import logging
import pathlib

from typing import List
from argparse import ArgumentParser, Namespace

import rich

from sentinel.profile import LauncherProfile
from sentinel.project import SentinelProject
from sentinel.utils.vars import load_extra_vars
from sentinel.utils.settings import IncorrectFileFormat
from sentinel.commands.common import SentinelCommand
from sentinel.dispatcher import Dispatcher, SentryDispatcher
from sentinel.services.service_account import import_service_tokens


logger = logging.getLogger(__name__)


class Command(SentinelCommand):
    def description(self) -> str:
        return "Launch sentinel process(-es)"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument("--profile", type=pathlib.Path, required=True, help="Sentinel Process Profile")
        parser.add_argument(
            "--vars",
            type=str,
            action="append",
            help="Set additional variables as JSON, " + "if filename prepend with @. Support YAML/JSON file",
        )
        parser.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run in dry-run mode w/o real processing, just profile validation and printing out",
        )
        parser.add_argument("--import-service-tokens", action="store_true", help="Import service tokens before launch")
        parser.add_argument("--sentry", action="store_true", help="Use sentry dispatcher")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        extra_vars = load_extra_vars(args.vars)

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v

        if args.import_service_tokens:
            logger.info("Importing service account tokens")
            import_service_tokens()

        try:
            if args.sentry:
                project = SentinelProject().parse(path=args.profile, extra_vars=extra_vars)
                dispatcher = SentryDispatcher(project)
                if args.dry_run:
                    rich.print_json(project.model_dump_json())
            else:
                profile = LauncherProfile().parse(path=args.profile, settings=extra_vars)
                dispatcher = Dispatcher(profile=profile)
                if args.dry_run:
                    rich.print_json(profile.model_dump_json())
            dispatcher.run()
        except IncorrectFileFormat as err:
            logger.error(err)
