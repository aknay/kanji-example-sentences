import os
from pathlib import Path

dirPath = os.path.dirname(os.path.realpath(__file__))


def get_kanji_dic_json_file() -> Path:
    return Path(f'{dirPath}/kanjidic.json')

def get_kanji_dic_yaml_saving_file() -> Path:
    return Path(f'{dirPath}/kanjidic.yaml')

def get_kanji_dic_generated_json_saving_file() -> Path:
    return Path(f'{dirPath}/kanjidic-generated.json')