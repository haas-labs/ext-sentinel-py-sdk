from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Contract:
    """
    Contract Model
    """

    contract_address: str
    network: str
