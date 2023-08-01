import os
from pathlib import Path
from difflib import SequenceMatcher
import shutil
from util.OsManager import OsManager


class ScalettaManager:

    def __init__(self, scaletta_latex: list):
        self.scaletta_latex = scaletta_latex

        self.song_source_list = self.__prepare_song_source_list__()

    @staticmethod
    def __prepare_song_source_list__():
        song_source_list = []
        for song in Path(OsManager.get_song_dir()).iterdir():
            song_source_list.append(song)
        return song_source_list

    @staticmethod
    def __next_cont__(cont: str):
        if int(cont) < 9:
            return "0"+str(int(cont)+1)
        else:
            return str(int(cont)+1)

    @staticmethod
    def __delete_dest_folder():
        res_dir = OsManager.get_result_dir()
        if Path(res_dir).exists():
            shutil.rmtree(res_dir)
        os.makedirs(res_dir)

    def __find_most_similar__(self, song: str):
        similar_ratio = 0.0
        similar = ''
        for file in self.song_source_list:
            file_to_compare = str(file).lower().replace(OsManager.get_song_dir(), '')
            song_to_compare = str(song[3:]).lower()
            this_ratio = SequenceMatcher(None, file_to_compare, song_to_compare).ratio()
            if this_ratio > similar_ratio:
                similar_ratio = this_ratio
                similar = file
        if similar_ratio > 0.7:
            return similar
        else:
            return "None"

    def make_scaletta(self, with_instrumental: bool):
        cont = "00"
        self.__delete_dest_folder()
        for song in self.scaletta_latex:
            cont = ScalettaManager.__next_cont__(cont)
            chosen_file = self.__find_most_similar__(song)
            if not chosen_file == "None":
                destination = OsManager.get_result_dir()+cont+" - "+str(chosen_file).replace(OsManager.get_song_dir(), '')
                shutil.copytree(chosen_file, destination)

        # Se vanno messe anche le strumentali, eseguiamo anche questa parte
        if with_instrumental:
            for file in (x for x in self.song_source_list if str(x).startswith(OsManager.get_song_dir()+"00")):
                shutil.copytree(file, str(file).replace(OsManager.get_song_dir(), OsManager.get_result_dir()))
