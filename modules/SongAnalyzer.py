from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

import librosa
import numpy as np
import os

@dataclass
class Song:
    song_track: str
    song_folder: str
    click_track: str
    title: str

    def __init__(self, song_track: str, song_folder: str, click_track: str, title: str):
        self.song_track = song_track
        self.song_folder = song_folder
        self.click_track = click_track
        self.title = title

    def song_path(self)-> str:
        return f'{self.song_folder}/{self.song_track}'

    def click_path(self)-> str:
        return f'{self.song_folder}/{self.click_track}'

class AnalysisResult:
    title: str
    key: str
    tempo: Optional[str]

    def __init__(self, title: str, key: str, tempo: str = None):
        self.title = title
        self.key = key
        self.tempo = tempo


class SongAnalyzer:

    song_list: list[Song]
    result: list[AnalysisResult]

    def __init__(self, song_folder: str):
        song_folder = song_folder[:-1]
        self.song_list = self.__find_songs__(song_folder)
        self.result = []

    @staticmethod
    def __find_songs__(songs_folder: str) -> list[Song]:
        song_dirs = os.listdir(songs_folder)
        result = []

        for song_dir in song_dirs:
            song_folder =f'{songs_folder}/{song_dir}'
            files = os.listdir(song_folder)
            song_track = next(filter(lambda x: '01' in x, files))
            click_track = next(filter(lambda x: '03' in x, files))
            title = song_dir
            result.append(Song(song_track=song_track,
                               click_track=click_track,
                               song_folder=song_folder,
                               title=title))
        return result

    def start_analysis(self):
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.estimate_key, self.song_list))
            self.result = results

    def estimate_key(self, song: Song) -> AnalysisResult:
        print(f"Analisi {song.title} in corso...")
        audio_path = song.song_path()
        y, sr = librosa.load(audio_path, sr=22050, mono=True, duration=60.0)

        # Estrae cromagramma (intensità delle 12 note in ogni istante)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Media sull'intero brano
        chroma_mean = np.mean(chroma, axis=1)

        # Tonalità candidate (12 maggiori + 12 minori)
        major_keys = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
        minor_keys = [k + ' minore' for k in major_keys]

        # Profilo teorico per tonalità maggiori e minori
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                                  2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                                  2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        # Trova la trasposizione che meglio si adatta al profilo
        def get_correlation(profile):
            return [np.corrcoef(np.roll(profile, i), chroma_mean)[0, 1] for i in range(12)]

        major_corr = get_correlation(major_profile)
        minor_corr = get_correlation(minor_profile)
        best_major = np.argmax(major_corr)
        best_minor = np.argmax(minor_corr)

        print(f"Analisi {song.title} terminata.")
        if major_corr[best_major] > minor_corr[best_minor]:
            return AnalysisResult(title=song.title,
                                  key=major_keys[best_major])
        else:
            return AnalysisResult(title=song.title,
                                  key=minor_keys[best_minor])

    def print_result(self):
        print("Risultato analisi:")
        for song in self.result:
            print(f'{song.title} -> Chiave: {song.key}')