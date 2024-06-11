import json

from sentinel.models.config import Configuration


def test_config_model_read_v1():
    data = """{
        "id": 1705,
        "createdAt": 1716215314873,
        "updatedAt": 1716215314873,
        "status": "ACTIVE",
        "contract": {
            "id": 1371,
            "createdAt": 1716215314839,
            "updatedAt": 1716215314839,
            "projectId": 503,
            "tenantId": 519,
            "chainUid": "ethereum",
            "proxyAddress": null,
            "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "eth"
        },
        "schema": {
            "id": 1,
            "createdAt": 1717751852969,
            "updatedAt": 1717751852969,
            "status": "ACTIVE",
            "name": "Empty",
            "version": "1",
            "schema": {}
        },
        "name": "Attack Detector",
        "source": "ATTACK_DETECTOR",
        "tags": [],
        "config": {},
        "destinations": [],
        "actions": []
    }"""

    data = json.loads(data)
    print(data)
    config = Configuration(**data)
    assert config.id == 1705, "Incorrect config id"
