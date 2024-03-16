from typing import List
from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str
    description: str


class ProjectSettings(BaseModel):

    project: Project

    sentries: List[str] = Field(default_factory=list)

    # the first settings in the list is default one
    settings: List[str] = Field(default_factory=list)
