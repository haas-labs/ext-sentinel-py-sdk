import os
import logging
import pathlib

from typing import List
from argparse import ArgumentParser, Namespace

from rich import box
from rich.table import Table
from rich.console import Console

from sentinel.project import load_project_settings
from sentinel.commands.common import SentinelCommand
from sentinel.utils.settings import load_extra_vars

logger = logging.getLogger(__name__)


class Command(SentinelCommand):
    def description(self) -> str:
        return "Sentinel Inventory"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument(
            "--scan", type=pathlib.Path, metavar="PATH", dest="scan_path", help="Search components in the path"
        )
        parser.add_argument(
            "--type",
            type=str,
            metavar="TYPE",
            dest="component_type",
            help="Component type, supported: project, sentries, inputs, outputs, databases",
        )
        parser.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v

        if args.scan_path:
            logger.info(f"Scanning sentinel components in {args.scan_path}")
            self.scan(args.scan_path, component_type=args.component_type)

    def scan(self, path: pathlib.Path, component_type: str) -> None:
        """
        Scan components in the path
        """
        console = Console()

        projects = []
        sentries = []
        inputs = []
        outputs = []
        databases = []

        for p in path.glob("**/*.yaml"):
            settings = load_project_settings(p)

            match component_type:
                case "project":
                    project = settings.project
                    if project is not None:
                        project = {
                            "name": project.name.strip() if project.name is not None else "",
                            "description": project.description.strip() if project.description is not None else "",
                        }
                        if project not in projects:
                            projects.append(project)

                case "sentries":
                    for sentry in settings.sentries:
                        sentry = {
                            "name": sentry.name if sentry.name is not None else "",
                            "description": sentry.description.strip() if sentry.description is not None else "",
                        }
                        if sentry not in sentries:
                            sentries.append(sentry)

                case "inputs":
                    for input in settings.inputs:
                        input = {"id": input.id, "name": input.name, "type": input.type}
                        if input not in inputs:
                            inputs.append(input)

                case "outputs":
                    for output in settings.outputs:
                        output = {"id": output.id, "name": output.name, "type": output.name}
                        if output not in outputs:
                            outputs.append(output)

                case "databases":
                    for db in settings.databases:
                        db = {"id": db.id, "name": db.name, "type": db.type}
                        if db not in databases:
                            databases.append(db)
                
                case _:
                    logger.error(f"Unknown component type: {component_type}")


        match component_type:
            case "project":
                if len(projects) > 0:
                    table = Table("Projects", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("name")
                    table.add_column("description")
                    for project in projects:
                        table.add_row(*list(project.values()))
                    console.print(table)

            case "sentries":
                if len(sentries) > 0:
                    table = Table("Sentries", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("name")
                    table.add_column("description")
                    for sentry in sentries:
                        table.add_row(*list(sentry.values()))
                    console.print(table)

            case "inputs":
                if len(inputs) > 0:
                    table = Table("Inputs", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("id")
                    table.add_column("name")
                    table.add_column("type")
                    for input in inputs:
                        table.add_row(*list(input.values()))
                    console.print(table)

            case "outputs":
                if len(outputs) > 0:
                    table = Table("Outputs", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("id")
                    table.add_column("name")
                    table.add_column("type")
                    for output in outputs:
                        table.add_row(*list(output.values()))
                    console.print(table)

            case "databases":
                if len(databases) > 0:
                    table = Table("Databases", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("id")
                    table.add_column("name")
                    table.add_column("type")
                    for db in databases:
                        table.add_row(*list(db.values()))
                    console.print(table)
