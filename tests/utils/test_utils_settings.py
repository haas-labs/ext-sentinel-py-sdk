import json

from sentinel.utils.settings import load_extra_vars


def test_load_extra_vars():
    """
    Test loading of extra vars
    """
    expected_result = {
        "TOKEN": "123",
        "transactions_path": "/tmp/transactions.jsonl",
    }
    assert load_extra_vars() == {}, "Incorrect extra vars values, source: no args"
    assert (
        load_extra_vars(
            [
                "@tests/utils/resources/vars.json",
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: json file"
    assert (
        load_extra_vars(
            [
                "@tests/utils/resources/vars.yaml",
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: yaml file"
    assert (
        load_extra_vars(
            [
                json.dumps(expected_result),
            ]
        )
        == expected_result
    ), "Incorrect extra vars values, source: vars as json object"
