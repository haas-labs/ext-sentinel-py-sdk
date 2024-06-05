from typing import Any

from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger

logger = get_logger(__name__)


def load_instance(settings: list, **kwargs) -> Any:
    """
    Load sentry instance by its settings
    """

    try:
        _, instance = import_by_classpath(settings.type)
        return instance.from_settings(settings=settings, **kwargs)
    except ModuleNotFoundError as err:
        logger.error(f"{settings.type}, {err}")
        return None
