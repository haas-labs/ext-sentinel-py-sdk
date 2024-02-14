from typing import List, Optional
from pydantic import BaseModel, Field


class Error(BaseModel):
    """
    Error
    """

    code: int
    field: str
    message: str


class EndpointError(BaseModel):
    """
    Endpoint Error
    """

    code: int
    message: str
    errors: Optional[List[Error]] = Field(default_factory=list)
