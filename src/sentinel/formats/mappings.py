NETWORKS_BY_ID = {
    '1': "ethereum",
    '56': "bsc",
    '42161': "arbitrum",
}

CHAIN_ID_BY_NETWORK = {
    "ethereum": '1',
    "bsc": '56',
    "arbitrum": '42161',    
}

JSONRPC_BLOCK_FIELD_IGNORE_LIST = [
    'transactions', 'mixHash', 'withdrawals', 'withdrawalsRoot',
]

JSONRPC_BLOCK_FIELD_MAPPINGS = {
    'baseFeePerGas': 'base_fee_per_gas',
    'extraData': 'extra_data',
    'gasLimit': 'gas_limit',
    'gasUsed': 'gas_used',
    'logsBloom': 'logs_bloom',
    'parentHash': 'parent_hash',
    'sha3Uncles': 'sha3_uncles',
    'transactionsRoot': 'transactions_root',
    'stateRoot': 'state_root',
    'receiptsRoot': 'receipts_root',
    'totalDifficulty': 'total_difficulty',
}

JSONRPC_BLOCK_FIELD_TRANSFORM = {
    'number': lambda v: int(v, 0),
    'timestamp': lambda v: int(v, 0),
    'difficulty': lambda v: int(v, 0),
    'size': lambda v: int(v, 0),
    'total_difficulty': lambda v: int(v, 0),
    'gas_limit': lambda v: int(v, 0),
    'gas_used': lambda v: int(v, 0),
    'base_fee_per_gas': lambda v: int(v, 0),
}

JSONRPC_TRANSACTION_FIELD_IGNORE_LIST = [
    'accessList', 'baseFeePerGas', 'chainId', 'difficulty', 'extraData', 
    'gasLimit', 'logsBloom', 'miner',  'mixHash', 'number', 'parentHash',
    'receiptsRoot', 'r', 's', 'sha3Uncles', 'size', 'stateRoot',
    'totalDifficulty', 'transactions',  'uncles', 'v','yParity', 
]

JSONRPC_TRANSACTION_FIELD_MAPPINGS = {
    'blockHash': 'block_hash',
    'blockNumber': 'block_number',
    'contractAddress': 'contract_address',
    'cumulativeGasUsed': 'cumulative_gas_used',
    'effectiveGasPrice': 'effective_gas_price',
    'from': 'from_address',
    'gasUsed': 'gas_used',
    'gasPrice': 'gas_price',
    'maxFeePerGas': 'max_fee_per_gas',
    'maxPriorityFeePerGas': 'max_priority_fee_per_gas',
    'timestamp': 'block_timestamp',
    'to': 'to_address',
    'transactionIndex': 'transaction_index',
    'transactionsRoot': 'root',
    'type': 'transaction_type',
    'transactionHash': 'hash',
}

JSONRPC_TRANSACTION_FIELD_TRANSFORM = {
    'nonce': lambda v: int(v, 0),
    'transaction_index': lambda v: int(v, 0),
    'value': lambda v: int(v, 0),
    'gas': lambda v: int(v, 0),
    'gas_used': lambda v: int(v, 0),
    'gas_price': lambda v: int(v, 0),
    'effective_gas_price': lambda v: int(v, 0),
    'max_fee_per_gas': lambda v: int(v, 0),
    'max_priority_fee_per_gas': lambda v: int(v, 0),
    'cumulative_gas_used': lambda v: int(v, 0),
    'status': lambda v: int(v, 0),
    'transaction_type': lambda v: int(v, 0),
}

JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_IGNORE_LIST = [
    'blockNumber', 'transactionHash', 'transactionIndex',
    'blockHash', 'removed',
]

JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_MAPPINGS = {
    'logIndex': 'index',
}

JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_TRANSFORM = {
    'index': lambda v: int(v, 0),
}

