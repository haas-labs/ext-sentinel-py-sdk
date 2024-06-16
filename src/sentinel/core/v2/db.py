from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sentinel.core.v2.instance import load_instance
from sentinel.utils.logger import get_logger


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
    label: Optional[Dict[str, str]] = Field(default_factory=dict)


class Databases:
    def __init__(self, databases: List[Database], **kwargs) -> None:
        self.logger = get_logger(__name__)

        for db in databases:
            try:
                self.logger.info(f"Initializing database: {db.id}, type: {db.type}")
                db_instance = load_instance(settings=db, **kwargs)
                setattr(self, db_instance.name, db_instance)
            except AttributeError as err:
                self.logger.error(f"Database initialization issue, id: {db.id}, error: {err}")
