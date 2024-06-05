import pathlib

from sentinel.core.v2.dispatcher import Dispatcher
from sentinel.models.sentry import Sentry
from sentinel.models.settings import Config, Project, Settings
from sentinel.utils.settings import load_settings

EMPTY_SETTINGS = Settings()


def test_core_dispatcher():
    dispatcher = Dispatcher(settings=EMPTY_SETTINGS)
    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
    assert isinstance(dispatcher.settings, Settings), "Incorrect settings type"


def test_core_dispatcher_restart_and_scheduler_opts():
    settings = Settings(
        sentries=[
            Sentry(
                name="eth://UserLoggerSentry-1",
                type="sentry.logger.UserLoggerSentry",
                restart=True,
                schedule="5 0 0 0 0",
            ),
            Sentry(
                name="eth://UserLoggerSentry-2",
                type="sentry.logger.UserLoggerSentry",
                restart=True,
            ),
        ]
    )
    dispatcher = Dispatcher(settings=settings)
    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
    assert len(dispatcher.active_sentries) == 0, "Incorrect list of active sentries"
    assert len(dispatcher.restarting_sentries) == 1, "Incorrect list of restarting sentries"
    assert len(dispatcher.scheduled_sentries) == 1, "Incorrect list of scheduled sentries"
    assert dispatcher.processing_completed is False, "Incorrect processing completed status"


def test_core_dispatcher_active_monitoring():
    dispatcher = Dispatcher(
        settings=Settings(project=Project(name="Monitoring", config=Config(monitoring_enabled=True)))
    )
    assert len(dispatcher.settings.sentries) == 1, "Incorrect sentry list"
    assert dispatcher.metrics is not None, "Incorrect metrics queue"
    monitor = dispatcher.settings.sentries[0]
    assert monitor.name == "MetricServer", "Incorrect monitor name"
    assert monitor.type == "sentinel.core.v2.metric.MetricServer", "Incorrect monitor type"
    assert monitor.restart is True, "Incorrect monitor restart flag"
    assert monitor.parameters == {"port": 9090}, "Incorrect monitor parameters"


def test_core_dispatcher_run():
    dispatcher = Dispatcher(settings=load_settings(pathlib.Path("tests/core/v2/resources/settings/plain.yaml")))
    # dispatcher.run()


# def test_sentry_dispatcher_discovery():
#     """
#     Dispatcher Init
#     """
#     settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
#     dispatcher = Dispatcher(settings)

#     assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"


# def test_sentry_dispatcher_init_components():
#     """
#     Dispatcher Components Init
#     """
#     settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
#     dispatcher = Dispatcher(settings)

#     assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
#     # TODO the test case is incomplete, this work needs to be done

# def test_sentry_dispatcher_telemetry_disabled():
#     """
#     Dispatcher Components Init
#     """
#     settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
#     dispatcher = Dispatcher(settings)

#     assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
#     assert dispatcher.settings.settings.get("TELEMETRY_ENABLED", False) is False, "Expected disabled telemetry"
#     assert (
#         len([s for s in dispatcher.settings.sentries if s.name == "MetricServer"]) == 0
#     ), "Unexpected enabled MetricServer"
#     assert dispatcher.metrics is None, "Unexpect to have metric queue enabled"

# def test_sentry_dispatcher_telemetry_enabled():
#     """
#     Dispatcher Components Init
#     """
#     settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/with-telemetry-enabled.yml"))
#     dispatcher = Dispatcher(settings)

#     assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
#     assert dispatcher.settings.settings.get("TELEMETRY_ENABLED") is True, "Expected enabled telemetry"
#     assert dispatcher.settings.settings.get("TELEMETRY_PORT") == 9090, "Expected telemetry port equals 9090"
#     assert (
#         len([s for s in dispatcher.settings.sentries if s.name == "MetricServer"]) == 1
#     ), "Missed enabled MetricServer"
#     assert dispatcher.metrics is not None and isinstance(
#         dispatcher.metrics, MetricQueue
#     ), "Expect to have metric queue enabled"
