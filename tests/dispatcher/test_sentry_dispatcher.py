import pathlib

from sentinel.project import SentinelProject
from sentinel.dispatcher import SentryDispatcher


def test_sentry_dispatcher_discovery():
    """
    Dispatcher Init
    """
    profile = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
    dispatcher = SentryDispatcher(profile)

    assert isinstance(dispatcher, SentryDispatcher), "Incorrect dispatcher type"


def test_sentry_dispatcher_init_components():
    """
    Dispatcher Components Init
    """
    project = SentinelProject().parse(pathlib.Path("tests/dispatcher/resources/simple-sentinel-project.yml"))
    dispatcher = SentryDispatcher(project)
    dispatcher.init()
