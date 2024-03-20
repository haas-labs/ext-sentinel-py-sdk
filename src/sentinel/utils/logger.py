import logging

from typing import Union
from rich.logging import RichHandler


def get_logger(name: str, log_level: Union[str, int], rich: bool = False) -> logging.Logger:
    """
    return Logger with required formatting
    """
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level)
    logger = logging.getLogger(name)

    handlers = [logging.StreamHandler()]

    format = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s/%(module)s:%(lineno)d) %(message)s"
    if rich:
        format = "%(asctime)s.%(msecs)03d (%(name)s/%(module)s:%(lineno)d) %(message)s"
        handlers.append(RichHandler(rich_tracebacks=True))

    for handler in handlers:
        handler.setFormatter(fmt=logging.Formatter(fmt=format, datefmt="%Y-%m-%dT%H:%M:%S"))
        logger.addHandler(handler)
    
    logger.setLevel(log_level)
    return logger
