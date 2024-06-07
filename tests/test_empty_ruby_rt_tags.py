from pathlib import Path

import pytest

from assets.get_example_sentences_file_path import getExampleSentenceFilePath
from utils.utils import has_empty_ruby_rt_tag


@pytest.fixture
def example_sentences_file_path() -> Path:
    return getExampleSentenceFilePath()


def test_empty_ruby_tag(example_sentences_file_path):
    results = has_empty_ruby_rt_tag(path=example_sentences_file_path)
    assert len(results) == 0
