import PyPDF2
import re


class MyPdfReader:

    def __init__(self, file):
        self.file = file

    def convert_file_to_song_list(self):
        pdf_reader = PyPDF2.PdfReader(self.file)
        song_list = []
        for page in pdf_reader.pages:
            lines = page.extract_text().split("\n")
            lines = list(filter(lambda line:  re.search("\d\d?[.] [a-zA-Z ]*",line) ,lines))
            song_list = song_list + lines
        return song_list
