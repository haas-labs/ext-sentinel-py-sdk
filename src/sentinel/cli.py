import sys
import logging
import pathlib
import argparse

from typing import List, Dict


from sentinel.settings import get_project_settings
from sentinel.commands.common import (
    get_command,
    get_commands_from_module,
    print_commands,
    print_unknown_command,
)

logger = logging.getLogger(__name__)


def execute(argv: List[str] = None, settings: Dict = dict()):
    # Add current directory to python path
    sys.path.append(str(pathlib.Path.cwd()))

    argv = argv or sys.argv
    settings = settings or get_project_settings()
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
    command.run(args, opts)
