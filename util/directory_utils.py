import os

from util.utils import get_constants


def get_song_directory():
    if is_windows():
        return get_constants("winSongDir")
    elif is_linux():
        return get_constants("linuxSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def extract_song_title(file) -> str:
    if is_windows():
        parts: [str] = str(file).split("\\")
    elif is_linux():
        parts: [str] = str(file).split("/")
    return parts[-1]

def get_generic_song_directory():
    base = get_song_directory()
    if is_windows():
        return base + "\\"+get_constants("genericSongDir")
    elif is_linux():
        return base + "/"+get_constants("genericSongDir")
    else:
        raise Exception(os.name+' OS is not currently supported')

def is_windows() -> bool:
    return os.name == 'nt'

def is_linux() -> bool:
    return os.name == 'posiz'

def get_guitarist_song_directory(guitarist: str):
    base = get_song_directory()
    if guitarist == get_constants("fabrizioGuitarist"):
        guitar_folder = get_constants("fabrizioSongDir")
    else:
        guitar_folder = get_constants("sergioSongDir")
    if os.name == 'nt':
        return base + "\\" + guitar_folder
    elif os.name == 'posix':
        return base + "/" + guitar_folder
    else:
        raise Exception(os.name + ' OS is not currently supported')
    
def get_result_directory():
    if is_windows():
        return get_constants("winResultDir")
    elif is_linux():
        return get_constants("linuxResultDir")
    else:
        raise Exception(os.name + ' OS is not currently supported')

def get_data_directory():
    if is_windows():
        return get_constants("winDataDir")
    elif is_linux():
        return get_constants("linuxDataDir")
    else:
        raise Exception(os.name+' OS is not currently supported')