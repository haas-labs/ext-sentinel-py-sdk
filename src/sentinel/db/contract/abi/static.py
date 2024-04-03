# Static (pre-defined) ABI signatures without dependencies to a contract address

from sentinel.models.contract import ABISignature, ABIRecord


ABI_EVENT_OWNERSHIP_TRANSFERED = ABISignature(
    contract_address="0x",
    type="event",
    signature_hash="0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0",
    signature="OwnershipTransferred(address,address)",
    abi=ABIRecord(
        **{
            "name": "OwnershipTransferred",
            "type": "event",
            "inputs": [
                {
                    "internal_type": "address",
                    "name": "previousOwner",
                    "type": "address",
                    "indexed": True,
                },
                {
                    "internal_type": "address",
                    "name": "newOwner",
                    "type": "address",
                    "indexed": True,
                },
            ],
            "outputs": [],
            "state_mutability": None,
            "payable": None,
            "anonymous": False,
            "constant": None,
        }
    ),
)


ABI_EVENT_UPGRADED = ABISignature(
    contract_address="0x",
    type="event",
    signature_hash="0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
    signature="Upgraded(address)",
    abi=ABIRecord(
        **{
            "name": "Upgraded",
            "type": "event",
            "inputs": [
                {
                    "internal_type": "address",
                    "name": "implementation",
                    "type": "address",
                    "indexed": True,
                }
            ],
            "outputs": [],
            "state_mutability": None,
            "payable": None,
            "anonymous": False,
            "constant": None,
        }
    ),
)


ABI_EVENT_WITHDRAWAL = ABISignature(
    contract_address="0x",
    type="event",
    signature_hash="0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
    signature="Withdrawal(address,bytes32,address,uint256)",
    abi=ABIRecord(
        **{
            "name": "Withdrawal",
            "type": "event",
            "inputs": [
                {
                    "internal_type": "address",
                    "name": "to",
                    "type": "address",
                    "indexed": False,
                },
                {
                    "internal_type": "bytes32",
                    "name": "nullifierHash",
                    "type": "bytes32",
                    "indexed": False,
                },
                {
                    "internal_type": "address",
                    "name": "relayer",
                    "type": "address",
                    "indexed": True,
                },
                {
                    "internal_type": "uint256",
                    "name": "fee",
                    "type": "uint256",
                    "indexed": False,
                },
            ],
            "outputs": [],
            "state_mutability": None,
            "payable": None,
            "anonymous": False,
            "constant": None,
        }
    ),
)

ABI_EVENT_TRANSFER = ABISignature(
    contract_address="0x",
    type="event",
    signature_hash="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    signature="Transfer(address,address,uint256)",
    abi=ABIRecord(
        **{
            "name": "Transfer",
            "type": "event",
            "inputs": [
                {
                    "internal_type": "address",
                    "name": "from",
                    "type": "address",
                    "indexed": True,
                },
                {
                    "internal_type": "address",
                    "name": "to",
                    "type": "address",
                    "indexed": True,
                },
                {
                    "internal_type": "uint256",
                    "name": "value",
                    "type": "uint256",
                    "indexed": False,
                },
            ],
            "outputs": [],
            "state_mutability": None,
            "payable": None,
            "anonymous": False,
            "constant": None,
        }
    ),
)
