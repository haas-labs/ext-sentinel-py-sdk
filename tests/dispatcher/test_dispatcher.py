import pathlib

from sentinel.profile import LauncherProfile
from sentinel.dispatcher import Dispatcher


def test_dispatcher_discovery():
    """
    Dispatcher Init
    """
    profile_path = pathlib.Path("tests/dispatcher/resources/single-process-profile.yml")
    profile = LauncherProfile().parse(profile_path)
    dispatcher = Dispatcher(profile)

    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"


def test_dispatcher_init_components():
    """
    Dispatcher Init
    """
    profile_path = pathlib.Path("tests/dispatcher/resources/single-process-profile.yml")
    profile = LauncherProfile().parse(profile_path)
    dispatcher = Dispatcher(profile=profile)
    dispatcher.init()

    assert sorted(dispatcher.processes.keys()) == sorted(
        [
            "SimpleDetector",
        ]
    ), "Incorrect database list"
