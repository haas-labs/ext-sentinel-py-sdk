import logging
import pathlib

from typing import Dict, List

from pydantic import BaseModel

from sentinel.models.process import Process
from sentinel.utils.settings import load_settings, apply_extra_settings

logger = logging.getLogger(__name__)


class Profile(BaseModel):
    """
    Launcher Profile
    """

    processes: List[Process]


class LauncherProfile:
    """
    Launcher Profile
    """

    def parse(self, path: pathlib.Path, settings: Dict = dict()) -> Profile:
        """
        Parse profile
        """
        profile_data = apply_extra_settings(path=path, settings=settings.copy())
        profile = load_settings(content=profile_data)
        return Profile(processes=profile)
