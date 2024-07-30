# Monitoring Contract

## Contract Data Model

| Field Name       | Field Type | Notes |
| ---------------- | ---------- | ----- |
| contract_address | STRING     |       |
| network          | STRING     |       |

## Local

Properties

- `contracts(self) -> List[Contract]`
	- returns the list of monitored contracts

Methods

- `update(self) -> None`
	- Update Local Monitored Contracts list
	- The `update_interval` paramater: will trigger update every N secs

- `exists(self, address: str) -> bool`
	- returns True if address is in monitored contracts list

## Remote

Properties

- `contracts(self) -> List[Contract]`
	- returns the list of monitored contracts

Methods

- `update(self) -> None`
	- Update Local Monitored Contracts list
	- The `update_interval` paramater: will trigger update every N secs

- `exists(self, address: str) -> bool`
	- returns True if address is in monitored contracts list
