from sentinel.sentry.transaction import TransactionDetector


def test_tx_detector_init():
    detector = TransactionDetector(
        name="TestTXDetector",
        parameters={
            "network": "ethereum",
        },
    )
    assert isinstance(detector, TransactionDetector), "Incorrect tx detector type"
    assert detector.name == "eth://TestTXDetector", "Incorrect detector name"
    assert (
        detector.description
        == "The base detector which can be used for mointoring activities in transactions stream and publishing results to events stream"
    )
    assert detector.databases.names == [], "Expect to have empty database list"
