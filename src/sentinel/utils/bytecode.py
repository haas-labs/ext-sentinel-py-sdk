from typing import List

import cbor2

from web3 import Web3
from pydantic import BaseModel


class Metadata(BaseModel):
    data: str
    length: int
    # Metadata hash
    ipfs: str = ""
    # If "bytecodeHash" was "bzzr1" in compiler settings not "ipfs" but "bzzr1"
    bzzr1: str = ""
    # Previous versions were using "bzzr0" instead of "bzzr1"
    bzzr0: str = ""
    # If any experimental features that affect code generation are used
    solc: List[int] = []
    experimental: bool = False


class Bytecode:
    def __init__(self, bytecode: str) -> None:
        if bytecode is None or bytecode == "0x":
            raise ValueError("Empty bytecode")

        if not bytecode.startswith("0x"):
            raise ValueError("Expected to have bytecode as string starts with 0x")

        self._metadata = None
        self._bytecode = bytecode[2:]

    @staticmethod
    def get_ipfs_hash(ipfs: bytes) -> str:
        """
        convert bytes into IPFS hash
        """
        return ipfs.hex()

    @property
    def contract(self) -> bytes:
        length = int(self._bytecode[-4:], 16)
        return self._bytecode[: -(2 * length + 4)]

    @property
    def contract_hash(self) -> bytes:
        return Web3.keccak(hexstr=self.contract)

    @property
    def metadata(self) -> Metadata:
        """
        return metadata details
        """
        if self._metadata is not None:
            return self._metadata

        length = int(self._bytecode[-4:], 16)
        data = self._bytecode[-(2 * length + 4) : -4]
        data_bytes = bytes.fromhex(data)

        attrs = cbor2.loads(data_bytes)

        self._metadata = Metadata(
            data=data,
            length=length,
            ipfs=self.get_ipfs_hash(attrs.get("ipfs", b"")),
            bzzr0=attrs.get("bzzr0", b"").hex(),
            bzzr1=attrs.get("bzzr1", b"").hex(),
            solc=list(attrs.get("solc", b"")),
        )

        return self._metadata
