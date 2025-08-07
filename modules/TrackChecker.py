import os
from pathlib import Path
from typing import Optional

from util import utils


def __load_from_result__():
    result_songs = []
    for directory in filter(lambda x: Path.is_dir(x), Path(utils.get_result_directory()).iterdir()):
        result_songs.append(directory)
    return result_songs



class TrackChecker:


    def __init__(self):
        self.song_list = __load_from_result__()

    def start_check(self):
        print("Analisi tracce iniziata")
        # D:\Musica\Canzoni Sweet Life\Basi\-- Generiche --\Le Freak
        warn_list: list[str] = []
        for song in self.song_list:
            name_result: Optional[str] = self.__check_name__(song)
            length_result: Optional[str] = self.__check_same_length__(song)
            if name_result:
                warn_list.append(name_result)
            if length_result:
                warn_list.append(length_result)
        print("Analisi terminata")
        if len(warn_list) == 0:
            print("Nessuna problematica riscontrata")
        else:
            print("Sono stati trovati i seguenti problemi:")
            for index,warn in enumerate(warn_list):
                print(f"{index}): {warn}")

    @staticmethod
    def __check_name__(song) -> Optional[str]:
        files = os.listdir(song)
        missing_numbers: list[str] = []
        file_01 = list(filter(lambda filename: filename.__contains__("1"), files))
        file_02 = list(filter(lambda filename: filename.__contains__("2"), files))
        file_03 = list(filter(lambda filename: filename.__contains__("3"), files))
        if len(file_01) == 0 or len(file_01) > 1:
            missing_numbers.append("01")
        if len(file_02) == 0 or len(file_03) > 1:
            missing_numbers.append("02")
        if len(file_03) == 0 or len(file_03) > 1:
            missing_numbers.append("03")

        if len(missing_numbers) > 0:
            title = song.name
            return f"Warning su canzone {title}. Mancano le tracce con i seguenti numeri: {missing_numbers}"
        return None


    @staticmethod
    def __check_same_length__(song) -> Optional[str]:
        files = list(filter(lambda x:x.__contains__('wav'), os.listdir(song)))
        file_path = os.path.join(song, files[0])
        previous_size = os.path.getsize(file_path)
        for file in files:
            file_path = os.path.join(song, file)
            current_size = os.path.getsize(file_path)
            if current_size != previous_size:
                title = song.name
                return f"Warning su canzone {title}. I file hanno dimensioni diverse"
        return None
