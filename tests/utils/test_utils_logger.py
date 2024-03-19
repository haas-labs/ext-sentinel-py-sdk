import pytest
import logging

from rich.logging import RichHandler
from sentinel.utils.logger import get_logger


def test_utils_get_logger_with_level():
    logger = get_logger(name="TestLogger#1", log_level="INFO")
    assert isinstance(logger, logging.Logger), "Incorrect logger type"
    assert logger.name == "TestLogger#1", "Incorrect logger name"
    assert logger.level == logging.INFO, "Incorrect logging level"

    logger = get_logger(name="TestLogger#2", log_level=logging.INFO)
    assert isinstance(logger, logging.Logger), "Incorrect logger type"
    assert logger.name == "TestLogger#2", "Incorrect logger name"
    assert logger.level == logging.INFO, "Incorrect logging level"

    with pytest.raises(AttributeError):
        logger = get_logger(name="TestLogger", log_level="UNKNOWN")

def test_utils_get_logger_rich():

    logger = get_logger(name="TestLogger#1", log_level="INFO", rich=True)
    assert logger.level == logging.INFO, "Incorrect log level"
    assert len([h for h in logger.handlers if isinstance(h, RichHandler)]) > 0, "Incorrect number of rich handlers"
    assert len([h for h in logger.handlers if isinstance(h, logging.StreamHandler)]) > 0, "Incorrect number of stream handlers"
