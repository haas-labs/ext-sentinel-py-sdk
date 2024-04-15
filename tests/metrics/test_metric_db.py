from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.core import MetricDatabase

from metric_samples import get_sample, db_with_metrics


def test_metric_core_database_init():
    db = MetricDatabase()
    assert isinstance(db, MetricDatabase), "Incorrect metric database type"

def test_metric_core_database_merge_labels():
    db = db_with_metrics()
    for mertic in db.all():
        assert mertic.labels == {"component": "A", "module": "A"}, "Incorrect labels values after merge"

def test_metric_core_database_update():
    db = db_with_metrics()

    db.clean()
    assert db.size == 6, "Incorrect number of records in database"
    assert len(list(db.all())) == 6, "Incorrect number of records in database"


def test_metric_core_database_clean():
    db = MetricDatabase()

    db.update(get_sample(kind=MetricsTypes.counter))
    assert len(list(db.all())) == 0, "Incorrect number of records in database"

    db.clean()
    assert db.size == 0, "Incorrect number of records in database"
