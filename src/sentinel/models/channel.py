from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class Channel(BaseModel):
    """
    Input/Output Channel
    """

    type: str
    name: Optional[str] = None
    alias: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    instance: Optional[Any] = None
