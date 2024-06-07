from pathlib import Path

import pytest

from assets.get_example_sentences_file_path import getExampleSentenceFilePath
from check_empty_ruby_tags import check_empty_ruby_tag

@pytest.fixture
def example_sentences_file_path() -> Path:
    return getExampleSentenceFilePath()

def test_empty_ruby_tag(example_sentences_file_path):
    results = check_empty_ruby_tag(path=example_sentences_file_path)
    assert len(results) == 0
