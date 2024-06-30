import re

from pydantic import BaseModel

FIELD_TYPE_MAPPING = {
    "integer": "INTEGER",
    "string": "TEXT",
    "number": "REAL",
    "array": "BLOB",
    "object": "BLOB",
}


def get_table_name(name: str):
    """
    return table name from model name
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def get_fields(model: BaseModel):
    return list(model.model_fields.keys())


def get_sql_create_table(model: BaseModel):
    """
    returns SQL for creating table from a model
    """
    tablename = get_table_name(model.__name__)
    SQL_CREATE_TABLE = f"CREATE TABLE IF NOT EXISTS {tablename} ("
    schema = model.model_json_schema()
    fields = []
    for field_name, details in schema.get("properties").items():
        fields.append(f"{field_name} {FIELD_TYPE_MAPPING[details['type']]}")
    SQL_CREATE_TABLE += ", ".join(fields)
    SQL_CREATE_TABLE += ")"

    return SQL_CREATE_TABLE


def get_sql_insert_record(model: BaseModel):
    tablename = get_table_name(model.__name__)
    fields = get_fields(model)
    field_names = ",".join(fields)
    field_values = ",".join([f":{f}" for f in fields])
    SQL_INSERT = f"INSERT INTO {tablename} ({field_names}) VALUES ({field_values})"
    return SQL_INSERT
