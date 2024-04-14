import pathlib

from sentinel.dispatcher import Dispatcher
from sentinel.project import SentinelProject
from sentinel.metrics.core import MetricQueue


def test_sentry_dispatcher_telemetry_disabled():
    """
    Dispatcher Components Init
    """
    settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
    dispatcher = Dispatcher(settings)

    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
    assert dispatcher.settings.settings.get("TELEMETRY_ENABLED", False) is False, "Expected disabled telemetry"
    assert (
        len([s for s in dispatcher.settings.sentries if s.name == "MetricServer"]) == 0
    ), "Unexpected enabled MetricServer"
    assert dispatcher.metrics is None, "Unexpect to have metric queue enabled"


def test_sentry_dispatcher_telemetry_enabled():
    """
    Dispatcher Components Init
    """
    settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/with-telemetry-enabled.yml"))
    dispatcher = Dispatcher(settings)

    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
    assert dispatcher.settings.settings.get("TELEMETRY_ENABLED") is True, "Expected enabled telemetry"
    assert dispatcher.settings.settings.get("TELEMETRY_PORT") == 9090, "Expected telemetry port equals 9090"
    assert (
        len([s for s in dispatcher.settings.sentries if s.name == "MetricServer"]) == 1
    ), "Missed enabled MetricServer"
    assert dispatcher.metrics is not None and isinstance(
        dispatcher.metrics, MetricQueue
    ), "Expect to have metric queue enabled"
