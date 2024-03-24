from enum import Enum


class ComponentType(Enum):
    project = "project"

    sentry = "sentry"

    # inbound channel
    input = "input"

    # outbound channel
    output = "output"

    database = "database"

    def __str__(self):
        return self.value
