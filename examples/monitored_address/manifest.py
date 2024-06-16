from sentinel.manifest import BaseSchema, MetadataModel, NetworkTag, Status


class Schema(BaseSchema): ...


metadata = MetadataModel(
    name="Monitored-Address-Tx-Monitor",
    version="0.1.0",
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
