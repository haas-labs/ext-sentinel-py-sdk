import pathlib

from typing import Dict

from sentinel.models.project import ProjectSettings
from sentinel.utils.settings import load_project_settings


class SentinelProject:
    def parse(self, path: pathlib.Path, extra_vars: Dict = dict()) -> ProjectSettings:
        return load_project_settings(path=path, extra_vars=extra_vars)
