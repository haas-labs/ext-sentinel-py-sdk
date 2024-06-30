from typing import Dict

from pydantic import BaseModel, Field
from sentinel.db.utils import (
    FIELD_TYPE_MAPPING,
    get_fields,
    get_sql_create_table,
    get_sql_insert_record,
    get_table_name,
)


class Target(BaseModel):
    address: str
    config_id: int
    config: Dict = Field(default_factory=dict)


def test_get_sql_type():
    assert FIELD_TYPE_MAPPING["integer"] == "INTEGER", "Incorrect integer type"
    assert FIELD_TYPE_MAPPING["number"] == "REAL", "Incorrect float type"
    assert FIELD_TYPE_MAPPING["string"] == "TEXT", "Incorrect string type"
    assert FIELD_TYPE_MAPPING["array"] == "BLOB", "Incorrect BLOB type"


def test_model_name_to_table_name():
    assert get_table_name("TestModel") == "test_model", "Incorrect table name"
    assert get_table_name("Testmodel") == "testmodel", "Incorrect table name"
    assert get_table_name("test_model") == "test_model", "Incorrect table name"
    assert get_table_name("testmodel") == "testmodel", "Incorrect table name"


def test_utils_get_fields():
    target = Target(address="0x1234", config_id=1, config={"k1": "v1"})
    assert get_fields(target) == ["address", "config_id", "config"], "Incorrect field list"


def test_get_sql_create_table():
    SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS target (address TEXT, config_id INTEGER, config BLOB)"
    assert get_sql_create_table(model=Target) == SQL_CREATE_TABLE, "Incorrect SQL CREATE TABLE"


def test_get_sql_insert_record():
    assert (
        get_sql_insert_record(model=Target)
        == "INSERT INTO target (address,config_id,config) VALUES (:address,:config_id,:config)"
    ), "Incorrect INSERT statement"
