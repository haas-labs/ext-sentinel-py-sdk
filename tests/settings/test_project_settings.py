import pathlib

from sentinel.utils.settings import load_project_settings


def test_project_settings_load_empty():
    settings = load_project_settings(pathlib.Path("tests/settings/resources/empty.yaml"))
    assert settings.project.name == "Empty Project", "Incorrect project name"
    assert settings.project.description == "Empty Project", "Incorrect project description"
    assert settings.settings == {}, "Expected empty settings"
    assert settings.imports == [], "Expected empty imports"
    assert settings.inputs == [], "Expected empty list of inputs"
    assert settings.outputs == [], "Expected empty list of outputs"
    assert settings.databases == [], "Expected empty list of databases"


def test_project_settings_load_plain():
    settings = load_project_settings(pathlib.Path("tests/settings/resources/plain.yaml"))
    assert settings.project.name == "Plain Project Configuration", "Incorrect project name"

    # Sentries
    assert len(settings.sentries) == 1, "Incorrect number of sentries"
    assert settings.sentries[0].name == "eth://UserLoggerSentry", "Incorrect sentry name"
    assert settings.sentries[0].type == "sentry.logger.UserLoggerSentry", "Incorrect sentry type"
    assert settings.sentries[0].parameters == {"network": "ethereum"}, "Incorrect sentry parameters"

    # Inputs
    assert len(settings.inputs) == 1, "Incorrect number of inputs"
    assert settings.inputs[0].id == "FSTransactions", "Incorrect input id"
    assert (
        settings.inputs[0].type == "sentinel.channels.fs.transactions.InboundTransactionsChannel"
    ), "Incorrect input type"
    assert settings.inputs[0].parameters == {
        "path": "./data/transactions.json",
    }, "Incorrect input parameters"

    # Outputs
    assert len(settings.outputs) == 1, "Incorrect number of outputs"
    assert settings.outputs[0].id == "FSEvents", "Incorrect output id"
    assert settings.outputs[0].type == "sentinel.channels.fs.common.OutboundFileChannel", "Incorrect output type"
    assert settings.outputs[0].parameters == {
        "record_type": "sentinel.models.event.Event",
        "path": "./events/events.json",
        "mode": "overwrite",
    }, "Incorrect output parameters"

    # Databases
    assert len(settings.databases) == 1, "Incorrect number of databases"
    assert settings.databases[0].id == "AddressDBList", "Incorrect database id"
    assert settings.databases[0].type == "sentinel.db.address.local.AddressDB", "Incorrect database type"
    assert settings.databases[0].parameters == {
        "path": "./data/address.list",
    }, "Incorrect database parameters"


def test_project_settings_import_partially():
    # Sentries
    settings = load_project_settings(pathlib.Path("tests/settings/resources/config/sentries.yaml"))
    assert len(settings.sentries) == 1, "Incorrect number of sentries"
    assert settings.sentries[0].name == "eth://UserLoggerSentry", "Incorrect sentry name"
    assert settings.sentries[0].type == "sentry.logger.UserLoggerSentry", "Incorrect sentry type"
    assert settings.sentries[0].parameters == {"network": "ethereum"}, "Incorrect sentry parameters"

    # Databases
    settings = load_project_settings(pathlib.Path("tests/settings/resources/config/databases.yaml"))
    assert len(settings.databases) == 1, "Incorrect number of databases"
    assert settings.databases[0].id == "AddressDBList", "Incorrect database id"
    assert settings.databases[0].type == "sentinel.db.address.local.AddressDB", "Incorrect database type"
    assert settings.databases[0].parameters == {
        "path": "./data/address.list",
    }, "Incorrect database parameters"

    # Inputs
    settings = load_project_settings(pathlib.Path("tests/settings/resources/config/inputs.yaml"))
    assert len(settings.inputs) == 1, "Incorrect number of inputs"
    assert settings.inputs[0].id == "FSTransactions", "Incorrect input id"
    assert (
        settings.inputs[0].type == "sentinel.channels.fs.transactions.InboundTransactionsChannel"
    ), "Incorrect input type"
    assert settings.inputs[0].parameters == {
        "path": "./data/transactions.json",
    }, "Incorrect input parameters"

    # Outputs
    settings = load_project_settings(pathlib.Path("tests/settings/resources/config/outputs.yaml"))
    assert len(settings.outputs) == 1, "Incorrect number of outputs"
    assert settings.outputs[0].id == "FSEvents", "Incorrect output id"
    assert settings.outputs[0].type == "sentinel.channels.fs.common.OutboundFileChannel", "Incorrect output type"
    assert settings.outputs[0].parameters == {
        "record_type": "sentinel.models.event.Event",
        "path": "./events/events.json",
        "mode": "overwrite",
    }, "Incorrect output parameters"


def test_project_settings_handling_imports():
    settings = load_project_settings(pathlib.Path("tests/settings/resources/with-imports.yaml"))
    assert settings.project.name == "Project with imports", "Incorrect project name"
    assert settings.project.description == "Project with imports", "Incorrect project description"

    assert len(settings.sentries) == 1, "Incorrect number of sentries"
    assert settings.sentries[0].name == "eth://UserLoggerSentry", "Incorrect sentry name"

    assert len(settings.inputs) == 1, "Incorrect number of inputs"
    assert settings.inputs[0].id == "FSTransactions", "Incorrect input id"

    assert len(settings.outputs) == 1, "Incorrect number of outputs"
    assert settings.outputs[0].id == "FSEvents", "Incorrect output id"

    assert len(settings.databases) == 1, "Incorrect number of databases"
    assert settings.databases[0].id == "AddressDBList", "Incorrect database id"
