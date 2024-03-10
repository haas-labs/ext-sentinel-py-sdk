from argparse import ArgumentParser, Namespace
import os
import logging
import pathlib
from typing import List

from sentinel.version import VERSION
from sentinel.dispatcher import Dispatcher
from sentinel.commands.common import SentinelCommand
from sentinel.services.service_account import import_service_tokens
from sentinel.profile import LauncherProfile, IncorrectProfileFormat, load_extra_vars

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
        parser.add_argument("--import-service-tokens", action="store_true", help="Import service tokens before launch")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        logger.info(f"Sentinel SDK version: {VERSION}")
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
            profile = LauncherProfile().parse(profile_path=args.profile, extra_vars=extra_vars)
            dispatcher = Dispatcher(profile=profile)
            dispatcher.run()
        except IncorrectProfileFormat as err:
            logger.error(err)
