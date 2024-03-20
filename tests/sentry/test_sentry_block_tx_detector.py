from sentinel.sentry.block_tx import BlockDetector


def test_block_tx_detector_init():
    detector = BlockDetector(
        name="TestBlockTXDetector",
        parameters={
            "network": "ethereum",
        },
    )
    assert isinstance(detector, BlockDetector), "Incorrect block tx detector type"
    assert detector.name == "eth://TestBlockTXDetector", "Incorrect detector name"
    assert (
        detector.description
        == "The base block tx detector which can be used for mointoring activities in transactions stream when all transactions in a block are required during a one call and publishing results to events stream"
    )
    assert detector.databases.names == [], "Expect to have empty database list"
