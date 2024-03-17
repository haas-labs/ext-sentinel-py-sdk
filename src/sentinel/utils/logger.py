import logging

from typing import Union


def get_logger(name: str, log_level: Union[str, int]) -> logging.Logger:
    """
    return Logger with required formatting
    """
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level)
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(
        fmt=logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d (%(processName)s/%(name)s:%(lineno)d) [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger
