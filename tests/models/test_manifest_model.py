from sentinel.manifest import BaseSchema, Severity
from sentinel.services.manifest_api import update_ui_schema


def test_severity_model():
    schema = BaseSchema()
    assert schema.severity == -1, "Incorrect severity value"

    assert Severity(schema.severity) == Severity.AUTO, "Incorrect default (AUTO) severity value"


def test_ui_schema_handling():
    class AddressManifest(BaseSchema):
        address: str

    class NoFieldsManifest(BaseSchema): ...

    assert update_ui_schema(ui_schema={}, schema=AddressManifest) == {
        "ui:order": ["address", "severity"]
    }, "Incorrect UI schema"

    assert update_ui_schema(ui_schema={"ui:order": ["severity", "address"]}, schema=AddressManifest) == {
        "ui:order": ["address", "severity"]
    }, "Incorrect UI schema"

    assert update_ui_schema(ui_schema={}, schema=NoFieldsManifest) == {"ui:order": ["severity"]}, "Incorrect UI schema"

    assert update_ui_schema(ui_schema={"ui:order": ["severity"]}, schema=NoFieldsManifest) == {
        "ui:order": ["severity"]
    }, "Incorrect UI schema"
