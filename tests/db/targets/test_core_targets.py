from sentinel.db.targets.core import CoreTargetDB


def test_core_targets_db():
    db = CoreTargetDB(name="TargetDB", sentry_name="TestSentry", sentry_hash="0x1234", network="ethereum")
    assert isinstance(db, CoreTargetDB), "Incorrect CoreTargetDB instance type"
