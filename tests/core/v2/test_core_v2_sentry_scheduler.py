from sentinel.core.v2.sentry import CoreSentry


def test_sentry_scheduler_init():
    sentry = CoreSentry()
    assert isinstance(sentry, CoreSentry), "Incorrect sentry type"
