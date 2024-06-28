from sentinel.manifest import BaseSchema, Severity


def test_severity_model():
    schema = BaseSchema()
    assert schema.severity == -1, "Incorrect severity value"

    assert Severity(schema.severity) == Severity.AUTO, "Incorrect default (AUTO) severity value"
