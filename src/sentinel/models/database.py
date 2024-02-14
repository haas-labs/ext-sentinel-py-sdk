
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict


class Database(BaseModel):
    '''
    Database
    '''
    name: str
    type: str
    description: str = Field(default='')
    parameters: Optional[Dict] = Field(default_factory=dict)
    instance: Any = Field(default=None)
