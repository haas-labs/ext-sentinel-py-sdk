from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sentinel.models.channel import Channel
from sentinel.models.database import Database


class Sentry(BaseModel):
    # Sentry Instance
    instance: Optional[Any] = None

    # Sentry ID
    id: Optional[str] = None
    # Sentry Type
    type: str
    # Sentry Name
    name: Optional[str]
    # Sentry Descriptions
    description: Optional[str] = None
    # Sentry Parameters
    parameters: Optional[Dict] = Field(default_factory=dict)

    inputs: Optional[List[str | Channel]] = Field(default_factory=list)
    outputs: Optional[List[str | Channel]] = Field(default_factory=list)
    databases: Optional[List[str | Database]] = Field(default_factory=list)

    # labels allow to mark a senty for specific purposes.
    # For example: label a senty for specific env only, prod or dev
    label: Optional[Dict[str, str]] = Field(default_factory=dict)

    # restart flag: true means that dispatcher should restart a sentry if it is finished
    restart: bool = True

    # schedule. Cron-style string to describe periodical sentry runs
    schedule: Optional[str] = None
