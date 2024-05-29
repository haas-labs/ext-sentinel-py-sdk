from sentinel.core.v2.sentry import AsyncCoreSentry, CoreSentry

"""
Core Sentry
"""


def test_sentry_core_init():
    monitored_contracts = ["0x1111", "0x2222", "0x3333"]
    sentry = CoreSentry(parameters={"network": "ethereum", "monitored_contracts": monitored_contracts})
    assert isinstance(sentry, CoreSentry), "Incorrect core sentry type"
    assert sentry.name == "CoreSentry", "Incorrect sentry name"
    assert sentry.description == "Core Sentry", "Incorrect sentry description"
    assert sentry.parameters.get("network") == "ethereum", "Incorrect network parameter value"
    assert (
        sentry.parameters.get("monitored_contracts") == monitored_contracts
    ), "Incorrect monitored contracts parameter value"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"


"""
Async Core Sentry
"""


def test_sentry_async_core_init():
    sentry = AsyncCoreSentry()
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect async core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"
