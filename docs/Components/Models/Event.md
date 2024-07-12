# Event

## Event Structure

| Field name | Field type          | Default Value | Optional | Notes                                                                           |
| ---------- | ------------------- | ------------- | -------- | ------------------------------------------------------------------------------- |
| did        | STRING              |               |          | Sentinel detector ID, currently: detector name + version(optional)              |
| eid        | STRING              |               |          | Event UUID, auto-generated                                                      |
| cid        | INTEGER             |               | YES      | Extractor Detector Config id                                                    |
| sid        | STRING              | `ext:ad`      |          | Source ID, Possible values: `ext:ad`, `sentinel`, ...                           |
| category   | STRING              | `EVENT`       |          | Event Category: `EVENT` (default) or `ALERT` or ...                             |
| type       | STRING              |               |          | Event Type                                                                      |
| severity   | FLOAT               |               |          | Event/Alert Severity                                                            |
| desc       | STRING              |               | YES      | Event/Alert Description                                                         |
| ts         | INT                 |               |          | Timestamp in epoch time with milliseconds                                       |
| blockchain | Blockchain          |               |          | Chain name and id, see [Blockchain structure](Blockchain.md)                    |
| metadata   | MAP<STRING, STRING> |               |          | Key/Value for Events metadata: tx_hash, tx_from, tx_to, monitored_contract, ... |
