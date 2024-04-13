# Enum

Enum metric, which of a set of states is true.

Example usage:
```python
from prometheus_client import Enum

e = Enum('task_state', 'Description of enum',
  states=['starting', 'running', 'stopped'])
e.state('running')
```
The first listed state will be the default.
