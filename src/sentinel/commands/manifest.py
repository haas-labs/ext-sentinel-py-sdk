from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import List

from rich import box, print, print_json
from rich.console import Console
from rich.table import Table
from sentinel.commands.common import SentinelCommand
from sentinel.manifest import Status
from sentinel.services.manifest_api import ManifestAPI
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
        return "Managing Sentinel Detector Manifest"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument(
            "--action",
            type=str,
            required=True,
            choices=[a.value.lower() for a in Action],
            help="Manifest actions",
        )
        parser.add_argument("--id", type=str, help="The detector schema id")
        parser.add_argument("--name", type=str, help="The detector schema name")
        parser.add_argument("--version", type=str, help="The detector schema version")
        parser.add_argument("--status", choices=[s.value.lower() for s in Status], help="The schema status")
        parser.add_argument("--classpath", type=str, help="The classpath to detector manifest")

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        if args.action.upper() not in (Action.show.value, Action.validate.value):
            logger.info("Importing service account tokens")
            import_service_tokens()

        manifest_api = ManifestAPI()
        match args.action.upper():
            case Action.change.value:
                if args.id is None or args.status is None:
                    logger.error("Missed or misconfigured required arguments, --id and/or --status")
                    return
                manifest_api.change(schema_id=args.id, name=args.name, status=Status(args.status.upper()))

            case Action.registrer.value:
                if args.classpath is None:
                    logger.error("Missed must have agrument for show action, --classpath")
                    return
                _, manifest = import_by_classpath(classpath=args.classpath)
                manifest_api.register(metadata=manifest.metadata, schema=manifest.Schema.model_json_schema())

            case Action.get.value:
                # Getting a schema by id
                if args.id is not None:
                    self.get_manifest_by(api=manifest_api, schema_id=args.id)
                # Getting a schema by name and version
                elif args.name is not None and args.version is not None:
                    self.get_manifest_by(api=manifest_api, name=args.name, version=args.version)
                # Getting rest of conditions
                else:
                    status = Status[args.status.upper()] if args.status is not None else None
                    self.get_all(manifest_api, name=args.name, status=status)

            case Action.show.value:
                if args.classpath is None:
                    logger.error("Missed must have agrument for show action, --classpath")
                    return
                _, manifest = import_by_classpath(classpath=args.classpath)
                print(manifest.metadata)

                print("JSON schema:")
                print_json(data=manifest.Schema.model_json_schema())

            case _:
                logger.error(f"Unknown action: {args.action}, possible values: create, get or validate")
                return

    def get_manifest_by(self, api: ManifestAPI, schema_id: int = None, name: str = None, version: str = None) -> None:
        if schema_id is not None:
            for schema in api.get(schema_id=schema_id):
                print_json(schema.model_dump_json())
        elif name is not None and version is not None:
            for schema in api.get(name=name, version=version):
                print_json(schema.model_dump_json())

    def get_all(self, api: ManifestAPI, name: str = None, status: Status = None) -> None:
        table = Table(box=box.MINIMAL)
        table.add_column(header="id")
        table.add_column(header="name")
        table.add_column(header="version")
        table.add_column(header="status")
        table.add_column(header="description")
        for manifest in api.get(name=name, status=status):
            status = manifest.status
            match manifest.status:
                case "ACTIVE":
                    status = f"[green]{manifest.status}[/]"
                case "DISABLED":
                    status = f"[yellow]{manifest.status}[/]"
                case "DELETED":
                    status = f"[red]{manifest.status}[/]"

            table.add_row(str(manifest.id), manifest.name, manifest.version, status, manifest.description)
        if table.row_count > 0:
            console = Console()
            console.print(table)
