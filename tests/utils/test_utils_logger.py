import pytest
import logging

from sentinel.utils.logger import Logger
from sentinel.utils.logger import get_logger


def test_utils_get_logger_with_level():
    logger = get_logger(name="TestLogger#1", log_level="INFO")
    assert isinstance(logger, Logger), "Incorrect logger type"
    assert logger.name == "TestLogger#1", "Incorrect logger name"
    assert logger.level == logging.INFO, "Incorrect logging level"

    logger = get_logger(name="TestLogger#2", log_level=logging.INFO)
    assert isinstance(logger, Logger), "Incorrect logger type"
    assert logger.name == "TestLogger#2", "Incorrect logger name"
    assert logger.level == logging.INFO, "Incorrect logging level"

    with pytest.raises(ValueError):
        logger = get_logger(name="TestLogger", log_level="UNKNOWN")
