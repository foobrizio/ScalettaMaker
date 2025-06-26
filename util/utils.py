import json
import os
from difflib import SequenceMatcher

def __read_json_file__(file_path: str):
    try:
        with open(file_path) as f:
            result = json.load(f)
            return result
    except Exception as e:
        raise Exception(f"Il file {file_path} è malformato")

def __get_constants__(property_name: str):
    consts = __read_json_file__("util/consts.json")
    property = consts.get(property_name)
    if property is None:
        raise Exception(f"property '{property_name}' non inizializzata")
    return property

def get_rules():
    return __read_json_file__('util/specialRules.json')

def is_similar(string1: str, string2: str) -> bool:
    string1 = string1.lower()
    string2 = string2.lower()
    similar_ratio = SequenceMatcher(None, string1, string2).ratio()
    return similar_ratio > 0.7

def extract_song_title(file) -> str:
    if is_windows():
        parts: [str] = str(file).split("\\")
    elif is_linux():
        parts: [str] = str(file).split("/")
    return parts[-1]

    
def get_song_directory():
    if is_windows():
        return __get_constants__("winSongDir")
    elif is_linux():
        return __get_constants__("linuxSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def get_generic_song_directory():
    base = get_song_directory()
    if is_windows():
        return base + "\\"+__get_constants__("genericSongDir")
    elif is_linux():
        return base + "/"+__get_constants__("genericSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def is_windows() -> bool:
    return os.name == 'nt'

def is_linux() -> bool:
    return os.name == 'posiz'

def get_guitarist_song_directory(guitarist: str):
    base = get_song_directory()
    if guitarist == __get_constants__("fabrizioGuitarist"):
        guitar_folder = __get_constants__("fabrizioSongDir")
    else:
        guitar_folder = __get_constants__("sergioSongDir")
    if os.name == 'nt':
        return base + "\\" + guitar_folder
    elif os.name == 'posix':
        return base + "/" + guitar_folder
    else:
        raise Exception(os.name + ' OS is not currently supported')

def get_fabrizio() -> str:
    return __get_constants__("fabrizioGuitarist")

def get_sergio() -> str:
    return __get_constants__("sergioGuitarist")

def get_similarity() -> float:
    return __get_constants__("similarity")

def get_result_directory():
    if is_windows():
        return __get_constants__("winResultDir")
    elif is_linux():
        return __get_constants__("linuxResultDir")
    else:
        raise Exception(os.name + ' OS is not currently supported')

def get_data_directory():
    if is_windows():
        return __get_constants__("winDataDir")
    elif is_linux():
        return __get_constants__("linuxDataDir")
    else:
        raise Exception(os.name+' OS is not currently supported')
