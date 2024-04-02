from sentinel.models.blockchain import Blockchain

# https://chainlist.org/

BLOCKCHAIN = {
    "anvil": Blockchain(
        network="anvil", chain_id=31337, short_name="anv", description="Anvil Testnet", currency="ETH"
    ),
    "arbitrum": Blockchain(
        network="arbitrum", chain_id=42161, short_name="arb", description="Arbitrum One", currency="ETH"
    ),
    "base": Blockchain(
        network="base", chain_id=8453, short_name="base", description="Base", currency="ETH"
    ),
    "bsc": Blockchain(
        network="bsc", chain_id=56, short_name="bsc", description="BNB Smart Chain Mainnet", currency="BNB"
    ),
    "ethereum": Blockchain(
        network="ethereum", chain_id=1, short_name="eth", description="Ethereum Mainnet", currency="ETH"
    ),
    "optimism": Blockchain(
        network="optimism", chain_id=10, short_name="op", description="OP Mainnet", currency="ETH"
    ),
}
