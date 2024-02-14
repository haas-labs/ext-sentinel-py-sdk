from enum import Enum

from pydantic import BaseModel


class AddressType(Enum):
    """
    Address Type
    """

    contract = "CONTRACT"
    account = "ACCOUNT"
    undefined = "UNDEFINED"


class AddressDetails(BaseModel):
    """
    Address Details
    """

    address: str
    is_contract: bool = False
    is_account: bool = False
