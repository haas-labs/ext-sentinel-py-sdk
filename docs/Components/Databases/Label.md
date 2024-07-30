# Label

## Label DB Record

| Field name | Field Type     | Notes |
| ---------- | -------------- | ----- |
| address    | STRING         |       |
| tags       | LIST OF STRING |       |
| category   | STRING         |       |

## Common

Properties

- `stats(self) -> Dict`
	- returns stats for local addresses by tags

Methods

- `current_time(self)`
	- returns current time in epoch time (seconds)

- `search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]`
	- search by tag(-s)

- `search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]`
	- search by address(-es)

- `add(self, address: str, tags: List[str], category: str) -> bool`
	- add address to label db

- `update(self)`
	- update local address db for predefined tags

- `has_tag(self, address: str, tag: str) -> bool`
	- returns True if the address has the tag
## Local

Based on Common Label DB

Methods

- `search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]`
	- search by tag(-s)

- `search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]`
	- search by address(-es)

- `add(self, address: str, tags: List[str], category: str) -> bool`
	- add address to label db

## Remote

Based on Common Label DB

Methods 

- `query(self, endpoint: str, query: Dict, fetch_all: bool = False) -> List[LabelDBRecord]`
	- Run query against remote LabelDB

- `search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]`
	- search by tag(-s)

- `search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]`
	- search by address(-es)

- `add(self, address: str, tags: List[str], category: str) -> bool`
	- add address to label db

