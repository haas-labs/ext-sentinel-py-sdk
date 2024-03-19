from sentinel.models.database import Database
from sentinel.sentry.db import SentryDatabases
from sentinel.db.address.memory import InMemoryAddressDB

DATABASES = [
    Database(id="address_db", type="sentinel.db.address.memory.InMemoryAddressDB", parameters={"metadata_type": "int"}),
    Database(id="failed", type="sentinel.db.transaction"),
]


def test_sentry_db_success_import():
    dbs = SentryDatabases(ids=["address_db"], databases=DATABASES)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry databases type"
    assert dbs.databases == ["address"], "Incorrect database list"
    assert hasattr(dbs, "address"), "Missed addresses database"
    assert isinstance(dbs.address, InMemoryAddressDB), "Incorrect address db type"


def test_sentry_db_failed_import():
    dbs = SentryDatabases(ids=["address"], databases=DATABASES)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry Databases type"
    assert dbs.databases == [], "Imported incorrect database(-s)"

    dbs = SentryDatabases(ids=["failed"], databases=DATABASES)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry Databases type"
    assert dbs.databases == [], "Imported incorrect database(-s)"
