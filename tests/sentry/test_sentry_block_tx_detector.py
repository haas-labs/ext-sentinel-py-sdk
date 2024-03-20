from sentinel.sentry.block_tx import BlockTxDetector


def test_block_tx_detector_init():
    detector = BlockTxDetector(
        name="TestBlockTxDetector",
        parameters={
            "network": "ethereum",
        },
    )
    assert isinstance(detector, BlockTxDetector), "Incorrect block tx detector type"
    assert detector.name == "eth://TestBlockTxDetector", "Incorrect detector name"
    assert (
        detector.description
        == "The base block tx detector which can be used for mointoring activities in transactions stream when all transactions in a block are required during a one call and publishing results to events stream"
    )
    assert detector.databases.names == [], "Expect to have empty database list"
