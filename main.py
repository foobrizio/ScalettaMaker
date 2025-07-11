# importing required modules
import sys

from util import utils
from pathlib import Path

from util.MyPdfReader import MyPdfReader
from util.ScalettaManager import ScalettaManager


def choose_file():

    list_of_files = [x for x in Path(utils.get_data_directory()).iterdir() if x.is_file() and x.suffix.__eq__('.pdf')]
    if len(list_of_files) == 0:
        data_dir = utils.get_data_directory()
        raise Exception(f"Nessun file .pdf trovato nella cartella '{data_dir}'. Inserire un file da usare come scaletta")
    elif len(list_of_files) == 1:
        return list_of_files[0]
    else:
        while True:
            print("Scegli il file da usare da questa lista:")
            cont = 1
            for file in list_of_files:
                print(str(cont)+") "+str(file))
                cont += 1
            choice = input("File number: ")
            if choice.isnumeric() and 0 < int(choice) <= len(list_of_files):
                return list_of_files[int(choice)-1]
            print()

def choose_guitarist() -> str:
    choice = input("Qual è il chitarrista di questa serata? -> ")
    if utils.is_similar(choice, utils.get_fabrizio()):
        guitarist = utils.get_fabrizio()
    elif utils.is_similar(choice, utils.get_sergio()):
        guitarist = utils.get_sergio()
    else:
        raise Exception(f"Il chitarrista {choice} non è stato riconosciuto. Impossibile continuare")
    return guitarist


def song_check():
    list_of_files = [x for x in Path(utils.get_song_directory()).iterdir() if x.is_dir()]
    return len(list_of_files) > 0


if __name__ == '__main__':
    try:
        if not song_check():
            directory = utils.get_song_directory()
            raise Exception(f"Non sono state trovate canzoni nella cartella '{directory}'. Scaricare le nuove canzoni da Proton Drive.")
        else:
            pdfFile = choose_file()
            if pdfFile is not None:
                guitarist = choose_guitarist()
                song_list = MyPdfReader(pdfFile).convert_file_to_song_list()
                ScalettaManager(song_list, guitarist).make_scaletta(True)
    except Exception as err:
        print(str(err))
    input("Premere Invio per terminare ")
    sys.exit(0)


