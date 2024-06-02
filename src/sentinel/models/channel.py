from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sentinel.core.v2.handler import FlowType


class Channel(BaseModel):
    """
    Input/Output Channel
    """

    type: str
    name: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    flow_type: FlowType = None
    instance: Optional[Any] = None
    label: Optional[Dict[str, str]] = Field(default_factory=dict)
