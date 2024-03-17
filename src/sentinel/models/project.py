from typing import List, Dict, Any
from pydantic import BaseModel, Field

from sentinel.models.sentry import Sentry

class Project(BaseModel):
    name: str
    description: str


class ProjectSettings(BaseModel):

    project: Project

    sentries: List[Sentry] = Field(default_factory=list)

    # the first settings in the list is default one
    settings: Dict[str, Any] = Field(default_factory=dict)
