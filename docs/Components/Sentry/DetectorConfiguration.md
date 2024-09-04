# Detector Configuration

The detector configurations are managed through two main options: static and dynamic. 

- Static configuration involves settings established before the detector starts, which cannot be changed during runtime and require a restart for any updates. 
- Dynamic configuration allows for real-time adjustments and additions while the detector is running, including the ability to customize options on a per-address basis. This flexibility enables the adaptation of detection parameters as conditions change or new requirements arise.
## Detector Schema

For dynamic configuration in Extractor, you need to create a detector schema and register it with the Extractor. This allows for real-time adjustments and customization while the detector is active.

```python
class Schema(BaseSchema):
   erc20_addr: str = Field(title="ERC20 Address", description="ERC20 Address")
   erc20_balance_threshold: int = Field(title="ERC20 Balance Threshold", default=300000000000)
   erc20_decimals: int = Field(title="ERC20 Decimals", description="ERC20 Decimals", default=8)
   balance_threshold: float = Field(title="Balance Threshold")
   severity: Severity = Field(title="Severity", description="Severity", default=Severity.INFO)
   decimals: int = Field(title="Decimals", description="Decimals", default=18)
)
```

## Local Use

```yaml
- name: BalanceMonitorDetector
  type: balance_monitor.sentry.BalanceMonitorDetector
  description: >
    Detector for tracking different activities with and against monitored contract
  parameters:
    network: {{ blockchain_network }}
    rpc_url: {{ rpc_url_var_name }}
  inputs:
  - balance_monitor/local/fs/transaction
  outputs:
  - balance_monitor/local/fs/event
  databases:
  - balance_monitor/local/fs/monitored_contract
```

## Hacken Cloud

```yaml
- name: BalanceMonitorDetector
  type: balance_monitor.sentry.BalanceMonitorDetector
  description: >
    Detector for tracking different activities with and against monitored contract
  parameters:
    network: {{ blockchain_network }}
    rpc_url: {{ rpc_url_var_name }}
  inputs:
  - hacken/cloud/kafka/transaction
  outputs:
  - hacken/cloud/kafka/event
  databases:
  - hacken/cloud/monitored_contract
```

## The difference between local configuration and Hacken Cloud

| Channel   | Local Use                                   | Hacken Cloud (production)       |
| --------- | ------------------------------------------- | ------------------------------- |
| inputs    | balance_monitor/local/fs/transaction        | hacken/cloud/kafka/transaction  |
| outputs   | balance_monitor/local/fs/event              | hacken/cloud/kafka/event        |
| databases | balance_monitor/local/fs/monitored_contract | hacken/cloud/monitored_contract |
