# Based on https://github.com/claws/aioprometheus

from typing import Dict, Iterator

from sentinel.metrics.collector import Collector, MetricModel


class Registry:
    def __init__(self) -> None:
        self.collectors: Dict[str, Collector] = {}

    def register(self, collector: Collector) -> None:
        """
        Register a collector into the container.

        The registry provides a container that can be used to access all metrics
        when exposing them into a specific format.

        :param collector: A collector to register in the registry.

        :raises: TypeError if collector is not an instance of
          :class:`Collector`.

        :raises: ValueError if collector is already registered.
        """
        if not isinstance(collector, Collector):
            raise TypeError(f"Invalid collector type: {collector}")

        if collector.name in self.collectors:
            raise ValueError(f"A collector for {collector.name} is already registered")

        self.collectors[collector.name] = collector
        setattr(self, collector.name, collector)

    def deregister(self, name: str) -> None:
        """
        Deregister a collector.

        This will stop the collector metrics from being emitted.

        :param name: The name of the collector to deregister.

        :raises: KeyError if collector is not already registered.
        """
        delattr(self, name)
        del self.collectors[name]

    def get(self, name: str) -> Collector:
        """
        Get a collector by name.

        :param name: The name of the collector to fetch.

        :raises: KeyError if collector is not found.
        """
        return self.collectors[name]

    def get_all(self) -> Iterator[Collector]:
        """Return a list of all collectors"""
        for c in self.collectors.values():
            yield c

    def dump_all(self) -> Iterator[MetricModel]:
        """
        Return dump of all collectors in MetricModel format for publishing in metrics queue
        """
        for c in self.collectors.values():
            yield c.dump()

    def clear(self):
        """Clear all registered collectors.

        This function is mainly of use in tests to reset the default registry
        which may be used in multiple tests.
        """
        for name in list(self.collectors.keys()):
            self.deregister(name)
