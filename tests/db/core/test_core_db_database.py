from sentinel.db.core import Database


def test_core_database(tmpdir):
    db = Database(":memory:")
    assert isinstance(db, Database), "Incorrect database instance"
    assert str(db) == "Database(:memory:)", "Incorrect database string representation"

    db = Database(tmpdir / "test.sqlite3")
    assert isinstance(db, Database), "Incorrect database instance"

    db = Database(tmpdir / "test.sqlite3", overwrite=True)
    assert isinstance(db, Database), "Incorrect database instance"

    db.close()


def test_core_database_operations():
    db = Database(":memory:")
    db.execute("CREATE TABLE kv (k,v)")
    db.execute("INSERT INTO kv (k,v) VALUES (:k, :v)", parameters={"k": "k1", "v": "v1"})
    results = list(db.query("SELECT count(*) AS total_records FROM kv"))
    db.commit()
    assert results[0].get("total_records") == 1, "Incorrect number of records in database"


def test_database_version():
    db = Database(":memory:")
    assert db.version == {"sqlite": "3.37.2"}, "Unexpected sqlite version"


def test_database_vacuum(tmpdir):
    db = Database(":memory:")
    db.vacuum()


def test_database_analyze(tmpdir):
    db = Database(":memory:")
    db.analyze()


def test_database_journal_mode(tmpdir):
    db = Database(":memory:")
    assert db.journal_mode == "memory", "Unexpected default journal mode"

    db = Database(tmpdir / "test.sqlite3")
    assert db.journal_mode == "delete", "Unexpected default journal mode"

    db.enable_wal()
    assert db.journal_mode == "wal", "Incorrect journal mode, wal expected"

    db.disable_wal()
    assert db.journal_mode == "delete", "Incorrect journal mode, delete expected"
