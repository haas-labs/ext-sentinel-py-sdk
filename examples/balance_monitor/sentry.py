import time
import uuid

from typing import List


from sentinel.definitions import BLOCKCHAIN
from sentinel.sentry.block_tx import BlockTxDetector
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction
from sentinel.db.contract.abi.erc20 import ERC20 as ERC20_ABI
from sentinel.utils.web3 import get_async_web3


class BalanceMonitor(BlockTxDetector):
    name = "BalanceMonitor"
    description = "Monitors Account/Contract balance (native token)"

    async def on_init(self):
        self.logger.info("init")
        addresses: list = self.databases.address.all()

        rpc_url = self.parameters.get("rpc")
        self.w3 = get_async_web3(rpc_url)

        self.native = self.parameters.get("native", "ETH")
        self.balances = {a: 0 for a in addresses}
        self.erc20_balances = {a: 0 for a in addresses}

        self.decimals = 10 ** self.parameters.get("decimals", 18)
        self.threshold = self.parameters.get("balance_threshold")
        self.erc20_addr = self.parameters.get("erc20_addr").lower()
        self.erc20_decimals = 10 ** self.parameters.get("erc20_decimals", 18)
        self.erc20_balance_threshold = self.parameters.get("erc20_balance_threshold", 0)
        # Change to 0.14 when new FrontEnd UI is ready
        self.severity = self.parameters.get("severity", 0.15)

        self.erc20_contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.erc20_addr), abi=ERC20_ABI)

        self.erc20_token = await self.erc20_contract.functions.symbol().call()

        self.logger.info(
            f"Native ({self.native}) balance threshold: {self.threshold} ({self.threshold / self.decimals})"
        )
        self.logger.info(
            f"ERC20 ({self.erc20_token}/{self.erc20_addr}): balance threshold: {self.erc20_balance_threshold} ({self.erc20_balance_threshold / self.erc20_decimals})"
        )

        self.balances = {a: await self.check_addr(a, None) for a in addresses}
        self.erc20_balances = {a: await self.check_erc20_addr(a, None) for a in addresses}

        for addr, bal in self.balances.items():
            self.logger.info(f"Initial Native ({self.native}) balance: {addr}: {bal} ({bal / self.decimals})")

        for addr, bal in self.erc20_balances.items():
            self.logger.info(f"Initial ERC20 ({self.erc20_token}) balance: {addr}: {bal} ({bal / self.erc20_decimals})")

    # Native -------------------------------------------------------------------------------------
    async def ask_balance(self, addr: str) -> int:
        balance = await self.w3.eth.get_balance(self.w3.to_checksum_address(addr))
        # cache
        self.balances[addr] = balance
        self.logger.debug("Balance: %s: %d (%.4f)", addr, balance, balance)
        return balance

    def get_balance(self, addr):
        return self.balances[addr]

    async def check_addr(self, addr, tx):
        balance = await self.ask_balance(addr)
        # logger.debug(f"BALANCE: {addr}: {balance} ({balance / self.decimals})")

        if tx is not None:
            tx_hash = tx.hash
            block_number = tx.block.number
        else:
            tx_hash = ""
            block_number = ""

        if balance <= self.threshold:
            self.logger.warn(
                "Native (%s) balance below threshold: %s: %.4f =< %.4f (block=%s, tx=%s)",
                self.native,
                addr,
                balance / self.decimals,
                self.threshold / self.decimals,
                block_number,
                tx_hash,
            )
            await self.send_notification(addr, self.native, balance, tx)

        # return balance
        return balance

    # ERC20 -------------------------------------------------------------------------------------
    async def ask_erc20_balance(self, addr: str, token_addr: str, token: str) -> int:
        balance = await self.erc20_contract.functions.balanceOf(self.w3.to_checksum_address(addr)).call()
        # cache
        self.erc20_balances[addr] = balance
        self.logger.debug("ERC20 Balance: %s: %s=%d (%.4f)", addr, token, balance, balance)
        return balance

    def get_erc20_balance(self, addr):
        return self.erc20_balances[addr]

    async def check_erc20_addr(self, addr, tx):
        token_addr = self.erc20_addr
        token = self.erc20_token

        balance = await self.ask_erc20_balance(addr, token_addr, token)
        # logger.debug(f"BALANCE: {addr}: {balance} ({balance / self.decimals})")

        if tx is not None:
            tx_hash = tx.hash
            block_number = tx.block.number
        else:
            tx_hash = ""
            block_number = ""

        if balance <= self.erc20_balance_threshold:
            self.logger.warn(
                "ERC20 (%s) balance below threshold: %s: %s: %.4f =< %.4f (block=%s, tx=%s)",
                token,
                addr,
                token_addr,
                balance / self.erc20_decimals,
                self.erc20_balance_threshold / self.erc20_decimals,
                block_number,
                tx_hash,
            )
            await self.send_notification(addr, token, balance, tx)

        # return balance
        return balance

    async def on_block(self, transactions: List[Transaction]) -> None:
        detected = False
        for tx in transactions:
            # ignore transactions not to our address
            addr_from = self.databases.address.exists(tx.from_address)
            addr_to = self.databases.address.exists(tx.to_address)
            if addr_from:
                self.logger.info(f"Detected: {addr_from}")
                await self.check_addr(tx.from_address, tx)
                await self.check_erc20_addr(tx.from_address, tx)
                detected = True
            if addr_to:
                self.logger.info(f"Detected: {addr_to}")
                await self.check_addr(tx.to_address, tx)
                await self.check_erc20_addr(tx.to_address, tx)
                detected = True

        if not detected:
            self.logger.info("Block: %s", tx.block.number)

    async def send_notification(self, addr: str, token: str, balance: int, tx: Transaction) -> None:
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

        self.logger.info(f"--> Event: {tx_ts}: {addr}, {balance}, {tx}")

        await self.outputs.events.send(
            Event(
                did=f"{self.name}-{token}",
                eid=uuid.uuid4().hex,
                type="balance_threshold",
                severity=self.severity,
                sid="ext:sentinel",
                ts=tx_ts,
                blockchain=Blockchain(
                    network=self.parameters["network"],
                    chain_id=str(BLOCKCHAIN.get(self.parameters["network"]).chain_id),
                ),
                metadata={
                    "tx_hash": tx_hash,
                    "tx_from": tx_from,
                    "tx_to": tx_to,
                    "token": token,
                    "value": tx_value,
                    "monitored_contract": addr,
                    "balance": balance,
                    "threshold": self.threshold,
                    "desc": f"Balance {token} below threshold ({balance / self.decimals}, {self.threshold / self.decimals})",
                },
            )
        )
