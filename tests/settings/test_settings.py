import pathlib

from sentinel.models.channel import Channel
from sentinel.models.database import Database
from sentinel.models.settings import ComponentType, Settings
from sentinel.utils.settings import load_settings


def validate_settings_id_types(settings: Settings) -> None:
    for sentry in settings.sentries:
        for input in sentry.inputs:
            assert isinstance(input, str), "Expect to have input as id (str)"
        for output in sentry.outputs:
            assert isinstance(output, str), "Expect to have output as id (str)"
        for database in sentry.databases:
            assert isinstance(database, str), "Expect to have database as id (str)"


def validate_settings_types(settings: Settings) -> None:
    for sentry in settings.sentries:
        for input in sentry.inputs:
            assert isinstance(input, Channel), "Expect to have input as channel type"
        for output in sentry.outputs:
            assert isinstance(output, Channel), "Expect to have output as channel type"
        for database in sentry.databases:
            assert isinstance(database, Database), "Expect to have database as database type"


def test_settings_component_types():
    assert str(ComponentType.project) == "project", "Incorrect project type"
    assert str(ComponentType.sentry) == "sentry", "Incorrect sentry type"
    assert str(ComponentType.input) == "input", "Incorrect input type"
    assert str(ComponentType.output) == "output", "Incorrect output type"
    assert str(ComponentType.database) == "database", "Incorrect database type"


def test_settings_search():
    settings = Settings(inputs=[Channel(id="incorrect_id", type="sentinel.channels.fs.events.OutboundEventsChannel")])
    assert settings.search(type="inputs", id="local/fs/event") is None, "Incorrect inputs search"

    settings = Settings(inputs=[Channel(id="local/fs/event", type="sentinel.channels.fs.events.OutboundEventsChannel")])
    assert isinstance(settings.search(type="inputs", id="local/fs/event"), Channel), "Incorrect inputs search"


def test_settings_enrich_sentries_plain_profile():
    settings = load_settings(pathlib.Path("tests/settings/resources/plain.yaml"))
    assert isinstance(settings, Settings), "Incorrect settings type"
    assert len(settings.sentries) == 1, "Incorrect sentries number"

    validate_settings_id_types(settings)
    settings.enrich_sentries()
    validate_settings_types(settings)


def test_settings_enrich_sentries_profile_with_imports():
    settings = load_settings(pathlib.Path("tests/settings/resources/with-imports.yaml"))
    assert isinstance(settings, Settings), "Incorrect settings type"
    assert len(settings.sentries) == 1, "Incorrect sentries number"

    validate_settings_id_types(settings)
    settings.enrich_sentries()
    validate_settings_types(settings)


def test_settings_enrich_sentries():
    settings = load_settings(pathlib.Path("tests/settings/resources/plain.yaml"))

    settings.enrich_sentries()
    validate_settings_types(settings)

    settings.enrich_sentries()
    validate_settings_types(settings)
