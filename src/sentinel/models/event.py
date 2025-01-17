import hashlib
import uuid
from typing import Dict, Optional

from pydantic import BaseModel, Field


def get_event_id() -> str:
    """
    Returns a unique event ID as a UUID
    """
    return str(uuid.uuid4().hex)


def get_hash_id(*values) -> str:
    """
    Calculate an hash ID as a hash sum from a list of field values

    Args:
        values: List of fields to calculate the hash sum

    Returns:
       str: Hash sum of the field values

    Raises:
        ValueError: If any field value in the list is not hashable.
    """
    # Create a hash object
    hash_object = hashlib.sha256()

    # Convert all values to strings and concatenate them if values are hashable
    for value in values:
        value = str(value).encode("utf-8")
        hash_object.update(value)

    # Return the hexadecimal digest
    return hash_object.hexdigest()


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

    # Monitoring ID
    mid: Optional[str] = None

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
