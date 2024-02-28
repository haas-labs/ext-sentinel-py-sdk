import pathlib

from typing import Any, Dict, List, Tuple


def get_sentinel_version():
    """
    returns sentinel version
    """
    return pathlib.Path(__file__).parent.joinpath("VERSION").read_text()


def import_by_classpath(classpath: str) -> Tuple[str, Any]:
    """
    import by classpath
    """
    module_name, class_name = classpath.rsplit(".", 1)

    module = __import__(
        module_name,
        globals(),
        locals(),
        [
            class_name,
        ],
        0,
    )
    _class = getattr(module, class_name)

    return module_name, _class


def dict_fields_mapping(data: Dict, mappings: Dict) -> Dict:
    """
    Dictionary fields mapping, working with 1st level keys only
    """
    result = dict()
    mapping_keys = mappings.keys()
    for k, v in data.items():
        if k not in mapping_keys:
            result[k] = v
        else:
            result[mappings[k]] = v
    return result


def dict_fields_filter(data: Dict, ignore_list: List[str]) -> Dict:
    """
    Dictionary fields filter
    """
    result = dict()
    for k, v in data.items():
        if k in ignore_list:
            continue
        result[k] = v
    return result


def dict_fields_transform(data: Dict, transformers: Dict) -> Dict:
    """
    Dictionary fields transform
    """
    for k, v in data.items():
        if k in transformers:
            data[k] = transformers[k](v)
    return data


def dicts_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge dictionaries
    """
    result = dict()
    result.update(dict1)
    result.update(dict2)
    return result
