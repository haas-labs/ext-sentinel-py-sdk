from sentinel.models.blockchain import Blockchain

# https://chainlist.org/

BLOCKCHAIN = {
    "anvil": Blockchain(network="anvil", chain_id=31337, short_name="anv", description="Anvil Testnet", currency="ETH"),
    "arbitrum": Blockchain(
        network="arbitrum", chain_id=42161, short_name="arb", description="Arbitrum One", currency="ETH"
    ),
    "base": Blockchain(network="base", chain_id=8453, short_name="base", description="Base", currency="ETH"),
    "bsc": Blockchain(
        network="bsc", chain_id=56, short_name="bsc", description="BNB Smart Chain Mainnet", currency="BNB"
    ),
    "ethereum": Blockchain(
        network="ethereum", chain_id=1, short_name="eth", description="Ethereum Mainnet", currency="ETH"
    ),
    "optimism": Blockchain(network="optimism", chain_id=10, short_name="op", description="OP Mainnet", currency="ETH"),
    "linea": Blockchain(network="linea", chain_id=59144, short_name="linea", description="Linea", currency="ETH"),
    "polygon": Blockchain(
        network="polygon", chain_id=137, short_name="polygon", description="Polygon Mainnet", currency="MATIC"
    ),
    "blast": Blockchain(network="blast", chain_id=238, short_name="blast", description="Blast Mainnet", currency="ETH"),
    "zksync": Blockchain(
        network="zksync", chain_id=324, short_name="zksync", description="zkSync Mainnet", currency="ETH"
    ),
    "scroll": Blockchain(network="scroll", chain_id=534352, short_name="scroll", description="Scroll", currency="ETH"),
    "avalanche": Blockchain(
        network="avalanche", chain_id=43114, short_name="avalanche", description="Avalanche C-Chain", currency="AVAX"
    ),
    "fantom": Blockchain(
        network="fantom", chain_id=250, short_name="fantom", description="Fantom Opera", currency="FTM"
    ),
}
