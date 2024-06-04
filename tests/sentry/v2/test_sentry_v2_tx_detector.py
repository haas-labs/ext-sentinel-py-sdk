import pathlib

from sentinel.channels.common import InboundChannel
from sentinel.core.v2.settings import Settings
from sentinel.sentry.v2.transaction import TransactionDetector


def test_sentry_tx_detector_init(tmpdir):
    local_tx_path = pathlib.Path(tmpdir / "transactions.jsonl")
    settings = Settings(
        inputs=[
            {
                "id": "local/fs/transactions",
                "type": "sentinel.channels.fs.transactions.InboundTransactionsChannel",
                "parameters": {"path": local_tx_path},
            },
        ]
    )
    tx_detector = TransactionDetector(parameters={"network": "ethereum"}, settings=settings)
    assert isinstance(tx_detector, TransactionDetector), "Incorrect Transaction Detector type"
    assert tx_detector.name == "TransactionDetector", "Incorrect tx detector name"
    assert tx_detector.logger_name == "ethereum://TransactionDetector", "Incorrect detector logger name"
    assert (
        tx_detector.description
        == "The base detector which can be used for mointoring activities in transactions stream and publishing results to events stream"
    )
    assert tx_detector.databases is None, "Expect to have empty database list"

    tx_detector.init()
    assert isinstance(tx_detector.inputs.transactions, InboundChannel), "Incorrect inbound transactions channel"
    assert (
        tx_detector.inputs.transactions.on_transaction == tx_detector.on_transaction
    ), "Incorrect refs to on_transaction method"
