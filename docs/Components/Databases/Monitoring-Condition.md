# Monitoring Condition

## Core

Properties

- `size(self) -> int`
	- returns the number of monitoring conditions in the database

Methods

- `update(self, conditions: Conditions) -> None`
	- update conditions in the database

- `has_address(self, address: str) -> bool`
	- return True if address in the database else False

## Remote

Based on Core Monitoring Condition Database

Properties

- addresses(self) -> Dict[str, Dict[int, Configuration]]
	- returns the list of addresses with monitoring conditions

Methods

- `get_address_conditions(self, address: str) -> Iterator[Configuration]`
	- returns monitoring conditions for specific address

- `update(self, record: aiokafka.ConsumerRecord) -> None`
	- update monitoring condition in database based on incoming Kafka record

- `ingest(self) -> None`
	- ingest all monitoring conditions from Kafka topic

Helpers

- `get_group_id(self) -> str`
	- returns Kafka group id

- `get_address(self, config: Configuration) -> str`
	- returns address or proxy
