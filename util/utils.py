import json
from difflib import SequenceMatcher

def __read_json_file__(file_path: str):
    try:
        with open(file_path) as f:
            result = json.load(f)
            return result
    except Exception as e:
        raise Exception(f"Il file {file_path} è malformato")

def get_constants(property_name: str):
    consts = __read_json_file__("conf/consts.json")
    property = consts.get(property_name)
    if property is None:
        raise Exception(f"property '{property_name}' non inizializzata")
    return property

def get_rules():
    return __read_json_file__('conf/specialRules.json')

def is_similar(string1: str, string2: str) -> bool:
    string1 = string1.lower()
    string2 = string2.lower()
    similar_ratio = SequenceMatcher(None, string1, string2).ratio()
    return similar_ratio > 0.7

    


def get_fabrizio() -> str:
    return get_constants("fabrizioGuitarist")

def get_sergio() -> str:
    return get_constants("sergioGuitarist")

def get_similarity() -> float:
    return get_constants("similarity")


