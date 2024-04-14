from enum import Enum
from typing import Dict

# Types

BucketType = float
LabelsType = Dict[str, str]


class MetricsTypes(Enum):
    untyped = 0
    counter = 1
    gauge = 2
    summary = 3
    histogram = 4
    info = 5
    stateset = 6
