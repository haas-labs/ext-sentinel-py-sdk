from pydantic import BaseModel


class Blockchain(BaseModel):
    """
    Blockchain Model
    """

    short_name: str
    network: str
    chain_id: str
    description: str
    currency: str
