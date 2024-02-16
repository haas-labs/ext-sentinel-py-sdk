""" The CLI Common Command
"""
import logging

from argparse import ArgumentParser
from logging.config import dictConfig

from rich.logging import RichHandler


from typing import List


logger = logging.getLogger(__name__)


class Command:
    name = "default"
    help = "Default help"

    def __init__(self, parsers: List[ArgumentParser]):
        """
        CommonCommand Init
        """
        self._parsers = parsers
        self._parser = self._parsers.add_parser(name=self.name, help=self.help)

        self._parser.add_argument(
            "-l",
            "--log-level",
            default="INFO",
            help="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        )

        self._parser.add_argument("--rich-logging", action="store_true", help="Activate rich logging")

    def add(self):
        """
        Add channel command and arguments

        Example:

            parser.add_argument('--profile', type=str,
                    help='The path to a profile')
            parser.set_defaults(handler=self.handle)
            return parser
        """
        raise NotImplementedError()

    @staticmethod
    def handle(args):
        """Handling command arguments"""
        Command.overwrite_logging_settings(args.log_level)

        if args.rich_logging:
            logging.basicConfig(
                level=args.log_level,
                format="%(asctime)s.%(msecs)03d (%(processName)s::%(name)s:%(lineno)d) %(message)s",
                # format="%(asctime)s.%(msecs)03d (%(name)s) %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
                handlers=[RichHandler(rich_tracebacks=True)],
            )
        else:
            logging.basicConfig(
                level=args.log_level,
                format="%(asctime)s.%(msecs)03d (%(processName)s::%(name)s:%(lineno)d) [%(levelname)s] %(message)s",
                # format="%(asctime)s.%(msecs)03d (%(name)s) %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )

    @staticmethod
    def overwrite_logging_settings(log_level: str) -> None:
        """
        Overwrite default logging settings for
        - httpx
        """
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "loggers": {
                    "httpx": {
                        "level": "ERROR",
                    }
                },
            }
        )
