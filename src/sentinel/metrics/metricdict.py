# Based on https://github.com/claws/aioprometheus

import re
import json

from collections import OrderedDict
from collections.abc import MutableMapping

# Sometimes python will access by string for example iterating objects, and
# it has this notation
regex = re.compile(r"\{.*:.*,?\}")


# http://stackoverflow.com/questions/3387691/python-how-to-perfectly-override-a-dict
class MetricDict(MutableMapping):
    """
    MetricDict stores the data based on the labels so we need to generate
    custom hash keys based on the labels
    """

    EMPTY_KEY = "__EMPTY__"

    def __init__(self, *args, **kwargs):
        self.store = {}
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        # Sometimes we need empty keys
        if not key or key == MetricDict.EMPTY_KEY:
            return MetricDict.EMPTY_KEY

        # Python accesses by string key so we allow if is str and
        # 'our custom' format
        if isinstance(key, bytes) and regex.match(key.decode()):
            return key

        if not isinstance(key, dict):
            raise TypeError("Only accepts dicts as keys")
        key = OrderedDict(sorted(key.items()))
        return bytes(json.dumps(key, separators=(',', ':')), encoding="utf-8")
