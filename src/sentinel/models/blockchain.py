from pydantic import BaseModel


class Blockchain(BaseModel):
    """
    Blockchain Model
    """

    short_name: str
    network: str
    chain_id: int
    description: str
    currency: str
