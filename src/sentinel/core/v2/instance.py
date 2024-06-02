from typing import Any

from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger

logger = get_logger(__name__)


def load_instance(id: str, settings: list) -> Any:
    """
    Load sentry instance

    Parameters:
    @id: str, component identificator
    @settings: Settings, profile settings
    """

    kinds = [kind for kind in settings if kind.id == id]
    if len(kinds) > 1:
        raise ValueError(f"Detected more than one id: {id}")
    instance_settings = kinds[0]

    try:
        _, instance = import_by_classpath(instance_settings.type)
        return instance.from_settings(instance_settings)
    except ModuleNotFoundError as err:
        logger.error(f"{instance_settings.type}, {err}")
        return None
