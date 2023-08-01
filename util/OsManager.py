import os


class Consts:
    # Windows folders
    __WIN_SONG_DIR__ = 'data\\songs\\'
    __WIN_RESULT_DIR__ = 'result\\'
    __WIN_DATA_DIR__ = 'data\\'

    # Linux folders
    __LX_SONG_DIR__ = 'data/songs/'
    __LX_RESULT_DIR__ = 'result/'
    __LX_DATA_DIR__ = 'data/'


class OsManager:

    @staticmethod
    def get_song_dir():
        if os.name == 'nt':
            return Consts.__WIN_SONG_DIR__
        elif os.name == 'posix':
            return Consts.__LX_SONG_DIR__
        else:
            raise Exception(os.name+' OS is not currently supported')

    @staticmethod
    def get_result_dir():
        if os.name == 'nt':
            return Consts.__WIN_RESULT_DIR__
        elif os.name == 'posix':
            return Consts.__LX_RESULT_DIR__
        else:
            raise Exception(os.name + ' OS is not currently supported')

    @staticmethod
    def get_data_dir():
        if os.name == 'nt':
            return Consts.__WIN_DATA_DIR__
        elif os.name == 'posix':
            return Consts.__LX_DATA_DIR__
        else:
            raise Exception(os.name+' OS is not currently supported')

