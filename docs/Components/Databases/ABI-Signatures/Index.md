# ABI Signatures

## Standard

The `StandardABISignatires` class help get access to ERC-20, ERC-721, ERC-1155 signatures

Properties

- `total_records`: returns total records number in database

Methods

- `update(self, standards: List[str] = list()) -> None`
	- Update local databases with ABI signatures the list of standard. 

- `search(self, standard: str = None, signature_type: str = None, signature_hash: str = None) -> Iterator[ABISignature]`
	- Search signatures

## Static

- ABI_EVENT_OWNERSHIP_TRANSFERED
- ABI_EVENT_UPGRADED
- ABI_EVENT_WITHDRAWAL
- ABI_EVENT_TRANSFER
- 