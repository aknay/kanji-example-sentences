import pytest
import yaml

from assets.get_example_sentences_file_path import get_n4_part_file_path, get_n5_part_file_path, \
    get_n3_part_two_file_path, get_n3_part_one_file_path
from utils.utils import has_empty_ruby_rt_tag, is_valid_ruby


# Assume has_empty_ruby_rt_tag is imported from 'your_module'

def test_empty_ruby_tag(n4_part_file_path):
    results = has_empty_ruby_rt_tag(path=n4_part_file_path)
    assert len(results) == 0


# List the file paths you want to use for the test
TEST_FILES = [
    get_n4_part_file_path(),
    get_n5_part_file_path(),
    get_n3_part_one_file_path(),
    get_n3_part_two_file_path()

]


@pytest.mark.parametrize("file_path", TEST_FILES)
def test_empty_ruby_tag(file_path):
    """Runs the test with each file path provided by the parametrize marker."""
    results = has_empty_ruby_rt_tag(path=file_path)
    assert len(results) == 0

@pytest.mark.parametrize("file_path", TEST_FILES)
def test_ruby_tag_is_correctly_formatted(file_path):
    with open(file_path) as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v and v['samples'] is not None:
                for key, sample in v["samples"].items():
                    if sample is not None:
                        assert "ruby" in sample
                        assert is_valid_ruby(sample['ruby']), print(sample['ruby'])
