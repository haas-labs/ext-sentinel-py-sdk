import pathlib

from typing import Dict

from sentinel.models.project import ProjectSettings
from sentinel.utils.settings import load_project_settings


class SentinelProject:
    def parse(self, path: pathlib.Path, extra_vars: Dict = dict()) -> ProjectSettings:
        settings = load_project_settings(pathlib.Path().cwd() / "sentinel.yaml")
        profile_settings = load_project_settings(path=path, extra_vars=extra_vars)
        settings.imports.extend(profile_settings.imports)
        settings.sentries.extend(profile_settings.sentries)
        settings.inputs.extend(profile_settings.inputs)
        settings.outputs.extend(profile_settings.outputs)
        settings.databases.extend(profile_settings.databases)
        return settings
