# Address Databases

## Common

Methods:

- `check(address: str) -> bool`
	- return True if address exists in pre-loaded local account addresses or contract addresses. If the address isn't found, check remote service (Label DB)
## Local

The local database for storing address list

Methods:

- internal `_import(path: pathlib.Path)
	- import addresses from file

- `exists(address: str) -> bool`
	- returns True if address exists in local database

- `all() -> List[str]`
	- returns a list of addresses in local database
## Remote

Based on [[#Common]] database

Methods:

- internal `_fetch(address: str) -> AddressType
	- fetch information from remote Label DB and returns information about address type: contract or undefined (no ABI available)
## In-Memory

The in-memory database for storing addresses and their metadata. Where Metadata refers to pydantic.BaseModel

Methods:

- `put(address: str, metadata: Metadata) -> None:`
	- store address and its metadata in local database

- `exists(address: str) -> bool`
	- returns True if the address exists in local database

- `get(address: str) -> Metadata`
	- returns the address metadata if exists or None 

- `remove(address: str) -> None`
	- remove address information from local database

- `all() -> Dict[Address, Metadata]`
	- return a dictionary with addresses and their metadata

Properties

- `size`
	- return the number of records in local database
