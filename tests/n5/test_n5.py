from pathlib import Path

import pytest

from assets.get_example_sentences_file_path import get_n5_part_file_path


@pytest.fixture
def n5_part_file_path() -> Path:
    return get_n5_part_file_path()


def test_find_malformed_ids(n5_part_file_path):
    # Load YAML data from a file
    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Collect malformed entries
    malformed_ids = []

    for word_id, word_data in data.items():
        if not isinstance(word_data, dict):
            malformed_ids.append(word_id)

    # Print malformed IDs
    if malformed_ids:
        print("Malformed entries found:")
        for mid in malformed_ids:
            print(f"  - {mid}")
    else:
        print("No malformed entries found.")


import yaml


def test_exact_kanji_exists_in_one_of_the_examples(n5_part_file_path):
    # Load YAML data from a file
    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Track entries that fail the test
    failed_ids = []
    failed_kanjis = []
    failed_hiraganas = []

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
                # failed_kanjis.append(target_kanji)
                # failed_hiraganas.append(samples.get("hiraganas", ""))
        else:
            failed_ids.append((word_id, target_kanji, word_data.get("hiragana", "")))
            # failed_kanjis.append(target_kanji)
            # failed_hiraganas.append(samples.get("hiraganas", ""))

    for word_id, target_kanji, hiragana in failed_ids:
        print(f"{word_id}: kanji: {target_kanji} hiragana: {hiragana}")

    # Final assertion
    assert not failed_ids, f"Kanji not found in samples for the following IDs: {failed_ids}"
