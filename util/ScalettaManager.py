import os
from pathlib import Path
from difflib import SequenceMatcher
import shutil

from util import utils


class ScalettaManager:

    def __init__(self, scaletta_latex: list, guitarist: str):
        self.scaletta_latex = scaletta_latex
        self.guitarist = guitarist
        self.__prepare_song_source_list__()
        self.skipped_songs = []

    """Creates an array of song titles, based on the available directories in the songs folder"""
    def __prepare_song_source_list__(self) -> [str]:
        generic_songs = ScalettaManager.__load_generic_in_source_list__()
        guitarist_songs = ScalettaManager.__load_specifics_in_source_list__(self.guitarist)
        self.song_source_list = generic_songs + guitarist_songs

    @staticmethod
    def __load_generic_in_source_list__() -> [str]:
        generic_path = Path(utils.get_generic_song_directory())
        generic_songs = []
        for directory in filter(lambda x: Path.is_dir(x), Path(generic_path).iterdir()):
            generic_songs.append(directory)
        return generic_songs

    @staticmethod
    def __load_specifics_in_source_list__(guitarist: str) -> [str]:
        guitarist_path = Path(utils.get_guitarist_song_directory(guitarist))
        guitarist_songs = []
        for directory in filter(lambda x: Path.is_dir(x), Path(guitarist_path).iterdir()):
            guitarist_songs.append(directory)
        return guitarist_songs

    @staticmethod
    def __next_cont__(cont: str):
        if int(cont) < 9:
            return "0"+str(int(cont)+1)
        else:
            return str(int(cont)+1)

    @staticmethod
    def __delete_dest_folder():
        res_dir = utils.get_result_directory()
        if Path(res_dir).exists():
            shutil.rmtree(res_dir)
        os.makedirs(res_dir)

    @staticmethod
    def get_alternative_titles_if_existing(song: str) -> (bool, [str]):
        rules = utils.get_rules()
        for ruleset in rules:
            for rule in rules[ruleset]:
                if utils.is_similar(rule, song):
                    return True, rules[ruleset]
        return False, []


    def __find_most_similar__(self, song: str) -> str:
        similar_ratio = 0.0
        similar = ''
        for file in self.song_source_list:
            song_title = utils.extract_song_title(file).lower()
            #song_to_compare = str(song[3:]).lower()
            song = song.lower()
            this_ratio = SequenceMatcher(None, song_title, song).ratio()
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
            song_title = song.split(".")[1].strip()
            cont = ScalettaManager.__next_cont__(cont)
            print(f"Canzone {cont}/{len(self.scaletta_latex)}...", end='')
            has_alternative_titles, alt_titles = ScalettaManager.get_alternative_titles_if_existing(song_title)
            all_titles = [song_title]
            if has_alternative_titles:
                all_titles = alt_titles
            copied = False
            for title in all_titles:
                chosen_file = self.__find_most_similar__(title)
                if not chosen_file == "None":
                    destination = utils.get_result_directory()+cont+" - "+utils.extract_song_title(str(chosen_file))
                    shutil.copytree(chosen_file, destination)
                    copied = True
                    break
            if copied:
                print("Copiato!!!")
            else:
                self.skipped_songs.append(song)
                print("Non trovato!!!")
        print(f"Processo terminato. Le seguenti {len(self.skipped_songs)} canzoni non sono state trovate:")
        print(self.skipped_songs)

        # Se vanno messe anche le strumentali, eseguiamo anche questa parte
        # if with_instrumental:
        #    for file in (x for x in self.song_source_list if str(x).startswith(OsManager.get_song_dir()+"00")):
        #        shutil.copytree(file, str(file).replace(OsManager.get_song_dir(), OsManager.get_result_dir()))
