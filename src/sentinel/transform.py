import json


def json_deserializer(serialized):
    """
    JSON Deserializer
    """
    if serialized is None:
        return None
    return json.loads(serialized)
