
import os
import json
import yaml
import jinja2
import logging
import pathlib

from pydantic import BaseModel
from typing import Dict, List, Union, Optional

from sentinel.models.process import Process


logger = logging.getLogger(__name__)


class IncorrectProfileFormat(Exception):
    pass

class ProfileNotFound(Exception):
    pass


class Profile(BaseModel):
    '''
    Launcher Profile
    '''
    processes: List[Process]


def load_extra_vars(extra_vars: List[str] = list()) -> Dict:
    ''' reused from https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/vars.py
        and modified according to sentinel requirements 
    ''' 
    extra_vars_result = {}

    if not extra_vars:
        return extra_vars_result

    if not isinstance(extra_vars, List):
        raise RuntimeError('Incorrect extra vars type, ' \
                           + f'found: {type(extra_vars)} ' \
                           + 'expected: List[str]')

    for vars in extra_vars:
        data = None
        if vars.startswith("@"):
            vars_path = pathlib.Path(vars[1:])
            # Argument is a YAML file (JSON is a subset of YAML)
            try:
                with vars_path.open('r', encoding='utf-8') as source:
                    try:
                        data = yaml.load(source, Loader=yaml.FullLoader)
                    except yaml.YAMLError as err:
                        logger.error('{}, {}'.format(err, vars))
            except FileNotFoundError as err:
                logger.error(err)
        else:
            try:
                data = json.loads(vars)
            except json.JSONDecodeError as err:
                logger.error('{}, {}'.format(err, vars))
        
        if data and isinstance(data, dict):
            extra_vars_result.update(data)

    return extra_vars_result


class LauncherProfile:
    '''
    Launcher Profile
    '''
    def __init__(self) -> None:
        '''
        Detector Profile Init
        '''
        self._processes = list()

    def parse(self, profile_path: pathlib.Path,
                    extra_vars: Dict = dict()) -> Profile:
        '''
        Parse profile
        '''
        profile_data = self.apply_extra_vars(profile_path=profile_path,
                                             extra_vars=extra_vars.copy())
        profile = self.load_profile(profile_data)
        return Profile(processes=profile)

    def load_profile(self, content: str) -> Profile:
        '''
        Load profile from YAML file
        '''
        profile = {}
        try:
            profile = yaml.load(content, Loader=yaml.FullLoader)
        except  yaml.YAMLError as err:
            raise IncorrectProfileFormat('Incorrect Profile format: {}'.format(err))
        return profile

    def apply_extra_vars(self, 
                         profile_path: pathlib.Path, 
                         extra_vars: Dict) -> str:
        ''' 
        Apply extra vars to topology file
        '''
        try:
            template = jinja2.Environment(
                            loader=jinja2.FileSystemLoader(profile_path.parent),
                            undefined=jinja2.StrictUndefined
                        ).get_template(profile_path.name)
        
            output = template.render(**extra_vars, 
                                     env=os.environ.copy())
        except jinja2.exceptions.TemplateNotFound as err:
            raise ProfileNotFound(f'Profile or bundle not found, {err}')
        except jinja2.exceptions.UndefinedError as err:
            raise IncorrectProfileFormat(f'Profile template error, {err}')

        return output
