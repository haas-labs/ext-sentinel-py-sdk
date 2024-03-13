import os
import re
import json
import yaml
import jinja2
import logging
import pathlib

from typing import Dict, List

from pydantic import BaseModel

from jinja2.ext import Extension as JinjaExtension

from sentinel.models.process import Process


logger = logging.getLogger(__name__)


class IncorrectProfileFormat(Exception):
    pass


class ProfileNotFound(Exception):
    pass


class Profile(BaseModel):
    """
    Launcher Profile
    """

    processes: List[Process]


def load_extra_vars(extra_vars: List[str] = list()) -> Dict:
    """reused from https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/vars.py
    and modified according to sentinel requirements
    """
    extra_vars_result = {}

    if not extra_vars:
        return extra_vars_result

    if not isinstance(extra_vars, List):
        raise RuntimeError("Incorrect extra vars type, " + f"found: {type(extra_vars)} " + "expected: List[str]")

    for vars in extra_vars:
        data = None
        if vars.startswith("@"):
            vars_path = pathlib.Path(vars[1:])
            # Argument is a YAML file (JSON is a subset of YAML)
            try:
                with vars_path.open("r", encoding="utf-8") as source:
                    try:
                        data = yaml.load(source, Loader=yaml.FullLoader)
                    except yaml.YAMLError as err:
                        logger.error("{}, {}".format(err, vars))
            except FileNotFoundError as err:
                logger.error(err)
        else:
            try:
                data = json.loads(vars)
            except json.JSONDecodeError as err:
                logger.error("{}, {}".format(err, vars))

        if data and isinstance(data, dict):
            extra_vars_result.update(data)

    return extra_vars_result


class YAMLCleaner(JinjaExtension):
    def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
        # Regular expression to match YAML comments
        pattern = r"^\s*#.*$"
        # Remove comments
        source = re.sub(pattern, "", source, flags=re.MULTILINE)
        return source



class LauncherProfile:
    """
    Launcher Profile
    """

    def parse(self, profile_path: pathlib.Path, extra_vars: Dict = dict()) -> Profile:
        """
        Parse profile
        """
        profile_data = self.apply_extra_vars(profile_path=profile_path, extra_vars=extra_vars.copy())
        profile = self.load_profile(profile_data)
        return Profile(processes=profile)

    def load_profile(self, content: str) -> Profile:
        """
        Load profile from YAML file
        """
        profile = {}
        try:
            profile = yaml.load(content, Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            raise IncorrectProfileFormat("Incorrect Profile format: {}".format(err))
        return profile

    def apply_extra_vars(self, profile_path: pathlib.Path, extra_vars: Dict) -> str:
        """
        Apply extra vars to topology file
        """
        logger.info(f"Loading profile template from {profile_path}")
        try:
            template_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(profile_path.parent),
                undefined=jinja2.StrictUndefined,
                extensions=['sentinel.profile.YAMLCleaner']
            )
            template = template_env.get_template(profile_path.name)
            output = template.render(**extra_vars, env=os.environ.copy())
        except jinja2.exceptions.TemplateNotFound as err:
            raise ProfileNotFound(f"Profile or bundle not found, {err}")
        except jinja2.exceptions.UndefinedError as err:
            raise IncorrectProfileFormat(f"Profile template error, {err}")

        return output
