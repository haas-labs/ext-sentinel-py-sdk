from typing import Dict, List

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
