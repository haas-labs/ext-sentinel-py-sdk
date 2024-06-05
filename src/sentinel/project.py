import pathlib
from typing import Dict

from sentinel.models.settings import Settings
from sentinel.utils.settings import load_settings


class SentinelProject:
    def parse(self, path: pathlib.Path, extra_vars: Dict = dict()) -> Settings:
        try:
            settings = load_settings(pathlib.Path().cwd() / "sentinel.yaml")
        except OSError:
            settings = Settings()
        profile_settings = load_settings(path=path, extra_vars=extra_vars)

        # Overwrite main project section (from sentinel.yaml) if project section specified in a profile
        if profile_settings.project is not None:
            settings.project = profile_settings.project

        settings.imports.extend(profile_settings.imports)
        settings.sentries.extend(profile_settings.sentries)
        settings.inputs.extend(profile_settings.inputs)
        settings.outputs.extend(profile_settings.outputs)
        settings.databases.extend(profile_settings.databases)
        settings.enrich_sentries()
        return settings
