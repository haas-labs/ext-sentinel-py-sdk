import argparse
import pathlib
import sys
from typing import List

from sentinel.commands.common import (
    get_command,
    get_commands_from_module,
    print_commands,
    print_unknown_command,
)
from sentinel.models.project import ProjectSettings
from sentinel.utils.logger import logger
from sentinel.utils.settings import load_project_settings


def execute(argv: List[str] = None):
    # Add current directory to python path
    current_path = pathlib.Path.cwd()
    sys.path.append(str())

    sentinel_settings_path = current_path / "sentinel.yaml"
    settings = ProjectSettings()
    if sentinel_settings_path.exists():
        logger.info(f"Checking settings from {sentinel_settings_path}")
        settings = load_project_settings(sentinel_settings_path)
        settings.project.path = sentinel_settings_path.parent

    argv = argv or sys.argv
    commands = get_commands_from_module()
    command_name = get_command(argv)
    if not command_name:
        print_commands(commands, settings)
        sys.exit(0)
    elif command_name not in commands:
        print_unknown_command(command_name, settings)
        sys.exit(2)
    command = commands[command_name]
    parser = argparse.ArgumentParser(
        usage=f"sentinel {command_name} {command.syntax()}",
        conflict_handler="resolve",
        description=command.description(),
    )
    command.add_options(parser)
    opts, args = parser.parse_known_args(args=argv[1:])
    opts.settings = settings
    command.run(args, opts)
