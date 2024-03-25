import os
import re
import json
import yaml
import jinja2
import logging
import pathlib

from typing import Dict, List

from jinja2.ext import Extension as JinjaExtension

from sentinel.models.project import ProjectSettings


logger = logging.getLogger(__name__)


class IncorrectFileFormat(Exception): ...


class IncorrectSettingsFormat(Exception): ...


class YAMLCleaner(JinjaExtension):
    def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
        # Regular expression to match YAML comments
        pattern = r"^\s*#.*$"
        # Remove comments
        source = re.sub(pattern, "", source, flags=re.MULTILINE)
        return source


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


def load_settings(content: str) -> Dict:
    """
    Load settings from YAML file
    """
    settings = {}
    try:
        settings = yaml.load(content, Loader=yaml.FullLoader)
    except yaml.YAMLError as err:
        raise IncorrectSettingsFormat("Incorrect Settings format: {}".format(err))
    return settings if settings is not None else {}


def load_env_vars(self, env_name: str = None):
    """
    Load environment vairables from SENTINEL_ENV. If not specified returns "local"
    """
    if env_name is None:
        env_name = os.environ.get("SENTINEL_ENV") or "local"

def load_project_settings(path: pathlib.Path, env: str = "local", extra_vars: Dict = dict()) -> ProjectSettings:
    """
    Load project settings from a path
    """
    if not path.exists():
        raise IOError(f"The path does not exist, {path}")
    config_dir = path.parent
    settings_content = apply_extra_settings(path=path, settings=extra_vars)

    logger.info(f"Loading settings from {path}")
    settings = load_settings(settings_content)

    for config in settings.get("imports", []):
        config_path = config_dir / pathlib.Path(config)
        if not config_path.exists():
            raise IOError(f"The import path does not exist, {config_path}")
        config_content = apply_extra_settings(config_path, settings=extra_vars)
        logger.info(f"Importing settings from {config_path}")
        settings.update(load_settings(config_content))
    return ProjectSettings(**settings)


def apply_extra_settings(path: pathlib.Path, settings: Dict) -> str:
    """
    Apply extra settings to the main ones
    """
    try:
        template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path.parent),
            undefined=jinja2.StrictUndefined,
            extensions=["sentinel.utils.settings.YAMLCleaner"],
        ).get_template(path.name)
        output = template.render(**settings, env=os.environ.copy())
    except jinja2.exceptions.TemplateNotFound as err:
        raise IOError(f"The path not found, {path}, error: {err}")
    except jinja2.exceptions.UndefinedError as err:
        raise IncorrectFileFormat(f"File format error in {path}, error: {err}")
    return output
