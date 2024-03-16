from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Sentry(BaseModel):
    type: str
    parameters: Optional[Dict] = Field(default_factory=dict)
    instance: Optional[Any] = None
