"""The CLI Common Command"""

import inspect
import logging
import os
from argparse import ArgumentParser, Namespace
from importlib import import_module
from logging.config import dictConfig
from pkgutil import iter_modules
from typing import Dict, List

from sentinel.models.project import ProjectSettings
from sentinel.utils.logger import get_logger
from sentinel.utils.settings import load_extra_vars
from sentinel.version import VERSION

logger = get_logger(__name__)


class SentinelCommand:
    def __init__(self) -> None:
        self.settings: Dict = dict()

    def description(self) -> str:
        return ""

    def syntax(self) -> str:
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def help(self) -> str:
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines since no post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser: ArgumentParser) -> None:
        """
        Populate option parse with options available for this command
        """
        group = parser.add_argument_group(title="global options")
        group.add_argument(
            "--log-level",
            metavar="LEVEL",
            default=logging.INFO,
            help=f"log level (default: {self.settings.get('LOG_LEVEL', 'INFO')})",
        )
        group.add_argument(
            "--vars",
            type=str,
            action="append",
            help="Set additional variables as JSON, " + "if filename prepend with @. Support YAML/JSON file",
        )
        # group.add_argument(
        #     "--env", type=str, default="local", help="Environment, possible values: local, demo, cloud. Default: local"
        # )
        group.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")
        # group.add_argument("--rich-logging", action="store_true", help="Activate rich logging")

        # group.add_argument(
        #     "--pidfile",
        #     metavar="FILE",
        #     help="Write dispatcher process ID to FILE"
        # )
        # group.add_argument(
        #     "-s",
        #     "--set",
        #     action="append",
        #     default=[],
        #     metavar="NAME=VALUE",
        #     help="set/override setting (may be repeated)",
        # )

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

    def run(self, opts: List[str], args: Namespace) -> None:
        """
        Entry point for running commands
        """
        SentinelCommand.overwrite_logging_settings(args.log_level)
        self.extra_vars = load_extra_vars(args.vars)

        # Update env variables via SENTINEL_ENV_PROFILE
        if "SENTINEL_ENV_PROFILE" in os.environ:
            logger.info(f"Loading variables from SENTINEL_ENV_PROFILE, {os.environ['SENTINEL_ENV_PROFILE']}")
            for k, v in load_extra_vars(
                [
                    f"@{os.environ['SENTINEL_ENV_PROFILE']}",
                ]
            ).items():
                os.environ[k] = v

        # Update env variables from file
        if args.env_vars is not None:
            logger.info(f"Loading variables from env vars file, {args.env_vars}")
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v


def get_commands_from_module(module: str = "sentinel.commands") -> Dict[str, SentinelCommand]:
    cmd_module = import_module(module)
    modules = [cmd_module]
    modules += [import_module(f"{module}.{subpath}") for _, subpath, _ in iter_modules(cmd_module.__path__)]

    commands = dict()
    for module in modules:
        for obj in vars(module).values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, SentinelCommand)
                and obj.__module__ == module.__name__
                and obj not in (SentinelCommand,)
            ):
                commands[obj.__module__.split(".")[-1]] = obj()
    return commands


def get_command(args: List[str]) -> str:
    return args[1] if (len(args[1:]) > 0 and not args[1].startswith("-")) else ""


def print_commands(commands: Dict[str, SentinelCommand], settings: ProjectSettings = None):
    project_details = f", Active project: {settings.project.name}" if settings.project is not None else ""
    print(f"Sentinel SDK Version: {VERSION}{project_details}\n")

    print("Usage:\n  sentinel <command> [options] [args]\n\nAvailable commands:")

    for cmdname, cmdclass in sorted(commands.items()):
        print(f"  {cmdname:<20} {cmdclass.description()}")
    print("\nMore commands available when run from project directory\n")
    print('Use "sentinel <command> -h" to see more info about a command')


def print_unknown_command(command: str, settings: Dict = dict()):
    print(f"Unknown command: {command}\nUse 'sentinel' to see available commands")
