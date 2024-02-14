
import json

from sentinel.utils import dicts_merge
from sentinel.utils import dict_fields_filter
from sentinel.utils import dict_fields_mapping

from sentinel.formats.mappings import (
    JSONRPC_TRANSACTION_FIELD_MAPPINGS,
    JSONRPC_TRANSACTION_FIELD_IGNORE_LIST,
) 


def test_transaction_data_merge():
    '''
    Merge transaction data
    '''
    block_path = 'tests/formats/resources/jsonrpc_block_v2.jsonl'
    transaction_path = 'tests/formats/resources/jsonrpc_transaction_v2.jsonl'
    transaction_receipt_path = 'tests/formats/resources/jsonrpc_transaction_receipt_v2.jsonl'

    block_data = json.load(open(block_path, 'r'))
    transaction_data = json.load(open(transaction_path, 'r'))
    transaction_receipt_data = json.load(open(transaction_receipt_path, 'r'))

    transaction = dicts_merge(block_data, 
                            transaction_data)
    transaction = dicts_merge(transaction,
                            transaction_receipt_data)
    
    assert sorted(transaction.keys()) == sorted([
            'accessList', 'baseFeePerGas', 'blockHash', 'blockNumber', 'chainId', 'contractAddress', 
            'cumulativeGasUsed', 'difficulty', 'effectiveGasPrice', 'extraData', 'from', 'gas', 
            'gasLimit', 'gasPrice', 'gasUsed', 'hash', 'input', 'logs', 'logsBloom', 'nonce', 
            'maxFeePerGas', 'maxPriorityFeePerGas', 'miner', 'mixHash', 'number', 'parentHash', 
            'r', 'receiptsRoot', 's', 'sha3Uncles', 'size', 'stateRoot', 'status', 'timestamp', 
            'to', 'totalDifficulty', 'transactionHash', 'transactionIndex', 'transactions', 
            'type', 'transactionsRoot', 'uncles', 'v', 'value', 'yParity',
        ]), \
        'Incorrect list of keys for merged transaction data'


def test_transaction_field_filter():
    '''
    Transaction field filtering test
    '''
    block_path = 'tests/formats/resources/jsonrpc_block_v2.jsonl'
    transaction_path = 'tests/formats/resources/jsonrpc_transaction_v2.jsonl'
    transaction_receipt_path = 'tests/formats/resources/jsonrpc_transaction_receipt_v2.jsonl'

    block_data = json.load(open(block_path, 'r'))
    transaction_data = json.load(open(transaction_path, 'r'))
    transaction_receipt_data = json.load(open(transaction_receipt_path, 'r'))

    transaction = dicts_merge(block_data, 
                            transaction_data)
    transaction = dicts_merge(transaction,
                            transaction_receipt_data)

    assert sorted(dict_fields_filter(transaction, 
                                    ignore_list=JSONRPC_TRANSACTION_FIELD_IGNORE_LIST).keys()
            ) == sorted([
                'blockHash', 'blockNumber', 'contractAddress', 'cumulativeGasUsed', 'effectiveGasPrice', 
                'from', 'gas', 'gasPrice', 'gasUsed', 'hash', 'input', 'logs', 'nonce', 'maxFeePerGas', 
                'maxPriorityFeePerGas', 'status', 'timestamp', 'to', 'transactionIndex', 'transactionHash',
                'transactionsRoot', 'type', 'value'            
            ])


def test_transaction_field_mappings():
    '''
    Test field mappings for transactions
    '''
    block_path = 'tests/formats/resources/jsonrpc_block_v2.jsonl'
    transaction_path = 'tests/formats/resources/jsonrpc_transaction_v2.jsonl'
    transaction_receipt_path = 'tests/formats/resources/jsonrpc_transaction_receipt_v2.jsonl'

    block_data = json.load(open(block_path, 'r'))
    transaction_data = json.load(open(transaction_path, 'r'))
    transaction_receipt_data = json.load(open(transaction_receipt_path, 'r'))

    source_transaction = dicts_merge(block_data, 
                                    transaction_data)
    source_transaction = dicts_merge(source_transaction,
                                    transaction_receipt_data)

    filtered_source_transaction = dict_fields_filter(source_transaction, 
                                                     JSONRPC_TRANSACTION_FIELD_IGNORE_LIST)

    target_transaction = dict_fields_mapping(filtered_source_transaction, 
                                            JSONRPC_TRANSACTION_FIELD_MAPPINGS)

    assert sorted(target_transaction.keys()) == sorted([
        'hash', 'nonce', 'block_hash', 'block_number', 'block_timestamp', 'transaction_index',
        'from_address', 'to_address', 'value', 'gas', 'gas_price', 'input', 'max_fee_per_gas',
        'max_priority_fee_per_gas', 'cumulative_gas_used', 'gas_used', 'contract_address',
        'root', 'status', 'effective_gas_price', 'transaction_type', 'logs',
    ])
