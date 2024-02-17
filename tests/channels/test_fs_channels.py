import pytest

from sentinel.channels.fs.common import InboundFileChannel, OutboundFileChannel

from sentinel.models.transaction import Transaction


def test_fs_channels_init(tmpdir):
    """
    Test File Channels Init
    """
    inbound_channel_filepath = tmpdir / "source.json"
    outbound_channel_filepath = tmpdir / "target.json"

    inbound_channel = InboundFileChannel(
        name="TestInboundFSChannel",
        record_type="sentinel.models.transaction.Transaction",
        path=inbound_channel_filepath,
    )
    outbound_channel = OutboundFileChannel(
        name="TestOutboundFSChannel",
        record_type="sentinel.models.transaction.Transaction",
        path=outbound_channel_filepath,
    )

    assert isinstance(inbound_channel, InboundFileChannel), "Incorrect type for InboundFileChannel"

    assert isinstance(outbound_channel, OutboundFileChannel), "Incorrect type for OutboundFileChannel"


@pytest.mark.asyncio
async def test_aio_fs_consumer_channel():
    """
    Test AIO FS Consumer Channel
    """
    messages = []

    async def handler(msg):
        assert isinstance(msg, Transaction)
        messages.append(msg)

    transactions_path = "tests/channels/resources/transactions.jsonl"
    transactions_channel = InboundFileChannel(
        name="TransactionsFSChannel",
        record_type="sentinel.models.transaction.Transaction",
        path=transactions_path,
    )
    transactions_channel.on_message = handler
    await transactions_channel.run()

    assert len(messages) == 5, "Incorrect number of consumed messages"
