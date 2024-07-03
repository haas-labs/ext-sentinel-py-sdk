from typing import AsyncIterator, Dict, List, Union

import httpx
from rich.progress import Progress
from sentinel.formats.mappings import (
    JSONRPC_BLOCK_FIELD_IGNORE_LIST,
    JSONRPC_BLOCK_FIELD_MAPPINGS,
    JSONRPC_BLOCK_FIELD_TRANSFORM,
    JSONRPC_TRANSACTION_FIELD_IGNORE_LIST,
    JSONRPC_TRANSACTION_FIELD_MAPPINGS,
    JSONRPC_TRANSACTION_FIELD_TRANSFORM,
    JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_IGNORE_LIST,
    JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_MAPPINGS,
    JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_TRANSFORM,
)
from sentinel.utils.dicts import (
    dict_fields_filter,
    dict_fields_mapping,
    dict_fields_transform,
    dicts_merge,
)
from sentinel.utils.logger import get_logger

JSONRPC_VERSION = "2.0"
HEADERS = {
    "Content-Type": "application/json",
}
DEFAULT_CONNECTION_TIMEOUT = 60


class JsonRpcRequest:
    """
    JSON RPC Request
    """

    def __init__(self, rpc: str, method: str, params: List):
        """
        JSON RPC Request Init
        """
        self.url = rpc
        self.data = {
            "jsonrpc": JSONRPC_VERSION,
            "method": method,
            "params": params,
            "id": 1,
        }

    def to_dict(self):
        """
        Transform the request to Dict type
        """
        return {"url": self.url, "data": self.data}


