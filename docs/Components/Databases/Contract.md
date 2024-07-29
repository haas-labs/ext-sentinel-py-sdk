# Contract

- [ABI Signatures](ABI-Signatures/Index.md)

## Common

Methods:

- `get(self, address: str) -> Contract`
	- return contract details by address

## Remote

Methods

- `get(self, address: str, follow_impl: bool = False) -> Union[Contract, EndpointError]`
	- get contract details by address
	- `follow impl` flag is used when we need to get contract implementation. 

- `get_abi_signatures(self, address: str) -> List[ABISignature]`
	- returns the list of ABI signatures

## Utilities

- `get_abi_input_types(abi: ABIRecord) -> List[str]`
	- returns ABI Input types

- `get_abi_input_fields(abi: Dict) -> Dict[str, str]`
	- returns ABI Input fields (w/o indexed): field name and type

- `extract_data_from_topics(abi_record: ABIRecord, topics: List[str]) -> Dict`
	- Extract data from topics

- `extract_data_from_event_log(abi_record: ABIRecord, topics: List[str], data: str) -> Dict`
	- Extract data from event

- `to_signature_record(contract_address: str, abi_record: ABIRecord) -> ABISignature`
	- Convert ABI Record to ABI Signature Record
