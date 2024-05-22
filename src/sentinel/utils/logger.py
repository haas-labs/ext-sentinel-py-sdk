import logging
from typing import Union

# from rich.logging import RichHandler


class Logger:
    def __init__(self, name: str, log_level: Union[str, int] = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        format = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s) %(message)s"

        # Create a handler for writing to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(fmt=logging.Formatter(fmt=format, datefmt="%Y-%m-%dT%H:%M:%S"))

        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    @property
    def name(self):
        return self.logger.name

    @property
    def level(self):
        return self.logger.level

    def isEnabledFor(self, level: int):
        return self.logger.isEnabledFor(level)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warn(self, *args, **kwargs):
        self.logger.warn(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)


def get_logger(name: str, log_level: Union[str, int] = logging.INFO) -> Logger:
    logger = Logger(name=name, log_level=log_level)
    return logger


logger = Logger(name=__name__, log_level=logging.INFO)
