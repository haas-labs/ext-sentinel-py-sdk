import os
import logging
import pathlib

from sentinel.dispatcher import Dispatcher
from sentinel.commands.common import Command
from sentinel.utils import get_sentinel_version
from sentinel.profile import LauncherProfile, IncorrectProfileFormat, load_extra_vars


logger = logging.getLogger(__name__)


class LaunchCommand(Command):
    """
    Launch Command
    """

    name = "launch"
    help = "Launch sentinel process(-es)"

    def add(self):
        """
        Add Launch command and arguments
        """
        self._parser.add_argument("--profile", type=pathlib.Path, required=True, help="Sentinel Process Profile")
        self._parser.add_argument(
            "--vars",
            type=str,
            action="append",
            help="Set additional variables as JSON, " + "if filename prepend with @. Support YAML/JSON file",
        )
        self._parser.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")

        self._parser.set_defaults(handler=self.handle)

        return self._parser

    def handle(self, args):
        """
        Handling Fetch command arguments
        """
        super().handle(args)

        logger.info(f"Sentinel SDK version: {get_sentinel_version()}")
        extra_vars = load_extra_vars(args.vars)

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v

        try:
            profile = LauncherProfile().parse(profile_path=args.profile, extra_vars=extra_vars)
            dispatcher = Dispatcher(profile=profile)
            dispatcher.run()
        except IncorrectProfileFormat as err:
            logger.error(err)
