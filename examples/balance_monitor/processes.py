import logging

from typing import List
from collections import defaultdict
from web3 import Web3

from sentinel.processes.block import BlockDetector
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction

logger = logging.getLogger(__name__)
db_name = "address"

class BalanceMonitor(BlockDetector):
    
    def __init__(self,name,description,inputs,outputs,databases,parameters):
        super().__init__(name,description,inputs,outputs,databases,parameters)
        
        addresses:list = self.databases[db_name].all("")
        self.balances = {value: 0.0 for value in addresses}
        logger.info(self.balances)

        self.threshold = 10.0

        self.w3 = Web3(Web3.HTTPProvider('http://geth.demo.hacken.cloud:8545'))

        for addr in self.balances:            
            self.askBalance(addr)

            
    def askBalance(self,addr):        
        balance = self.w3.eth.get_balance(self.w3.to_checksum_address(addr))
        #balance = 10.0
        self.balances[addr] = balance
        logger.info("Balance: %s: %.4f",addr,balance)
        return balance

    def getBalance(self,addr):
        self.balances[addr]

    async def on_block(self, transactions: List[Transaction]) -> None:
        
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
                    logger.warn("Balance change: %s: %.4f (block=%s: tx=%s)",addr,balance,tx.block.number,tx.hash)
                    await self.send_notification(addr,balance,tx)
        
        if not detected:
            logger.info("block: %s",tx.block.number)

    async def send_notification(self, addr, balance,transaction: Transaction) -> None:
        
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
