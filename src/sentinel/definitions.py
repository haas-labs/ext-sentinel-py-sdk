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
    "ethereum_sepolia": Blockchain(
        network="ethereum_sepolia", chain_id=11155111, short_name="sepolia", description="Sepolia", currency="ETH"
    ),
    "telos": Blockchain(
        network="telos", chain_id=40, short_name="telos", description="Telos EVM Mainnet", currency="TLOS"
    ),
    "vechain": Blockchain(
        network="vechain", chain_id=100009, short_name="vechain", description="VeChain Mainnet", currency="VET"
    ),
    "zeta": Blockchain(
        network="zeta", chain_id=7000, short_name="zeta", description="ZetaChain Mainnet", currency="ZETA"
    ),
    "polygon_amoy": Blockchain(
        network="polygon_amoy", chain_id=80002, short_name="amoy", description="Polygon Amoy Testnet", currency="POL"
    ),
    "ethereum_holesky": Blockchain(
        network="ethereum_holesky", chain_id=17000, short_name="holesky", description="Ethereum Holesky Testnet", currency="ETH"
    ),
}
