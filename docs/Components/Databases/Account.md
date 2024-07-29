# Suspicious Account Database

## Common

Methods

- `add(self, address: str) -> None`
	- Add address to local database

- `is_suspicios(self, address: str) -> bool`
	- returns True if address is suspicious

- `pull_changes(self, remote_uri: str) -> None`
	- Pull changes to remote DB
	
- `push_changes(self, remote_uri: str) -> None`
	- Push changes to remote DB
