# importing required modules
from util.Consts import Consts
from pathlib import Path

from util.MyPdfReader import MyPdfReader
from util.ScalettaManager import ScalettaManager


def choose_file():

    list_of_files = [x for x in Path(Consts.get_data_dir()).iterdir() if x.is_file() and x.suffix.__eq__('.pdf')]
    if len(list_of_files) == 0:
        print("Nessun file .pdf trovato nella cartella 'data'")
        exit(0)
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


def song_check():
    list_of_files = [x for x in Path(Consts.get_song_dir()).iterdir() if x.is_dir()]
    return len(list_of_files) > 0


if __name__ == '__main__':

    if not song_check():
        print("Non sono state trovate canzoni nella cartella 'data/songs'")
        exit(0)
    pdfFile = choose_file()

    song_list = MyPdfReader(pdfFile).convert_file_to_song_list()
    ScalettaManager(song_list).make_scaletta(True)


