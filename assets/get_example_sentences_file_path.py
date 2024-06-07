import os
from pathlib import Path

dirPath = os.path.dirname(os.path.realpath(__file__))


def getExampleSentenceFilePath() -> Path:
    return Path(f'{dirPath}/kanji_example_sentences.yml')
