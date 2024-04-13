# Info

Info metric, key-value pairs.

Examples of Info include:
- Build information
- Version information
- Potential target metadata

Example usage:

```python
from prometheus_client import Info
i = Info('my_build', 'Description of info')
i.info({'version': '1.2.3', 'buildhost': 'foo@bar'})
```
