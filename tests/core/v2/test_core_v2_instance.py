import pytest
from sentinel.core.v2.instance import load_instance
from sentinel.core.v2.sentry import CoreSentry
from sentinel.models.sentry import Sentry
from sentinel.models.settings import Settings


def test_core_load_sentry_instance():
    settings = Settings(
        sentries=[Sentry(id="test/core_sentry", name="test://CoreSentry", type="sentinel.core.v2.sentry.CoreSentry")]
    )

    sentry = load_instance(id="test/core_sentry", settings=settings.sentries)
    assert isinstance(sentry, CoreSentry), "Incorrect sentry instance type"
    assert sentry.name == "test://CoreSentry", "Incorrect sentry name"


def test_core_load_sentry_instance_duplicated_ids():
    settings = Settings(
        sentries=[
            Sentry(id="test/core_sentry", name="test://CoreSentry", type="sentinel.core.v2.sentry.CoreSentry"),
            Sentry(id="test/core_sentry", name="test://CoreSentry", type="sentinel.core.v2.sentry.CoreSentry"),
        ]
    )
    with pytest.raises(ValueError) as err:
        load_instance(id="test/core_sentry", settings=settings.sentries)
    assert str(err.value) == "Detected more than one id: test/core_sentry", "Incorrect error message"


def test_core_load_sentry_instance_init_issue():
    settings = Settings(
        sentries=[Sentry(id="test/core_sentry", name="test://CoreSentry", type="sentinel.core.sentry.CoreSentry")]
    )
    sentry = load_instance(id="test/core_sentry", settings=settings.sentries)
    assert sentry is None, "Incorrect sentry instance type"
