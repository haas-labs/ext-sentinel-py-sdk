import logging
import pathlib

from typing import Dict, List
from logging.config import dictConfig

from rich import box
from rich.table import Table
from rich.console import Console

from sentinel.utils.settings import load_project_settings
from sentinel.models.component import ComponentType
from sentinel.models.project import ProjectSettings

logger = logging.getLogger(__name__)


class Inventory:
    def __init__(self) -> None:
        self.projects = []
        self.sentries = []
        self.inputs = []
        self.outputs = []
        self.databases = []

        # disable extra information which are required during normal launch project,
        # but extra for inventory scan
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "loggers": {
                    "sentinel.utils.settings": {
                        "level": "ERROR",
                    }
                },
            }
        )

    def scan(self, path: pathlib.Path, ctype: ComponentType) -> None:
        for p in path.glob("**/*.y*ml"):
            settings = load_project_settings(p)
            match ctype:
                case ComponentType.project:
                    self.extract_projects(p, settings)
                case ComponentType.sentry:
                    self.extract_sentries(p, settings)
                case ComponentType.input:
                    self.extract_inputs(p, settings)
                case ComponentType.output:
                    self.extract_outputs(p, settings)
                case ComponentType.database:
                    self.extract_databases(p, settings)

        match ctype:
            case ComponentType.project:
                self.show(data=self.projects)
            case ComponentType.sentry:
                self.show(data=self.sentries)
            case ComponentType.input:
                self.show(data=self.inputs)
            case ComponentType.output:
                self.show(data=self.outputs)
            case ComponentType.database:
                self.show(data=self.databases)

    def extract_projects(self, path: pathlib.Path, settings: ProjectSettings) -> List[Dict]:
        project = settings.project
        if project is not None:
            project = {
                "name": project.name.strip() if project.name is not None else "",
                "description": project.description.strip() if project.description is not None else "",
                "path": str(path),
            }
            if project not in self.projects:
                self.projects.append(project)

    def extract_sentries(self, path: pathlib.Path, settings: ProjectSettings) -> List[Dict]:
        for sentry in settings.sentries:
            sentry = {
                "name": sentry.name if sentry.name is not None else "",
                "description": sentry.description.strip() if sentry.description is not None else "",
                "path": str(path),
            }
            if sentry not in self.sentries:
                self.sentries.append(sentry)

    def extract_inputs(self, path: pathlib.Path, settings: ProjectSettings) -> List[Dict]:
        for input in settings.inputs:
            input = {"id": input.id, "type": input.type}
            if input not in self.inputs:
                self.inputs.append(input)

    def extract_outputs(self, path: pathlib.Path, settings: ProjectSettings) -> List[Dict]:
        for output in settings.outputs:
            output = {"id": output.id, "type": output.type}
            if output not in self.outputs:
                self.outputs.append(output)

    def extract_databases(self, path: pathlib.Path, settings: ProjectSettings) -> List[Dict]:
        for db in settings.databases:
            db = {"id": db.id, "type": db.type}
            if db not in self.databases:
                self.databases.append(db)

    def show(self, data: List[Dict] = list()) -> None:
        """
        Show components details in table form
        """
        if len(data) == 0:
            return

        table = Table(box=box.MINIMAL_HEAVY_HEAD)
        for col_name in data[0].keys():
            table.add_column(col_name)

        for row in data:
            table.add_row(*row.values())

        console = Console()
        console.print(table)