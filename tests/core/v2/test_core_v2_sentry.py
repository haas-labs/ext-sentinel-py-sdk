from sentinel.core.v2.sentry import AsyncCoreSentry, CoreSentry
from sentinel.models.sentry import Sentry

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


def test_sentry_from_settings():
    sentry = CoreSentry.from_settings(settings=Sentry(name="TestSentry", type="sentinel.core.v2.CoreSentry"))
    assert isinstance(sentry, CoreSentry), "Incorrect sentry type"
    assert sentry.name == "TestSentry", "Incorrect Sentry name"


def test_sentry_run():
    class TestSentry(CoreSentry):
        def init(self) -> None:
            super().init()
            self.on_init_flag = False
            self.on_run_flag = False
            self.on_schedule_flag = False

        def on_init(self):
            self.on_init_flag = True

        def on_run(self):
            self.on_run_flag = True

        def on_schedule(self):
            self.on_schedule_flag = True

    sentry = TestSentry()
    sentry.run()
    assert sentry.on_init_flag is True, "Incorrect on_init flag"
    assert sentry.on_run_flag is True, "Incorrect on_run flag"
    assert sentry.on_schedule_flag is False, "Incorrect on_schedule flag"


"""
Async Core Sentry
"""


def test_sentry_async_core_init():
    sentry = AsyncCoreSentry()
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect async core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"
