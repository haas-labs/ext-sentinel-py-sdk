import pathlib

from sentinel.project import SentinelProject
from sentinel.dispatcher import SentryDispatcher


def test_sentry_dispatcher_discovery():
    """
    Dispatcher Init
    """
    settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
    dispatcher = SentryDispatcher(settings)

    assert isinstance(dispatcher, SentryDispatcher), "Incorrect dispatcher type"


def test_sentry_dispatcher_init_components():
    """
    Dispatcher Components Init
    """
    settings = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
    dispatcher = SentryDispatcher(settings)

    assert isinstance(dispatcher, SentryDispatcher), "Incorrect dispatcher type"
    # TODO the test case is incomplete, this work needs to be done