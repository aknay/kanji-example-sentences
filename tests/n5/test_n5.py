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
    assert not failed_ids, f"Kanji not found in samples for the following IDs: {failed_ids}"
def test_exact_kanji_part_exists_in_all_of_the_examples(n5_part_file_path):
    # Function to check if a character is hiragana
    def is_hiragana(char):
        return '\u3040' <= char <= '\u309F'

    # Function to check if a character is kanji
    def is_kanji(char):
        return '\u4E00' <= char <= '\u9FFF'

    # Extract core kanji: remove hiragana at start and end, preserve hiragana between kanji
    def extract_core_kanji(word):
        chars = list(word)
        start = 0
        end = len(chars)

        # Remove leading hiragana
        while start < end and is_hiragana(chars[start]):
            start += 1
        # Remove trailing hiragana
        while end > start and is_hiragana(chars[end - 1]):
            end -= 1

        # Preserve all characters between start and end
        return ''.join(chars[start:end])

    # Check if core kanji is present in the sentence
    def check_core_kanji_presence(entry):
        core_kanji = extract_core_kanji(entry['kanji'])
        results = {}
        for idx, sample in entry['samples'].items():
            sentence = sample['kanji']
            results[idx] = core_kanji in sentence
        return core_kanji, results


    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    # Run the check and print results
    for entry_id, entry in data.items():
        core_kanji, results = check_core_kanji_presence(entry)
        print(f"Entry {entry_id} (Kanji: {entry['kanji']}, Core: {core_kanji}):")
        for sample_id, has_core in results.items():
            assert has_core, f"Sample {sample_id} has no core kanji."
            # print(f"  Sample {sample_id}: {'✅ Contains core kanji' if has_core else '❌ Missing core kanji'}")



