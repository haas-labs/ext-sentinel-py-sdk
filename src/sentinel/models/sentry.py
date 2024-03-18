from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


class Sentry(BaseModel):
    name: Optional[str]
    type: str
    parameters: Optional[Dict] = Field(default_factory=dict)
    instance: Optional[Any] = None
    inputs: Optional[List[str]] = Field(default_factory=list)
    outputs: Optional[List[str]] = Field(default_factory=list)
    databases: Optional[List[str]] = Field(default_factory=list)
