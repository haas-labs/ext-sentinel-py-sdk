from typing import List, Optional

from pydantic import BaseModel, Field


class ABIInput(BaseModel):
    """
    ABI Input
    """

    internal_type: Optional[str] = Field(alias="internalType", default=None)
    name: str
    type: str
    indexed: Optional[bool] = False


class ABIOutput(BaseModel):
    """
    ABI Output
    """

    internal_type: Optional[str] = Field(alias="internalType", default=None)
    name: str
    type: str
    indexed: Optional[bool] = False


class ABIRecord(BaseModel):
    """
    ABI Record
    """

    name: Optional[str] = None
    type: str
    inputs: Optional[List[ABIInput]] = Field(default_factory=list)
    outputs: Optional[List[ABIOutput]] = Field(default_factory=list)
    state_mutability: str = Field(alias="stateMutability", default=None)
    payable: Optional[bool] = None
    anonymous: Optional[bool] = None
    constant: Optional[bool] = None


class Contract(BaseModel):
    """
    Contract
    """

    # Contract Address
    address: str = Field(alias="contractAddress")

    # Contract Implementation
    implementation: Optional[str] = None

    # ABIs
    abi: Optional[List[ABIRecord]] = None


class ABISignature(BaseModel):
    """
    ABI Signature Model
    """

    contract_address: str
    type: str
    signature_hash: str
    signature: str
    abi: ABIRecord
