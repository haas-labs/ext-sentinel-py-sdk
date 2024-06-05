import pathlib
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from sentinel.models.channel import Channel
from sentinel.models.database import Database
from sentinel.models.sentry import Sentry


class ComponentType(Enum):
    project = "project"

    sentry = "sentry"

    # inbound channel
    input = "input"

    # outbound channel
    output = "output"

    database = "database"

    def __str__(self):
        return self.value


class Config(BaseModel):
    # Activate monitoring
    monitoring_enabled: bool = False
    # Monitoring port for metrics and health check
    monitoring_port: int = 9090


class Project(BaseModel):
    name: str
    description: Optional[str] = ""
    path: Optional[pathlib.Path] = None
    label: Optional[Dict[str, str]] = Field(default_factory=dict)
    config: Optional[Config] = Config()


class Settings(BaseModel):
    project: Optional[Project] = Project(name="default")
    sentries: Optional[List[Sentry]] = Field(default_factory=list)
    imports: Optional[List[str]] = Field(default_factory=list)
    inputs: Optional[List[Channel]] = Field(default_factory=list)
    outputs: Optional[List[Channel]] = Field(default_factory=list)
    databases: Optional[List[Database]] = Field(default_factory=list)

    def search(self, type: str, id: str) -> Channel | Database:
        for kind in getattr(self, type):
            if kind.id == id:
                return kind
        return None

    def enrich_sentries(self):
        """
        Update inputs/outputs/databases ids with definitions instead of ids
        """
        for sentry in self.sentries:
            for ni, input in enumerate(sentry.inputs):
                if not isinstance(input, str):
                    continue
                input_details = self.search(type="inputs", id=input)
                if input_details is not None:
                    sentry.inputs[ni] = input_details

            for no, output in enumerate(sentry.outputs):
                if not isinstance(output, str):
                    continue
                output_details = self.search(type="outputs", id=output)
                if output_details is not None:
                    sentry.outputs[no] = output_details

            for nd, database in enumerate(sentry.databases):
                if not isinstance(database, str):
                    continue
                database_details = self.search(type="databases", id=database)
                if database_details is not None:
                    sentry.databases[nd] = database_details

    def cleanup(self):
        """
        Usually used to remove inputs/outputs/databases definitions
        after sentry configuration enrichment (enrich_rentries)
        """
        self.inputs = []
        self.outputs = []
        self.databases = []
