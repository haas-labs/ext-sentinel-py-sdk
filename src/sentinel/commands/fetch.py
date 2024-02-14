import sys
import json
import logging
import pathlib

from enum import Enum

from sentinel.commands.common import Command
from sentinel.services.fetcher import Fetcher


logger = logging.getLogger(__name__)


class DatasetType(Enum):
    """
    Dataset Types
    """

    block = "block"
    transaction = "transaction"
    trace = "trace"
    trace_transaction = "trace_transaction"
    debug_trace_transaction = "debug_trace_transaction"

    def __str__(self) -> str:
        return self.value


class FetchCommand(Command):
    """
    Fetch Command
    """

    name = "fetch"
    help = "Fetch data via JSON-RPC"

    def add(self):
        """
        Add Fetch command and arguments
        """
        self._parser.add_argument(
            "--rpc", type=str, required=True, help="JSON-RPC End-Point"
        )
        self._parser.add_argument(
            "--dataset",
            type=DatasetType,
            choices=list(DatasetType),
            help="Dataset type for fetching",
        )
        self._parser.add_argument(
            "--from-file", type=pathlib.Path, required=True, help="Fetch data from list"
        )
        self._parser.add_argument(
            "--to-file", type=pathlib.Path, help="Store results into file"
        )

        self._parser.set_defaults(handler=self.handle)

        return self._parser

    def handle(self, args):
        """
        Handling Fetch command arguments
        """
        super().handle(args)

        logger.info(f"Fetch {args.dataset} data via JSON-RPC endpont: {args.rpc}")
        fetcher = Fetcher(endpoint=args.rpc)

        try:
            if args.dataset == DatasetType.block:
                self.handle_blocks(
                    fetcher=fetcher,
                    source_path=args.from_file,
                    target_path=args.to_file,
                )

            elif args.dataset == DatasetType.transaction:
                self.handle_transactions(
                    fetcher=fetcher,
                    source_path=args.from_file,
                    target_path=args.to_file,
                )

            elif args.dataset == DatasetType.trace_transaction:
                self.handle_trace_transactions(
                    fetcher=fetcher,
                    source_path=args.from_file,
                    target_path=args.to_file,
                )

            elif args.dataset == DatasetType.debug_trace_transaction:
                self.handle_debug_trace_transactions(
                    fetcher=fetcher,
                    source_path=args.from_file,
                    target_path=args.to_file,
                )

            else:
                logger.error(f"Unknown dataset: {args.dataset}")
        except KeyboardInterrupt:
            logger.warning("Interrupted by user")

    def handle_blocks(
        self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path
    ) -> None:
        """
        Handle fetch block transactions
        """
        with source_path.open("r") as source:
            block_nums = [
                blk_nm.strip() for blk_nm in source.readlines() if blk_nm != ""
            ]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                for transaction in fetcher.get_block_transactions(block_nums):
                    target.write(f"{json.dumps(transaction)}\n")
            finally:
                target.close()

    def handle_transactions(
        self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path
    ) -> None:
        """
        Handle fetch transactions
        """
        with source_path.open("r") as source:
            tx_hashes = [tx.strip() for tx in source.readlines() if tx != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                for transaction in fetcher.get_transactions(tx_hashes):
                    target.write(f"{json.dumps(transaction)}\n")
            finally:
                target.close()

    def handle_trace_transactions(
        self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path
    ) -> None:
        """
        Handle Trace Transactions
        """
        with source_path.open("r") as source:
            tx_requests = [tx.strip() for tx in source.readlines() if tx != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                for trace in fetcher.get_trace_transaction(tx_requests):
                    target.write(f"{json.dumps(trace)}\n")
            finally:
                target.close()

    def handle_debug_trace_transactions(
        self, fetcher: Fetcher, source_path: pathlib.Path, target_path: pathlib.Path
    ) -> None:
        """
        Handle Debug Trace Transactions
        """
        with source_path.open("r") as source:
            tx_requests = [tx.strip() for tx in source.readlines() if tx != ""]
            target = target_path.open("w") if target_path else sys.stdout
            try:
                for trace in fetcher.get_debug_trace_transaction(tx_requests):
                    target.write(f"{json.dumps(trace)}\n")
            finally:
                target.close()
