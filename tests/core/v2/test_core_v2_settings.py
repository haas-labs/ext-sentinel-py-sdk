import pathlib

from sentinel.core.v2.settings import Config, Project, Settings
from sentinel.utils.settings import load_settings


def test_core_settings():
    settings = load_settings(path=pathlib.Path("tests/core/v2/resources/settings/empty.yaml"))
    project = settings.project
    assert isinstance(settings, Settings), "Incorrect settings type"
    assert isinstance(project, Project), "Incorrect project type"
    assert project.name == "Empty Project", "Incorrect project name"
    assert project.description == "Empty Project", "Incorrect project description"
    assert project.config == Config(), "Incorrect project config"


def test_core_settings_plain_format():
    settings = load_settings(path=pathlib.Path("tests/core/v2/resources/settings/plain.yaml"))

    project = settings.project
    assert project.name == "Plain Project Configuration", "Incorrect project name"
    assert project.config == Config(), "Incorrect default project config"

    sentries = settings.sentries
    assert len(sentries) == 1, "Incorrect sentries list, expected one sentry"
    sentry = sentries[0]
    assert sentry.name == "eth://CoreSentry", "Incorrect sentry name"
    assert sentry.type == "sentinel.core.v2.sentry.CoreSentry", "Incorrect sentry type"
    assert sentry.restart is True, "Incorrect sentry restart flag"
    assert sentry.schedule is None, "Incorrect sentry schedule"
    assert sentry.parameters == {"network": "ethereum"}, "Incorrect sentry parameters"
    assert sentry.inputs == ["local/fs/transaction"], "Incorrect sentry input list"
    assert sentry.outputs == ["local/fs/Event"], "Incorrect sentry output list"
    assert sentry.databases == ["local/address"], "Incorrect sentry database list"

    inputs = settings.inputs
    assert len(inputs) == 1, "Incorrect input list, expected one input"
    input = inputs[0]
    assert input.id == "local/fs/transaction", "Incorrect input id"
    assert input.type == "sentinel.channels.fs.transactions.InboundTransactionsChannel", "Incorrect input type"
    assert input.parameters == {"path": "./data/transactions.json"}, "Incorrect input parameters"

    outputs = settings.outputs
    assert len(outputs) == 1, "Incorrect output list, expected one output"
    output = outputs[0]
    assert output.id == "local/fs/event", "Incorrect output id"
    assert output.type == "sentinel.channels.fs.common.OutboundFileChannel", "Incorrect output type"
    assert output.parameters == {
        "record_type": "sentinel.models.event.Event",
        "path": "./events/events.json",
        "mode": "overwrite",
    }, "Incorrect output parameters"

    databases = settings.databases
    assert len(databases) == 1, "Incorrect output list, expected one output"
    db = databases[0]
    assert db.id == "local/address", "Incorrect db id"
    assert db.type == "sentinel.db.address.local.AddressDB", "Incorrect db type"
    assert db.parameters == {"path": "./data/address.list"}, "Incorrect db parameters"


def test_core_settings_with_multi_imports():
    settings = load_settings(path=pathlib.Path("tests/core/v2/resources/settings/multiple-imports.yaml"))
    project = settings.project
    assert project.name == "Project with multiple imports", "Incorrect project name"
    assert project.description == "Project with multiple imports", "Incorrect project description"
    assert project.config == Config(monitoring_enabled=True, monitoring_port=9090), "Incorrect project config"
    assert settings.imports == [
        "profiles/sentries.yaml",
        "profiles/local-inputs.yaml",
        "profiles/cloud-inputs.yaml",
        "profiles/local-outputs.yaml",
        "profiles/cloud-outputs.yaml",
        "profiles/local-databases.yaml",
        "profiles/cloud-databases.yaml",
    ], "Incorrect list of imports"
    assert len(settings.sentries) == 1, "Incorrect sentries number"
    assert len(settings.inputs) == 2, "Incorrect inputs number"
    assert len(settings.outputs) == 2, "Incorrect outputs number"
    assert len(settings.databases) == 2, "Incorrect databases number"
