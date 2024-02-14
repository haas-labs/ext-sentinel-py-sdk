import json
import pathlib

from typing import Dict, Iterator

from pydantic import BaseModel


class JsonRPCFormat:
    """
    JSON RPC Format Reader/Writer
    """

    def read(self, path: pathlib.Path, record_type: BaseModel) -> Iterator[Dict]:
        """
        read data from JSONRPC result files
        """
        if not path.exists():
            raise IOError(f"The file doesn't exist, {path}")

        with path.open("r") as source:
            for line in source:
                data = json.loads(line)
                record = record_type(**data)
                yield record

    def write(self, path: pathlib.Path) -> None:
        """
        write data in JSONRPC format
        """
        raise NotImplementedError
