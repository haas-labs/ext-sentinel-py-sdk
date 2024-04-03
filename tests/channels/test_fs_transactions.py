import pathlib
from sentinel.channels.fs.transactions import InboundTransactionsChannel


def test_fs_channel_transactions_init(tmpdir):
    transactions = InboundTransactionsChannel(name="transactions", path=pathlib.Path(tmpdir / "events.json"))
    assert isinstance(transactions, InboundTransactionsChannel), "Incorrect transactions channel type"
