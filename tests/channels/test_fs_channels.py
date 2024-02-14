
import pytest

from sentinel.channels.fs.common import (
    AioConsumerFileChannel, 
    AioProducerFileChannel
)

from sentinel.models.transaction import Transaction


def test_aio_fs_channels_init(tmpdir):
    '''
    Test File Channels Init
    '''
    consumer_filepath = tmpdir / 'consumer.json'
    producer_filepath = tmpdir / 'producer.json'

    consumer_channel = AioConsumerFileChannel(name='TestFSConsumer', 
                                              record_type='sentinel.models.transaction.Transaction',
                                              path=consumer_filepath)
    producer_channel = AioProducerFileChannel(name='TestFSProducer', 
                                              record_type='sentinel.models.transaction.Transaction',
                                              path=producer_filepath)

    assert isinstance(consumer_channel, AioConsumerFileChannel), \
        'Incorrect type for AioConsumerFileChannel'

    assert isinstance(producer_channel, AioProducerFileChannel), \
        'Incorrect type for AioProducerFileChannel'

@pytest.mark.asyncio
async def test_aio_fs_consumer_channel():
    '''
    Test AIO FS Consumer Channel
    '''
    messages = []

    async def handler(msg):
        assert isinstance(msg, Transaction)
        messages.append(msg)
        
    transactions_path = 'tests/channels/resources/transactions.jsonl'
    transactions_channel = AioConsumerFileChannel(name='TransactionsFSChannel',
                                                  record_type='sentinel.models.transaction.Transaction',
                                                  path=transactions_path)
    transactions_channel.on_message = handler
    await transactions_channel.run()

    assert len(messages) == 5, \
        'Incorrect number of consumed messages'
