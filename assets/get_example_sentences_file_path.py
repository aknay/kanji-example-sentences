import os
from pathlib import Path

dirPath = os.path.dirname(os.path.realpath(__file__))


def get_example_sentence_file_path() -> Path:
    return Path(f'{dirPath}/kanji_example_sentences.yml')

def get_n5_part_file_path() -> Path:
    return Path(f'{dirPath}/split_jlpt_files/N5.yaml')
