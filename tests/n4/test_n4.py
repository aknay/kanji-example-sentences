from pathlib import Path

import pytest
import yaml

from assets.get_example_sentences_file_path import get_n4_part_file_path
from utils.utils import has_empty_ruby_rt_tag, is_valid_ruby


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

def test_check_at_least_one_sample(n4_part_file_path):
    with open(n4_part_file_path) as file:
        # Load YAML
        parsed_data = yaml.safe_load(file)

        # Check if there is at least one sample for each entry
        has_empty_sample = False
        for word_id, word_data in parsed_data.items():
            samples = word_data.get('samples', {})
            if not samples:
                print(f"Word with ID '{word_id}' has no samples.")
                has_empty_sample = True
            # else:
            #     print(f"Word with ID '{word_id}' has {len(samples)} sample(s).")

        assert has_empty_sample is False

def test_exact_kanji_exists_in_one_of_the_examples(n4_part_file_path):
    # Load YAML data from a file
    with open(n4_part_file_path, "r", encoding="utf-8") as file:
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