class Fetcher:
    """
    JSON RPC Fetcher
    """

    def __init__(self, endpoint: str) -> None:
        """
        JSON RPC Fetcher Init
        """
        self.logger = get_logger(__name__)
        self.endpoint = endpoint

    async def fetch(self, request: JsonRpcRequest) -> Dict:
        """
        Fetch data by request
        """
        async with httpx.AsyncClient(
            verify=False,
            headers=HEADERS,
            timeout=DEFAULT_CONNECTION_TIMEOUT,
            follow_redirects=True,
        ) as httpx_async_client:
            response = await httpx_async_client.post(self.endpoint, json=request.data)
        if response.status_code == 200:
            data = response.json()
            if data.get("error", None):
                raise RuntimeError(f"request: {request.data}, response: {data}")
            else:
                return data.get("result", {})
        else:
            self.logger.error(f"RPC Data Fetching error code: {response.status_code}, request: {request.data}")
            self.logger.error(response.content)
            return None

    async def get_block_transactions(self, block_numbers: List[str]) -> AsyncIterator[Dict]:
        """
        Get Block Transactions

        Transactions Data contains merged data from
        - block
        - transaction
        - and transaction receipt
        """
        with Progress() as progress:
            fetching_blocks = progress.add_task("Fetching block transactions", total=len(block_numbers))
            for blk_nm in block_numbers:
                block_data = await self.get_block_by_number(blk_nm)
                transactions = block_data.get("transactions", [])
                block_data["transaction_count"] = len(transactions)
                block_data = dict_fields_filter(block_data, JSONRPC_BLOCK_FIELD_IGNORE_LIST)
                block_data = dict_fields_mapping(block_data, JSONRPC_BLOCK_FIELD_MAPPINGS)
                block_data = dict_fields_transform(block_data, JSONRPC_BLOCK_FIELD_TRANSFORM)

                fetching_transactions = progress.add_task(
                    f"Fetching transactions of block: {blk_nm}", total=len(transactions)
                )
                for tx_hash in transactions:
                    progress.update(fetching_transactions, advance=1)

                    tx_data = await self.get_transaction_by_hash(tx_hash)
                    if not tx_data:
                        continue

                    tx_receipt_data = await self.get_transaction_receipt_by_hash(tx_hash)
                    tx_data["logs"] = []
                    for log_data in tx_receipt_data.pop("logs", []):
                        log_data = dict_fields_filter(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_IGNORE_LIST)
                        log_data = dict_fields_mapping(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_MAPPINGS)
                        log_data = dict_fields_transform(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_TRANSFORM)
                        tx_data["logs"].append(log_data)

                    if tx_receipt_data:
                        tx_data = dicts_merge(tx_data, tx_receipt_data)

                    tx_data["block"] = block_data

                    tx_data = dict_fields_filter(tx_data, JSONRPC_TRANSACTION_FIELD_IGNORE_LIST)
                    tx_data = dict_fields_mapping(tx_data, JSONRPC_TRANSACTION_FIELD_MAPPINGS)
                    tx_data = dict_fields_transform(tx_data, JSONRPC_TRANSACTION_FIELD_TRANSFORM)

                    if "root" not in tx_data:
                        tx_data["root"] = None

                    yield tx_data

                progress.update(fetching_blocks, advance=1)

    async def get_transactions(self, tx_hashes: List[str]) -> AsyncIterator[Dict]:
        """
        Get Transactions Data

        Transactions Data contains merged data from
        - block
        - transaction
        - and transaction receipt
        """
        for tx_hash in tx_hashes:
            if not tx_hash:
                self.logger.error("The hash field required for fetching transaction data")
                continue

            tx_data = await self.get_transaction_by_hash(tx_hash)
            if not tx_data:
                continue

            tx_receipt_data = await self.get_transaction_receipt_by_hash(tx_hash)
            tx_data["logs"] = []
            for log_data in tx_receipt_data.pop("logs", []):
                log_data = dict_fields_filter(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_IGNORE_LIST)
                log_data = dict_fields_mapping(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_MAPPINGS)
                log_data = dict_fields_transform(log_data, JSONRPC_TRANSACTION_RECEIPT_LOG_FIELD_TRANSFORM)
                tx_data["logs"].append(log_data)

            if tx_receipt_data:
                tx_data = dicts_merge(tx_data, tx_receipt_data)

            block_data = await self.get_block_by_hash(tx_data.get("blockHash"))
            block_data["transaction_count"] = len(block_data.get("transactions", []))
            block_data = dict_fields_filter(block_data, JSONRPC_BLOCK_FIELD_IGNORE_LIST)
            block_data = dict_fields_mapping(block_data, JSONRPC_BLOCK_FIELD_MAPPINGS)
            block_data = dict_fields_transform(block_data, JSONRPC_BLOCK_FIELD_TRANSFORM)
            tx_data["block"] = block_data

            tx_data = dict_fields_filter(tx_data, JSONRPC_TRANSACTION_FIELD_IGNORE_LIST)
            tx_data = dict_fields_mapping(tx_data, JSONRPC_TRANSACTION_FIELD_MAPPINGS)
            tx_data = dict_fields_transform(tx_data, JSONRPC_TRANSACTION_FIELD_TRANSFORM)

            if "root" not in tx_data:
                tx_data["root"] = None

            yield tx_data

    # TODO update the code
    # def get_trace_calls(self, tx_hashes: List[str]):
    #     '''
    #     Get Trace Calls
    #     '''
    #     for tx_hash in tx_hashes:
    #         trace_call_data = self.get_trace_call(from_address=None, to_address=tx_hash)
    #         if not trace_call_data:
    #             continue
    #         logger.info(trace_call_data)

    # TODO update the code
    # def get_trace_transactions(self, tx_hashes: List[str]):
    #     '''
    #     Get Trace Transaction
    #     '''
    #     for tx_hash in tx_hashes:
    #         trace_data = self.get_transaction_trace(transaction_hash=tx_hash)
    #         if not trace_data:
    #             continue
    #         logger.info(trace_data)

    # TODO update the code
    # def get_debug_trace_calls(self, tx_hashes: List[str]):
    #     '''
    #     Get Debug Trace Calls
    #     '''
    #     for tx_hash in tx_hashes:
    #         trace_data = self.get_debug_trace_call(transaction_hash=tx_hash)
    #         print(trace_data)
    #         if not trace_data:
    #             continue
    #         logger.info(trace_data)

    def transform_transaction_fields(self, transaction: Dict) -> Dict:
        """
        Transform Transaction Fields
        """
        # logger.info(transaction)
        transaction["block_timestamp"] = int(transaction["block_timestamp"], 0)
        return transaction

    async def get_block_by_number(self, block_number: str, transaction_detail_flag: bool = False) -> Dict:
        """
        returns block data by number
        """
        return await self.fetch(
            JsonRpcRequest(
                self.endpoint,
                method="eth_getBlockByNumber",
                params=[block_number, transaction_detail_flag],
            )
        )

    async def get_block_by_hash(self, block_hash: str, transaction_detail_flag: bool = False) -> Dict:
        """
        returns block data by hash
        """
        return await self.fetch(
            JsonRpcRequest(
                self.endpoint,
                method="eth_getBlockByHash",
                params=[block_hash, transaction_detail_flag],
            )
        )

    async def get_transaction_by_hash(self, transaction_hash: str) -> Dict:
        """
        returns transaction data by hash
        """
        return await self.fetch(
            JsonRpcRequest(
                self.endpoint,
                method="eth_getTransactionByHash",
                params=[transaction_hash],
            )
        )

    async def get_transaction_receipt_by_hash(self, transaction_hash: str) -> Dict:
        """
        returns transaction receipt data by hash
        """
        return await self.fetch(
            JsonRpcRequest(
                self.endpoint,
                method="eth_getTransactionReceipt",
                params=[transaction_hash],
            )
        )

    async def get_block_trace(self, block_number: str) -> Dict:
        """
        returns block trace
        """
        return await self.fetch(JsonRpcRequest(self.endpoint, method="trace_block", params=[block_number]))

    # TODO update the code
    # def get_transaction_trace(self, transaction_hash: str) -> Dict:
    #     '''
    #     returns transaction trace
    #     '''
    #     return self.fetch(JsonRpcRequest(self.endpoint,
    #                                      method='trace_transaction',
    #                                      params=[transaction_hash]))

    async def get_trace_transaction(self, tx_hash: Union[str, List[str]]) -> AsyncIterator[Dict]:
        """
        returns transaction trace
        """

        async def get_trace(tx_hash: str) -> Dict:
            return await self.fetch(
                JsonRpcRequest(
                    self.endpoint,
                    method="trace_transaction",
                    params=[
                        tx_hash,
                    ],
                )
            )

        if isinstance(tx_hash, str):
            yield await get_trace(tx_hash)

        elif isinstance(tx_hash, list):
            for tx in tx_hash:
                trace_data = await get_trace(tx)
                if not trace_data:
                    continue
                yield trace_data

    async def get_debug_trace_transaction(self, tx_hash: Union[str, List[str]]) -> AsyncIterator[Dict]:
        """
        returns transaction trace
        """

        async def get_trace(tx_hash: str) -> Dict:
            return await self.fetch(
                JsonRpcRequest(
                    self.endpoint,
                    method="debug_traceTransaction",
                    params=[tx_hash, {"tracer": "callTracer"}],
                )
            )

        if isinstance(tx_hash, str):
            yield await get_trace(tx_hash)

        elif isinstance(tx_hash, list):
            for tx in tx_hash:
                trace_data = await get_trace(tx)
                if not trace_data:
                    continue
                yield trace_data

    # TODO update the code
    # def get_debug_trace_call(self, from_address: str, to_address: str) -> Dict:
    #     '''
    #     returns debug transaction trace
    #     '''
    #     return self.fetch(JsonRpcRequest(self.endpoint,
    #                                      method='debug_traceCall',
    #                                      params=[{"to": to_address }]))

    # TODO update the code
    # def get_trace_call(self, from_address: str, to_address: str) -> Dict:
    #     '''
    #     returns transaction trace
    #     '''
    #     return self.fetch(JsonRpcRequest(self.endpoint,
    #                                      method='trace_call',
    #                                      params=[{"to": to_address }]))

    async def get_code(self, addr: Union[str, List[str]]) -> AsyncIterator[Dict]:
        """
        returns code by address or address list
        """

        async def _get_code(addr: str) -> Dict:
            return await self.fetch(
                JsonRpcRequest(
                    self.endpoint,
                    method="eth_getCode",
                    params=[addr, "latest"],
                )
            )

        if isinstance(addr, str):
            yield await _get_code(addr)

        elif isinstance(addr, list):
            for _addr in addr:
                code_data = await _get_code(_addr)
                if not code_data:
                    continue
                yield code_data
