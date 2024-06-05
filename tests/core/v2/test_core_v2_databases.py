from sentinel.core.v2.db import Databases
from sentinel.db.address.memory import InMemoryAddressDB
from sentinel.models.database import Database

DATABASES = [
    Database(type="sentinel.db.address.memory.InMemoryAddressDB", parameters={"metadata_type": "int"}),
    Database(type="sentinel.db.transaction"),
]


def test_sentry_db_success_import():
    dbs = Databases(databases=DATABASES)
    assert isinstance(dbs, Databases), "Incorrect Sentry databases type"
    assert hasattr(dbs, "address"), "Missed addresses database"

    assert isinstance(dbs.address, InMemoryAddressDB), "Incorrect address db type"
    assert dbs.address is not None, "Address database shouldn't be None"
