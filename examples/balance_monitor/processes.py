import logging

from typing import List, Dict

from web3 import Web3
from web3.eth import AsyncEth

from sentinel.processes.block import BlockDetector
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction

logger = logging.getLogger(__name__)
db_name = "address"


class BalanceMonitor(BlockDetector):
    def init(self, parameters: Dict):
        addresses: list = self.databases[db_name].all()
        self.balances = {value: 0.0 for value in addresses}
        logger.info(f"Initial balance values: f{self.balances}")
        self.balances_initialized = False

        self.threshold = parameters.get("balance_threshold", 10.0)
        logger.info(f"Using balance threshold: {self.threshold}")

        rpc_proxy_node_url = parameters.get("rpc_proxy_node")
        self.w3 = Web3(Web3.AsyncHTTPProvider(rpc_proxy_node_url), modules={"eth": (AsyncEth,)}, middlewares=[])

    async def askBalance(self, addr: str) -> int:
        balance = await self.w3.eth.get_balance(self.w3.to_checksum_address(addr))
        # balance = 10.0
        self.balances[addr] = balance
        logger.info("Balance: %s: %.4f", addr, balance)
        return balance

    def getBalance(self, addr):
        return self.balances[addr]

    async def on_block(self, transactions: List[Transaction]) -> None:
        if not self.balances_initialized:
            for addr in self.balances:
                await self.askBalance(addr)
            self.balances_initialized = True

        detected = False
        for tx in transactions:
            # ignore transactions not to our address
            if self.databases[db_name].exists(tx.to_address) or self.databases[db_name].exists(tx.from_address):
                if self.databases[db_name].exists(tx.to_address):
                    addr = tx.to_address
                else:
                    addr = tx.from_address

                detected = True
                # get current balance
                balance = self.askBalance(addr)

                if balance <= self.threshold:
                    logger.warn("Balance change: %s: %.4f (block=%s: tx=%s)", addr, balance, tx.block.number, tx.hash)
                    await self.send_notification(addr, balance, tx)

        if not detected:
            logger.info("Block: %s", tx.block.number)

    async def send_notification(self, addr, balance, transaction: Transaction) -> None:
        await self.channels["events"].send(
            Event(
                did=self.detector_name,
                type="balance_change",
                severity=0.3,
                ts=transaction.block.timestamp * 1000,
                blockchain=Blockchain(
                    network=self.parameters["network"],
                    chain_id=str(self.parameters["chain_id"]),
                ),
                metadata={
                    "tx_hash": transaction.hash,
                    "tx_from": transaction.from_address,
                    "tx_to": transaction.to_address,
                    "value": transaction.value,
                    "addr": addr,
                    "balance": balance,
                    "desc": "Balance Change",
                },
            )
        )
