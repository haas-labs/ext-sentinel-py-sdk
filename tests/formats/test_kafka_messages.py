import json
import pathlib

from sentinel.models.transaction import Transaction


def test_mapping_kafka_message_to_transaction_model():
    """
    Test mapping Kafka message to Transaction data model
    """
    msg_data = json.loads(pathlib.Path("tests/formats/resources/kafka_message_transaction_v1.json").open("r").read())

    transaction = Transaction(**msg_data)
    assert isinstance(transaction, Transaction), "Incorrect transaction type"
