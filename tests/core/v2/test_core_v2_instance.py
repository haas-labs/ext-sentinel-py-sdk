from sentinel.core.v2.instance import load_instance
from sentinel.core.v2.sentry import CoreSentry
from sentinel.models.sentry import Sentry


def test_core_load_sentry_instance():
    settings = Sentry(name="test://CoreSentry", type="sentinel.core.v2.sentry.CoreSentry")
    sentry = load_instance(settings=settings)
    assert isinstance(sentry, CoreSentry), "Incorrect sentry instance type"
    assert sentry.name == "test://CoreSentry", "Incorrect sentry name"


def test_core_load_sentry_instance_init_issue():
    settings = Sentry(name="test://CoreSentry", type="sentinel.core.sentry.CoreSentry")
    sentry = load_instance(settings=settings)
    assert sentry is None, "Incorrect sentry instance type"
