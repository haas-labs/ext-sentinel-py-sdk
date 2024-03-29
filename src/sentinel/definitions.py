from sentinel.models.blockchain import Blockchain

# https://chainlist.org/

BLOCKCHAIN = {
    "ethereum": Blockchain(
        network="ethereum", chain_id=1, short_name="eth", description="Ethereum Mainnet", currency="ETH"
    ),
    "bsc": Blockchain(
        network="bsc", chain_id=56, short_name="bsc", description="BNB Smart Chain Mainnet", currency="BNB"
    ),
    "arbitrum": Blockchain(
        network="arbitrum", chain_id=42161, short_name="arb", description="Arbitrum One", currency="ETH"
    ),
    "anvil": Blockchain(
        network="anvil", chain_id=31337, short_name="anv", description="Anvil Testnet", currency="ETH"
    ),
}
