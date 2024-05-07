import sys
import json
import asyncio
import pathlib

from argparse import ArgumentParser, Namespace

from enum import Enum
from typing import List

from sentinel.utils.logger import logger
from sentinel.services.fetcher import Fetcher
from sentinel.commands.common import SentinelCommand


class DatasetType(Enum):
    """
    Dataset Types
    """

    block = "block"
    transaction = "transaction"
    trace = "trace"
    trace_transaction = "trace_transaction"
    debug_trace_transaction = "debug_trace_transaction"
    code = "code"

    def __str__(self) -> str:
        return self.value


class Command(SentinelCommand):
    def description(self) -> str:
        return "Fetch data via JSON-RPC"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument("--rpc", type=str, required=True, help="JSON-RPC End-Point")
        parser.add_argument(
            "--dataset",
            type=DatasetType,
            choices=list(DatasetType),
            help="Dataset type for fetching",
        )
        parser.add_argument("--from-file", type=pathlib.Path, required=True, help="Fetch data from list")
        parser.add_argument("--to-file", type=pathlib.Path, help="Store results into file")

    def run(self, opts: List[str], args: Namespace) -> None:
        asyncio.run(self._run(opts=opts, args=args))

    async def _run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        logger.info(f"Fetch {args.dataset} data via JSON-RPC endpont: {args.rpc}")
        fetcher = Fetcher(endpoint=args.rpc)

        try:
            match args.dataset:
                case DatasetType.block:
                    await self.handle_blocks(
                        fetcher=fetcher,
                        source_path=args.from_file,
                        target_path=args.to_file,
                    )
                case DatasetType.transaction:
                    await self.handle_transactions(
                        fetcher=fetcher,
                        source_path=args.from_file,
                        target_path=args.to_file,
                    )
                case DatasetType.trace_transaction:
                    await self.handle_trace_transactions(
                        fetcher=fetcher,
                        source_path=args.from_file,
                        target_path=args.to_file,
                    )
                case DatasetType.debug_trace_transaction:
                    await self.handle_debug_trace_transactions(
                        fetcher=fetcher,
                        source_path=args.from_file,
                        target_path=args.to_file,
                    )
                case DatasetType.code:
                    await self.handle_code(
                        fetcher=fetcher,
                        source_path=args.from_file,
                        target_path=args.to_file,
                    )
                case _:
                    logger.error(f"Unknown dataset: {args.dataset}")
        except KeyboardInterrupt:
            logger.warning("Interrupted by user")

    async def handle_blocks(self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path) -> None:
        """
        Handle fetch block transactions
        """
        with source_path.open("r") as source:
            block_nums = [blk_nm.strip() for blk_nm in source.readlines() if blk_nm != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                async for transaction in fetcher.get_block_transactions(block_nums):
                    target.write(f"{json.dumps(transaction)}\n")
            finally:
                target.close()

    async def handle_transactions(self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path) -> None:
        """
        Handle fetch transactions
        """
        with source_path.open("r") as source:
            tx_hashes = [tx.strip() for tx in source.readlines() if tx.strip() != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                async for transaction in fetcher.get_transactions(tx_hashes):
                    target.write(f"{json.dumps(transaction)}\n")
            finally:
                target.close()

    async def handle_trace_transactions(self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path) -> None:
        """
        Handle Trace Transactions
        """
        with source_path.open("r") as source:
            tx_requests = [tx.strip() for tx in source.readlines() if tx != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                async for trace in fetcher.get_trace_transaction(tx_requests):
                    target.write(f"{json.dumps(trace)}\n")
            finally:
                target.close()

    async def handle_debug_trace_transactions(
        self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path
    ) -> None:
        """
        Handle Debug Trace Transactions
        """
        with source_path.open("r") as source:
            tx_requests = [tx.strip() for tx in source.readlines() if tx != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                async for trace in fetcher.get_debug_trace_transaction(tx_requests):
                    target.write(f"{json.dumps(trace)}\n")
            finally:
                target.close()

    async def handle_code(self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path) -> None:
        """
        Handle Code
        """
        with source_path.open("r") as source:
            requests = [addr.strip() for addr in source.readlines() if addr != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                async for code in fetcher.get_code(requests):
                    target.write(f"{code}\n")
            finally:
                target.close()
