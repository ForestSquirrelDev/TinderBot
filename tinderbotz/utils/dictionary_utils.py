from typing import Dict, Any, List


def try_get_string(dictionary: Dict[str, Any], key: str, default_value: str = "") -> str:
    if key not in dictionary:
        return default_value
    return str(dictionary[key])

def try_get_node(dictionary: Dict[str, Any], key: str) -> Dict[str, Any]:
    if key not in dictionary:
        return dict()
    return dictionary[key]

def try_get_bool(dictionary: Dict[str, Any], key: str, default_value: bool = False) -> bool:
    if key not in dictionary:
        return default_value
    return bool(dictionary[key])

def try_get_list(dictionary: Dict[str, Any], key: str) -> List[Any]:
    if key not in dictionary:
        return list()
    return list(dictionary[key])

def try_get_float(dictionary: Dict[str, Any], key: str, default_value: float = 0) -> float:
    if key not in dictionary:
        return default_value
    return float(dictionary[key])
