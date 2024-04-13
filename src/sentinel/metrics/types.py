from enum import Enum
from typing import Dict

# Types

BucketType = float
LabelsType = Dict[str, str]


class MetricsTypes(Enum):
    counter = 0
    gauge = 1
    summary = 2
    untyped = 3
    histogram = 4
    info = 5
    stateset = 6
