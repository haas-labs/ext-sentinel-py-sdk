from sentinel.models.project import ProjectSettings
from sentinel.sentry.transaction import TransactionDetector


def test_tx_detector_init():
    detector = TransactionDetector(
        name="TestTXDetector",
        settings=ProjectSettings(),
        parameters={
            "network": "ethereum",
        },
    )
    detector.activate()
    assert isinstance(detector, TransactionDetector), "Incorrect tx detector type"
    assert detector.name == "TestTXDetector", "Incorrect detector name"
    assert detector.logger_name == "ethereum://TestTXDetector", "Incorrect detector logger name"
    assert (
        detector.description
        == "The base detector which can be used for mointoring activities in transactions stream and publishing results to events stream"
    )
    assert detector.databases.names == [], "Expect to have empty database list"
