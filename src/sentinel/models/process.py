from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

from sentinel.models.channel import Channel
from sentinel.models.database import Database


class Process(BaseModel):
    """
    Process
    """

    name: str
    type: str
    description: Optional[str] = None
    instance: Optional[Any] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    inputs: Optional[List[Channel]] = Field(default_factory=list)
    outputs: Optional[List[Channel]] = Field(default_factory=list)
    databases: Optional[List[Database]] = Field(default_factory=list)
