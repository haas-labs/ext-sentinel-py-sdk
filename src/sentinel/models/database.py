from pydantic import BaseModel, Field
from typing import Any, Optional, Dict


class Database(BaseModel):
    """
    Database
    """

    type: str
    instance: Any = Field(default=None)
    description: Optional[str] = Field(default="")
    name: Optional[str] = None
    id: Optional[str] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    label: Optional[Dict[str,str]] = Field(default_factory=dict)

