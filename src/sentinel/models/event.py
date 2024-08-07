import uuid
from typing import Dict, Optional

from pydantic import BaseModel, Field


def get_event_id() -> str:
    return str(uuid.uuid4().hex)


class Blockchain(BaseModel):
    network: str
    chain_id: str


class Event(BaseModel):
    """
    Event Model
    """

    # Sentinel detector ID, currently: detector name + version(optional)
    did: str

    # Event UUID
    eid: str = Field(default_factory=get_event_id)

    # Extractor Detector Config id
    cid: Optional[int] = None

    # Source ID
    # TODO Default value for Sentinel Detector
    sid: str = Field(default="ext:ad")

    # Event Category: EVENT (default) or ALERT or ...
    category: str = Field(default="EVENT")

    # Event Type
    type: str

    # Event/Alert Severity
    severity: float

    # Event/Alert Description
    desc: Optional[str] = None

    # Timestamp in epoch time with milliseconds
    ts: int

    # Chain name
    blockchain: Blockchain

    # Metadata
    """
    contract:  Contract address
    account:   Account address
    """
    metadata: Dict = Field(default_factory=dict)  # Metadata
