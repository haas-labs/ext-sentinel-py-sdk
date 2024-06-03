# Registry

A container to hold metrics collectors.

Collectors in the registry must comply with the Collector interface which means that they inherit 
from the base Collector object and implement a no-argument method called 'get_all' that returns 
a list of Metric instance objects.

## Methods

### register(self, collector: Collector)

Register a collector into the container. The registry provides a container that can be used to 
access all metrics when exposing them into a specific format.

### deregister(self, name: str)

Deregister a collector. This will stop the collector metrics from being emitted.

### get(self, name: str)

Get a collector by name.

### get_all(self)

Return a list of all collectors

### dump_all(self)

Return dump of all collectors in MetricModel format for publishing in metrics queue

### clear(self)

Clear all registered collectors. This function is mainly of use in tests to reset the default 
registry which may be used in multiple tests.

