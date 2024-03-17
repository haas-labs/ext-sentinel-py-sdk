import json
import yaml

import pathlib
import logging

from typing import List, Dict


logger = logging.getLogger(__name__)


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
