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

@pytest.mark.parametrize("file_path", TEST_FILES)
def test_exact_kanji_exists_in_one_of_the_examples(file_path):
    # Load YAML data from a file
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Track entries that fail the test
    failed_ids = []

    # Iterate through each word entry safely
    for word_id, word_data in data.items():
        if isinstance(word_data, dict):
            target_kanji = word_data.get("kanji", "")
            samples = word_data.get("samples", {})

            found_in_any = False
            for sample in samples.values():
                sentence_kanji = sample.get("kanji", "")
                if target_kanji in sentence_kanji:
                    found_in_any = True
                    break  # No need to check further samples

            if not found_in_any:
                failed_ids.append((word_id, target_kanji, word_data.get("hiragana", "")))

        else:
            failed_ids.append((word_id, target_kanji, word_data.get("hiragana", "")))

    for word_id, target_kanji, hiragana in failed_ids:
        print(f"{word_id}: kanji: {target_kanji} hiragana: {hiragana}")

    # Final assertion
    print(f"Exact Kanji not found in samples for the following IDs: {failed_ids}. You should include at least one exact kanji.")
    assert not failed_ids, f"Kanji not found in samples for the following IDs: {failed_ids}"