from typing import Dict, Union, TypeVar
from pydantic import BaseModel

Address = TypeVar("Address", bound=Union[str, bytes])
Metadata = TypeVar("Metadata", bound=Union[BaseModel, None])


def to_bytes(addr: Union[str, bytes]) -> bytes:
    if isinstance(addr, str) and addr.startswith("0x"):
        addr = addr.lower()
        addr = bytes(addr[2:], "utf-8")
    return addr


class InMemoryAddressDB:
    name = "address"

    def __init__(self, metadata_type: Metadata):
        self.db: Dict[Address, metadata_type] = {}

    def put(self, address: Address, metadata: Metadata):
        self.db[to_bytes(address)] = metadata

    def exists(self, address: Address) -> bool:
        return True if to_bytes(address) in self.db else False

    def get(self, address: Address) -> Metadata:
        return self.db.get(to_bytes(address), None)

    def remove(self, address: Address):
        address = to_bytes(address)
        if address in self.db:
            del self.db[address]

    def all(self) -> Dict[Address, Metadata]:
        return self.db

    @property
    def size(self) -> int:
        return len(self.db)
