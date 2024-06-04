from sentinel.models.transaction import Block, Transaction


def block_generate(block_num: int, block_size: int) -> Block:
    return Block(
        hash="0x",
        number=block_num,
        transaction_count=block_size,
        timestamp=0,
        parent_hash="",
        nonce="",
        sha3_uncles="",
        logs_bloom="",
        transactions_root="",
        state_root="",
        receipts_root="",
        miner="",
        difficulty=0,
        total_difficulty=0,
        size=0,
        extra_data="",
        gas_limit=0,
        gas_used=0,
    )


def tx_generate(block_num: int, block_size: int, tx_index: int) -> Transaction:
    return Transaction(
        hash="0x",
        block=block_generate(block_num=block_num, block_size=block_size),
        nonce=0,
        transaction_index=tx_index,
        value=0,
        gas=0,
        gas_price=0,
        receipt_gas_used=0,
        receipt_effective_gas_price=0,
        receipt_cumulative_gas_used=0,
        input="",
        receipt_root="",
        receipt_status=0,
        transaction_type=0,
        logs=[],
    )
