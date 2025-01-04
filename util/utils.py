import json
import os
from difflib import SequenceMatcher


def get_constants():
    with open('util/consts.json') as f:
        return json.load(f)

def get_rules():
    with open('util/specialRules.json') as spf:
        return json.load(spf)

def is_similar(string1: str, string2: str) -> bool:
    string1 = string1.lower()
    string2 = string2.lower()
    similar_ratio = SequenceMatcher(None, string1, string2).ratio()
    return similar_ratio > 0.7

def extract_song_title(file) -> str:
    if os.name == 'nt':
        parts: [str] = str(file).split("\\")
    elif os.name == 'posix':
        parts: [str] = str(file).split("/")
    return parts[-1]

    
def get_song_directory():
    if os.name == 'nt':
        return get_constants().get("winSongDir")
    elif os.name == 'posix':
        return get_constants().get("linuxSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def get_generic_song_directory():
    base = get_song_directory()
    if os.name == 'nt':
        return base + "\\"+get_constants().get("genericSongDir")
    elif os.name == 'posix':
        return base + "/"+get_constants().get("genericSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def get_guitarist_song_directory(guitarist: str):
    base = get_song_directory()
    if guitarist == get_constants().get("fabrizioGuitarist"):
        guitar_folder = get_constants().get("fabrizioSongDir")
    else:
        guitar_folder = get_constants().get("sergioSongDir")
    if os.name == 'nt':
        return base + "\\" + guitar_folder
    elif os.name == 'posix':
        return base + "/" + guitar_folder
    else:
        raise Exception(os.name + ' OS is not currently supported')

def get_result_directory():
    if os.name == 'nt':
        return get_constants().get("winResultDir")
    elif os.name == 'posix':
        return get_constants().get("linuxResultDier")
    else:
        raise Exception(os.name + ' OS is not currently supported')

def get_data_directory():
    if os.name == 'nt':
        return get_constants().get("winDataDir")
    elif os.name == 'posix':
        return get_constants().get("linuxDataDir")
    else:
        raise Exception(os.name+' OS is not currently supported')
