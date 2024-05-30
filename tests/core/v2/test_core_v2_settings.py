import pathlib

from sentinel.models.settings import Project, Settings
from sentinel.utils.settings import load_settings


def test_core_settings():
    settings = load_settings(path=pathlib.Path("tests/core/v2/resources/settings/empty.yaml"))
    project = settings.project
    assert isinstance(settings, Settings), "Incorrect settings type"
    assert isinstance(project, Project), "Incorrect project type"
    assert project.name == "Empty Project", "Incorrect project name"
    assert project.description == "Empty Project", "Incorrect project description"
