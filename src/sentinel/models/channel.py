from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class Channel(BaseModel):
    """
    Input/Output Channel
    """

    name: str
    type: str
    description: Optional[str] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    instance: Optional[Any] = None
