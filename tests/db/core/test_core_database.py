from sentinel.core.v2.sentry import Sentry
from sentinel.db.core.database import Database


def test_core_database():
    db = Database(name="TestDatabase", sentry=Sentry(name="TestSentry", type="sentinel.core.v2.sentry.Sentry"))
    assert isinstance(db, Database), "Incorrect database instance type"
