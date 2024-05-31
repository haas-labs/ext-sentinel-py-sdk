import pytest
from sentinel.core.v2.db import SentryDatabases
from sentinel.db.address.memory import InMemoryAddressDB
from sentinel.models.database import Database

DATABASES = [
    Database(id="address_db", type="sentinel.db.address.memory.InMemoryAddressDB", parameters={"metadata_type": "int"}),
    Database(id="failed", type="sentinel.db.transaction"),
]


def test_sentry_db_success_import():
    dbs = SentryDatabases(ids=["address_db"], databases=DATABASES)
    assert isinstance(dbs, SentryDatabases), "Incorrect Sentry databases type"
    assert dbs.names == ["address"], "Incorrect database list"
    assert hasattr(dbs, "address"), "Missed addresses database"
    assert isinstance(dbs.address, InMemoryAddressDB), "Incorrect address db type"
    assert dbs.address is not None, "Address database shouldn't be None"


def test_sentry_db_failed_import():
    with pytest.raises(RuntimeError):
        SentryDatabases(ids=["address"], databases=DATABASES)

    with pytest.raises(RuntimeError):
        SentryDatabases(ids=["failed"], databases=DATABASES)
