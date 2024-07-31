# Databases

- [Address](Address.md)
- [Blacklist](Blacklist.md)
- [Contract](Contract.md)
- [Label](Label.md)
- [Mixer](Mixer.md)
- [Monitoring-Contract](Monitoring-Contract.md)
- [Monitoring-Condition](Monitoring-Condition.md)
- [Monitoring-Target](Monitoring-Target.md)
- [Trace](Trace.md)
- [Account](Account.md)
- [DEX](DEX.md)

## Data Models per database

| Database             | Fields                    | Notes                                 |
| -------------------- | ------------------------- | ------------------------------------- |
| Address \| Common    | address                   |                                       |
| Address \| Local     | address                   |                                       |
| Address \| Remote    | address                   |                                       |
| Blacklist \| Local   | address                   |                                       |
| Blacklist \| Remote  | address                   |                                       |
| Contract \| Remote   | contract or abi signature |                                       |
| Label                | label db record           |                                       |
| Mixer                | address                   |                                       |
| Monitoring Contract  | address, network          |                                       |
| Monitoring Condition | address, conditions       |                                       |
| Trace                | address, dictionary       | The dictionary contains trace details |
| Account              | address                   |                                       |
| DEX                  | address                   |                                       |
|                      |                           |                                       |
