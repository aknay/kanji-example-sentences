from pathlib import Path

import pytest
import yaml

from assets.get_example_sentences_file_path import get_n4_part_file_path
from is_ruby_formated_correctly import is_valid_ruby
from utils.utils import has_empty_ruby_rt_tag


@pytest.fixture
def n4_part_file_path() -> Path:
    return get_n4_part_file_path()

def test_empty_ruby_tag(n4_part_file_path):
    results = has_empty_ruby_rt_tag(path=n4_part_file_path)
    assert len(results) == 0

def test_ruby_tag_is_correctly_formatted(n4_part_file_path):
    with open(n4_part_file_path) as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v and v['samples'] is not None:
                for key, sample in v["samples"].items():
                    if sample is not None:
                        assert "ruby" in sample
                        assert is_valid_ruby(sample['ruby']), print(sample['ruby'])