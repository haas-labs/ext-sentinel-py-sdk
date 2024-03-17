import os
import pathlib

from sentinel.profile import LauncherProfile


def test_launcher_profile_init():
    """
    Launcher Profile Init
    """
    profile = LauncherProfile()
    assert isinstance(profile, LauncherProfile), "Incorrect profile type"


def test_launcher_profile_parse():
    """
    Launcher Profile Parse
    """
    profile = LauncherProfile()
    settings = profile.parse(pathlib.Path("tests/profile/resources/single-process-profile.yml"))

    assert len(settings.processes) == 1, "Incorrect number of processes"


def test_launcher_profile_parse_with_extra_vars():
    """
    Launcher Profile Parse with extra vars
    """
    os.environ["TOKEN"] = "123"
    profile = LauncherProfile()
    path = pathlib.Path("tests/profile/resources/single-process-profile-with-placeholders.yml")
    settings = profile.parse(path, settings={"transactions_path": "/tmp/transactions.json"})

    assert len(settings.processes) == 1, "Incorrect number of processes"
    assert settings.processes[0].inputs[0].parameters == {
        "path": "/tmp/transactions.json"
    }, "Incorrect process input path"
