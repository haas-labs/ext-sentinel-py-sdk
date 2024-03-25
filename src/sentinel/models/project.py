import pathlib

from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

from sentinel.models.sentry import Sentry
from sentinel.models.channel import Channel
from sentinel.models.database import Database


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


class Project(BaseModel):
    name: str
    description: Optional[str] = ""
    path: Optional[pathlib.Path] = None
    label: Optional[Dict[str, str]] = Field(default_factory=dict)


class ProjectSettings(BaseModel):
    project: Optional[Project] = None
    envs: Optional[Dict] = Field(default_factory=dict)
    sentries: Optional[List[Sentry]] = Field(default_factory=list)
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    imports: Optional[List[str]] = Field(default_factory=list)
    inputs: Optional[List[Channel]] = Field(default_factory=list)
    outputs: Optional[List[Channel]] = Field(default_factory=list)
    databases: Optional[List[Database]] = Field(default_factory=list)
