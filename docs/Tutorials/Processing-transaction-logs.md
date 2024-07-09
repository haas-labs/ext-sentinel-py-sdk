# Processing Transaction Logs

Often, during analysing transaction data, there is needed to filter and parse specific events from transaction logs.
To make this process more simple, Sentinel SDK has function `filter_events` (module: sentinel.utils.transaction)

```python
def filter_events(log_entries: List[LogEntry], signatures: List[ABISignature]) -> Iterator[Dict]:
```
where
- log_entries: the list of transaction logs
- signatures: required ABI signatures, for more details check `sentinel.db.contract.abi.static` with several ERC20
    signatures (ABI_EVENT_OWNERSHIP_TRANSFERED, ABI_EVENT_UPGRADED, ABI_EVENT_WITHDRAWAL, ABI_EVENT_TRANSFER)

## Examples of use

```python
for event in filter_events(transaction.logs, [ABI_EVENT_TRANSFER]):
    # Skip processing if no monitored address founded in TRANSFER event
    if monitored_address != event.address:
        continue
```

The event structure
```python
@dataclass
class Event:
    address: str
    type: str
    fields: Dict[str, str]
```

where
- address: the value of `log_entry.address` in lower case
- type: the name of event from ABI
- fields: the dictionary with parsed fields

For better understanding of event fields, let's review example with TRANSFER event. According to ERC20 spec, 
we have next input fields

```json
"inputs": [
    {
        "internal_type": "address",
        "name": "from",
        "type": "address",
        "indexed": True,
    },
    {
        "internal_type": "address",
        "name": "to",
        "type": "address",
        "indexed": True,
    },
    {
        "internal_type": "uint256",
        "name": "value",
        "type": "uint256",
        "indexed": False,
    },
],
```

to get access for them

```python
from_address = event.fields.get("from")
to_address = event.fields.get("to")
value = event.fields.get("value")
```
