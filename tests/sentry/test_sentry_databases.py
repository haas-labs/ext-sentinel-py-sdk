from sentinel.sentry.db import SentryDatabases
from sentinel.db.address.memory import InMemoryAddressDB

DB_SETTINGS = {
    "databases": [
        {
            "alias": "address_db",
            "type": "sentinel.db.address.memory.InMemoryAddressDB",
            "parameters": {
                "metadata_type": "int"
            }
        },
        {
            "alias": "failed",
            "type": "sentinel.db.transaction",
        },
    ]
}


def test_sentry_db_success_import():
    dbs = SentryDatabases(aliases=["address_db"], settings=DB_SETTINGS)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry databases type"
    assert dbs.databases == ["address"], "Incorrect database list"
    assert hasattr(dbs, "address"), "Missed addresses database"
    assert isinstance(dbs.address, InMemoryAddressDB), "Incorrect address db type"


def test_sentry_db_failed_import():
    dbs = SentryDatabases(aliases=["address"], settings=DB_SETTINGS)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry Databases type"
    assert dbs.databases == [], "Imported incorrect database(-s)"

    dbs = SentryDatabases(aliases=["failed"], settings=DB_SETTINGS)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry Databases type"
    assert dbs.databases == [], "Imported incorrect database(-s)"
