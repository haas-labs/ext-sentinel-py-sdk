import pathlib

from typing import Dict

from sentinel.models.project import ProjectSettings
from sentinel.utils.settings import apply_extra_settings, load_settings


class SentinelProject:
    def parse(self, path: pathlib.Path, settings: Dict = dict()) -> ProjectSettings:
        project_data = apply_extra_settings(path=path, settings=settings.copy())
        project_settings = load_settings(content=project_data)
        return ProjectSettings(**project_settings)
