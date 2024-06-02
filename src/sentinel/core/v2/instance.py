from sentinel.core.v2.sentry import AsyncCoreSentry, CoreSentry
from sentinel.models.settings import Settings
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger

logger = get_logger(__name__)

TYPES_MAPPING = {
    "sentry": "sentries",
    "input": "inputs",
    "output": "outputs",
    "database": "databases",
}


def load_instance(type: str, id: str, settings: Settings) -> CoreSentry | AsyncCoreSentry:
    """
    Load sentry instance

    Parameters:
    @type: str, possible values: sentry, input, output, database
    @id: str, component identificator
    @settings: Settings, profile settings
    """
    settings_section = TYPES_MAPPING.get(type, None)
    if settings_section is None:
        known_types = ", ".join(TYPES_MAPPING.keys())
        raise ValueError(f"Unknown instance type, found: {type}, expected: {known_types}")

    kinds = [kind for kind in getattr(settings, settings_section) if kind.id == id]
    if len(kinds) > 1:
        raise ValueError(f"Detected more than one {type} with id: {id}")
    instance_settings = kinds[0]

    try:
        _, instance = import_by_classpath(instance_settings.type)
        return instance.from_settings(instance_settings)
    except ModuleNotFoundError as err:
        logger.error(f"{instance_settings.type}, {err}")
        return None
