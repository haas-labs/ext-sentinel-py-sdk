import pathlib

from typing import Any

import multiprocessing as mp

from sentinel.utils.logger import logger


class LocalChannel:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        logger.info(f"Channel: {self.name}, parameters: {kwargs}")
        self._settings = kwargs
        self._queue = mp.Queue()

        if kwargs.get("load_from_file", None):
            self.load_from_file(pathlib.Path(kwargs["load_from_file"]))

    @property
    def size(self):
        """
        returns channel's queue size
        """
        return self._queue.qsize()

    def is_empty(self):
        """
        returns True if channel's queue is empty
        """
        return True if self._queue.empty() else False

    def get(self):
        """
        get from a channel
        """
        pass

    def put(self, record: Any):
        """
        put to a channel
        """
        pass

    def load_from_file(self, path: pathlib.Path) -> None:
        """
        Load data into a channel from file
        """
        logger.info(f"Channel: {self.name}, loading data from file: {str(path)}")
