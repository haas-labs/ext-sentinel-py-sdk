import os
import csv
import json
import asyncio
import logging
import pathlib

from argparse import ArgumentParser, Namespace
from typing import List

from sentinel.utils.settings import load_extra_vars
from sentinel.db.contract.remote import RemoteContractDB
from sentinel.services.service_account import import_service_tokens

from sentinel.commands.common import SentinelCommand
from sentinel.formats.mappings import NETWORKS_BY_ID

logger = logging.getLogger(__name__)


class Command(SentinelCommand):
    def description(self) -> str:
        return "ABI Signature fetcher"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

        parser.add_argument("--env-vars", type=str, help="Set environment variables from JSON/YAML file")
        parser.add_argument(
            "--from",
            dest="contract_list",
            type=pathlib.Path,
            required=True,
            help="The contract list, CSV file with address and network",
        )
        parser.add_argument(
            "--to",
            type=pathlib.Path,
            required=True,
            help="Store ABI signatures in the directory",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip existing contract(-s)",
        )

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)

        # Update env var from file
        if args.env_vars is not None:
            for k, v in load_extra_vars(
                [
                    f"@{args.env_vars}",
                ]
            ).items():
                os.environ[k] = v

        import_service_tokens()
        try:
            logger.info(f"Fetching ABI Signatures from the contract list, {args.contract_list}")
            contracts = [addr for addr in csv.DictReader(args.contract_list.open("r"))]
            asyncio.run(
                self.fetch_abi_signatures(
                    contracts=contracts,
                    skip_existing=args.skip_existing,
                    target_path=args.to,
                )
            )
        except KeyboardInterrupt:
            logger.warning("Interrupted by User")

    async def fetch_abi_signatures(
        self,
        contracts: List[str],
        skip_existing: bool,
        target_path: pathlib.Path,
    ) -> None:
        """
        Update ABI Signatures DB from contracts list
        """
        dbs = dict()
        for cid, contract in enumerate(contracts):
            # Check address
            contract_address = contract.get("address", None)
            if contract_address is None:
                logger.warning(f"Empty contract address: {contract_address}")
                continue

            # Collect chain details
            chain_id = contract["network_id"]
            network = NETWORKS_BY_ID.get(chain_id, None)
            if network is None:
                logger.warning(f"Unknown chain id: {chain_id}, network: {network}")
                continue

            # Check if a connection to Contract DB exists
            if chain_id not in dbs:
                dbs[chain_id] = RemoteContractDB(
                    endpoint_url=os.environ["HAAS_API_ENDPOINT_URL"],
                    token=os.environ["HAAS_API_TOKEN"],
                    network=network,
                    chain_id=chain_id,
                )

            abi_signatures = await dbs[chain_id].get_abi_signatures(contract_address)
            if len(abi_signatures) == 0:
                logger.info(f"No ABI signatures for chain id: {chain_id}, contract: {contract['address']}")
                continue

            if target_path is not None:
                os.makedirs(target_path / f"chain_id={chain_id}/", exist_ok=True)
                target_file = target_path / f"chain_id={chain_id}/{contract_address}.json"
                with target_file.open("w") as abi_signatures_file:
                    for signature in abi_signatures:
                        abi_signatures_file.write(f"{json.dumps(signature.model_dump())}\n")
