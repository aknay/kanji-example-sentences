from pathlib import Path

import pytest
import yaml

from assets.get_example_sentences_file_path import getExampleSentenceFilePath
from is_ruby_formated_correctly import is_valid_ruby
from utils.utils import has_empty_ruby_rt_tag


@pytest.fixture
def example_sentences_file_path() -> Path:
    return getExampleSentenceFilePath()


def test_empty_ruby_tag(example_sentences_file_path):
    results = has_empty_ruby_rt_tag(path=example_sentences_file_path)
    assert len(results) == 0


def test_ruby_tag_is_correctly_formatted(example_sentences_file_path):
    with open(example_sentences_file_path) as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v and v['samples'] is not None:
                for key, sample in v["samples"].items():
                    if sample is not None:
                        assert "ruby" in sample
                        assert is_valid_ruby(sample['ruby']), print(sample['ruby'])
