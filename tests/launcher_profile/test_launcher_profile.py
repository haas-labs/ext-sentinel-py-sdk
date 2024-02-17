import os
import json
import pathlib

from sentinel.profile import LauncherProfile, load_extra_vars


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
    settings = profile.parse(pathlib.Path("tests/launcher_profile/resources/single-process-profile.yml"))

    assert len(settings.processes) == 1, "Incorrect number of processes"


def test_load_extra_vars():
    """
    Test loading of extra vars
    """
    expected_result = {
        "TOKEN": "123",
        "transactions_path": "/tmp/transactions.jsonl",
    }
    assert load_extra_vars() == {}, "Incorrect extra vars values, source: no args"
    assert (
        load_extra_vars(
            [
                "@tests/launcher_profile/resources/vars.json",
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: json file"
    assert (
        load_extra_vars(
            [
                "@tests/launcher_profile/resources/vars.yml",
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: yaml file"
    assert (
        load_extra_vars(
            [
                json.dumps(expected_result),
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: vars as json object"


def test_launcher_profile_parse_with_extra_vars():
    """
    Launcher Profile Parse with extra vars
    """
    os.environ["TOKEN"] = "123"
    profile = LauncherProfile()
    path = pathlib.Path("tests/launcher_profile/resources/single-process-profile-with-placeholders.yml")
    settings = profile.parse(path, extra_vars={"transactions_path": "/tmp/transactions.json"})

    assert len(settings.processes) == 1, "Incorrect number of processes"
    assert settings.processes[0].inputs[0].parameters == {
        "path": "/tmp/transactions.json"
    }, "Incorrect process input path"
