import pathlib

from sentinel.utils.settings import load_project_settings


def test_project_settings_load_empty():
    settings = load_project_settings(pathlib.Path("tests/settings/resources/telemetry.yaml"))
    assert settings.project.name == "TelemetryProject", "Incorrect project name"
    assert settings.project.description == "Sample project with active telemetry", "Incorrect project description"

    assert len(settings.settings) > 0, "Expected non-empty settings"
    assert settings.settings.get("TELEMETRY_ENABLED", False), "Disabled telemetry"
    assert settings.settings.get("TELEMETRY_PORT"), "Expected telemetry port: 9090"
