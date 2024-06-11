from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import List

from rich import box, print, print_json
from rich.console import Console
from rich.table import Table
from sentinel.commands.common import SentinelCommand
from sentinel.services.detector_schema import DetectorSchemaAPI, SchemaStatus
from sentinel.services.service_account import import_service_tokens
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import logger


class Action(Enum):
    change = "CHANGE"
    get = "GET"
    registrer = "REGISTER"
    show = "SHOW"
    validate = "VALIDATE"


class Command(SentinelCommand):
    def description(self) -> str:
        return "Managing Sentinel Detector Schemas"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument(
            "--action",
            type=str,
            required=True,
            choices=[a.value.lower() for a in Action],
            help="The schema actions",
        )
        parser.add_argument("--id", type=str, help="The schema id")
        parser.add_argument("--name", type=str, help="The schema name")
        parser.add_argument("--version", type=str, help="The schema version")
        parser.add_argument("--status", choices=[s.value.lower() for s in SchemaStatus], help="The schema status")
        parser.add_argument("--classpath", type=str, help="The classpath to detector schema")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        if args.action.upper() not in (Action.show.value, Action.validate.value):
            logger.info("Importing service account tokens")
            import_service_tokens()

        schema_api = DetectorSchemaAPI()
        match args.action.upper():
            case Action.change.value:
                if args.id is None or args.status is None:
                    logger.error("Missed or misconfigured required arguments, --id and/or --status")
                    return
                schema_api.change(schema_id=args.id, name=args.name, status=SchemaStatus(args.status.upper()))
            case Action.registrer.value:
                if args.classpath is None:
                    logger.error("Missed must have agrument for show action, --classpath")
                    return
                _, schema = import_by_classpath(classpath=args.classpath)
                name, version = schema.revision()
                schema_api.register(name=name, version=version, schema=schema.model_json_schema())

            case Action.get.value:
                # Getting a schema by id
                if args.id is not None:
                    self.get_schema_by(api=schema_api, schema_id=args.id)
                # Getting a schema by name and version
                elif args.name is not None and args.version is not None:
                    self.get_schema_by(api=schema_api, name=args.name, version=args.version)
                # Getting all schema versions
                elif args.name is not None and args.version is None:
                    self.get_all(schema_api, name=args.name)
                # Getting all schemas
                else:
                    self.get_all(schema_api)

            case Action.show.value:
                if args.classpath is None:
                    logger.error("Missed must have agrument for show action, --classpath")
                    return
                _, schema = import_by_classpath(classpath=args.classpath)
                name, version = schema.revision()
                print(f"Schema name: {name}, version: {version}")
                print("JSON schema:")
                print_json(data=schema.model_json_schema())

            case _:
                logger.error(f"Unknown action: {args.action}, possible values: create, get or validate")
                return

    def get_schema_by(
        self, api: DetectorSchemaAPI, schema_id: int = None, name: str = None, version: str = None
    ) -> None:
        if schema_id is not None:
            for schema in api.get(schema_id=schema_id):
                print_json(schema.model_dump_json())
        elif name is not None and version is not None:
            for schema in api.get(name=name, version=version):
                print_json(schema.model_dump_json())

    def get_all(self, api: DetectorSchemaAPI, name: str = None) -> None:
        table = Table(box=box.MINIMAL)
        table.add_column(header="id")
        table.add_column(header="name")
        table.add_column(header="version")
        table.add_column(header="status")
        for schema in api.get(name=name):
            status = schema.status
            match schema.status:
                case "ACTIVE":
                    status = f"[green]{schema.status}[/]"
                case "DISABLED":
                    status = f"[yellow]{schema.status}[/]"
                case "DELETED":
                    status = f"[red]{schema.status}[/]"

            table.add_row(str(schema.id), schema.name, schema.version, status)
        console = Console()
        console.print(table)
