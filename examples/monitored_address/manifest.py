from typing import List

from sentinel.manifest import BaseSchema, Field, MetadataModel, NetworkTag, Status


class Schema(BaseSchema):
    address: List[str] = Field(default_factory=list)


metadata = MetadataModel(
    name="Monitored-Address-Tx-Monitor",
    title="Monitored Address Tx Monitor",
    version="0.1.1",
    status=Status.ACTIVE,
    description="Monitored Address Transaction Monitor",
    tags=[
        NetworkTag.EVM,
    ],
    faq=[
        {
            "name": "What is for?",
            "value": " ".join(
                [
                    "Monitored Address Transaction Detector is a simple monitor ",
                    "tracking statistics against monitored address",
                ]
            ),
        }
    ],
)
