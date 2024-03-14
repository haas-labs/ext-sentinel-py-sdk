from sentinel.sentry.core import CoreSentry, AsyncCoreSentry


def test_sentry_core_init():
    sentry = CoreSentry(name="TestSentry", description="Test sentry process")
    assert isinstance(sentry, CoreSentry), "Incorrect core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"


def test_sentry_async_core_init():
    sentry = AsyncCoreSentry(name="AsyncTestSentry", description="Async Test sentry process")
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect async core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"
