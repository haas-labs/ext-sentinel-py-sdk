import logging

from typing import List

from web3 import Web3
from web3.eth import AsyncEth

from sentinel.processes.block import BlockDetector
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction

logger = logging.getLogger(__name__)
db_name = "address"


class BalanceMonitor(BlockDetector):
    async def init(self):
        logger.info("User defined init process started")
        addresses: list = self.databases[db_name].all()
        self.balances = {value: 0.0 for value in addresses}
        logger.info(f"Initial balance values: f{self.balances}")

        self.threshold = self.parameters.get("balance_threshold", 10000000000000000000000.0000)
        logger.info(f"Using balance threshold: {self.threshold}")

        rpc_proxy_node_url = self.parameters.get("rpc_proxy_node")
        self.w3 = Web3(Web3.AsyncHTTPProvider(rpc_proxy_node_url), modules={"eth": (AsyncEth,)}, middlewares=[])

        for addr in self.balances:
            await self.askBalance(addr)

    async def askBalance(self, addr: str) -> int:
        balance = await self.w3.eth.get_balance(self.w3.to_checksum_address(addr))
        # balance = 10.0
        self.balances[addr] = balance
        logger.debug("Balance: %s: %.4f", addr, balance)
        return balance

    def getBalance(self, addr):
        return self.balances[addr]

    async def check_addr(self, addr, tx):
        balance = await self.askBalance(addr)
        logger.info(f"Detected: {addr}: {balance}")

        if balance <= self.threshold:
            logger.warn("Balance change: %s: %.4f (block=%s: tx=%s)", addr, balance, tx.block.number, tx.hash)
            await self.send_notification(addr, balance, tx)

    async def on_block(self, transactions: List[Transaction]) -> None:
        # logger.info(f"transactions: {transactions}")

        detected = False
        for tx in transactions:
            # ignore transactions not to our address
            addr_from = self.databases[db_name].exists(tx.from_address)
            addr_to = self.databases[db_name].exists(tx.to_address)
            if addr_from:
                await self.check_addr(tx.from_address, tx)
                detected = True
            if addr_to:
                await self.check_addr(tx.to_address, tx)
                detected = True

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
