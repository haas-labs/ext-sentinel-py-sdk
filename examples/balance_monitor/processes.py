import time
import logging

from typing import List

from web3 import Web3
from web3.eth import AsyncEth

import uuid

from sentinel.processes.block import BlockDetector
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction

logger = logging.getLogger(__name__)
db_name = "address"


class BalanceMonitor(BlockDetector):
    async def init(self):
        logger.info("User defined init process started")
        addresses: list = self.databases[db_name].all()
        self.balances = {a: 0 for a in addresses}

        self.decimals = 10 ** self.parameters.get("decimals", 18)
        self.threshold = self.parameters.get("balance_threshold")
        self.severity = self.parameters.get("severity",0.14)
        logger.info(f"Using balance threshold: {self.threshold} ({self.threshold / self.decimals})")

        rpc_url = self.parameters.get("rpc")
        self.w3 = Web3(Web3.AsyncHTTPProvider(rpc_url), modules={"eth": (AsyncEth,)}, middlewares=[])

        self.balances = {a: await self.check_addr(a,None) for a in addresses}
        for addr, bal in self.balances.items():
            logger.info(f"Initial balance value: {addr}: {bal} ({bal / self.decimals})")            


    async def ask_balance(self, addr: str) -> int:
        balance = await self.w3.eth.get_balance(self.w3.to_checksum_address(addr))
        # cache
        self.balances[addr] = balance
        logger.debug("Balance: %s: %d (%.4f)", addr, balance, balance)
        return balance

    def get_balance(self, addr):
        return self.balances[addr]

    async def check_addr(self, addr, tx):
        balance = await self.ask_balance(addr)        
        #logger.debug(f"BALANCE: {addr}: {balance} ({balance / self.decimals})")
        
        if tx is not None: 
            tx_hash = tx.hash
            block_number = tx.block.number
        else:
            tx_hash = ""
            block_number = ""

        if balance <= self.threshold:
            logger.warn(
                "Balance below threshold: %s: %.4f =< %.4f (block=%s, tx=%s)",
                addr,
                balance / self.decimals,
                self.threshold / self.decimals,
                block_number,
                tx_hash,
            )
            await self.send_notification(addr, balance, tx)
        
        # return balance    
        return balance

    async def on_block(self, transactions: List[Transaction]) -> None:

        detected = False
        for tx in transactions:
            # ignore transactions not to our address
            addr_from = self.databases[db_name].exists(tx.from_address)
            addr_to = self.databases[db_name].exists(tx.to_address)
            if addr_from:
                logger.info(f"Detected: {addr_from}")
                await self.check_addr(tx.from_address, tx)
                detected = True
            if addr_to:
                logger.info(f"Detected: {addr_to}")
                await self.check_addr(tx.to_address, tx)
                detected = True

        if not detected:
            logger.info("Block: %s", tx.block.number)

    async def send_notification(self, addr: str, balance: int, tx: Transaction) -> None:        
        if tx is not None:
            tx_ts = tx.block.timestamp
            tx_hash = tx.hash
            tx_from = tx.from_address
            tx_to = tx.to_address
            tx_value = tx.value
        else:
            tx_ts = int(time.time() * 1000)
            tx_hash = ""
            tx_from = ""
            tx_to = ""
            tx_value = balance

        logger.info(f"--> Event: {tx_ts}: {addr}, {balance}, {tx}")

        await self.channels["events"].send(
            Event(
                did=self.detector_name,
                eid = uuid.uuid4().hex,
                type="balance_threshold",
                severity=self.severity,
                sid = "ext:sentinel",
                ts = tx_ts,
                blockchain=Blockchain(
                    network=self.parameters["network"],
                    chain_id=str(self.parameters["chain_id"]),
                ),
                metadata={
                    "tx_hash": tx_hash,
                    "tx_from": tx_from,
                    "tx_to": tx_to,
                    "value": tx_value,
                    "monitored_contract": addr,
                    "balance": balance,
                    "threshold": self.threshold,
                    "desc": f"Balance Change below threshold ({balance / self.decimals}, {self.threshold / self.decimals})",
                },
            )
        )
