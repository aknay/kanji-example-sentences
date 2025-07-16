from pathlib import Path
import yaml
import re
import pytest

from assets.get_example_sentences_file_path import get_n5_part_file_path
from utils.utils import has_empty_ruby_rt_tag, is_valid_ruby


@pytest.fixture
def n5_part_file_path() -> Path:
    return get_n5_part_file_path()


def test_empty_ruby_tag(n5_part_file_path):
    results = has_empty_ruby_rt_tag(path=n5_part_file_path)
    assert len(results) == 0


def test_ruby_tag_is_correctly_formatted(n5_part_file_path):
    with open(n5_part_file_path) as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v and v['samples'] is not None:
                for key, sample in v["samples"].items():
                    if sample is not None:
                        assert "ruby" in sample
                        assert is_valid_ruby(sample['ruby']), print(sample['ruby'])


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


def is_all_kanji(s):
    # Unicode range for CJK Unified Ideographs
    return all('\u4e00' <= char <= '\u9fff' for char in s)


def test_ruby_exists_for_all_kanji_words(n5_part_file_path):
    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    failed_ids = []

    for word_id, word_data in data.items():
        if not isinstance(word_data, dict):
            continue

        target_kanji = word_data.get("kanji", "")
        samples = word_data.get("samples", {})

        if not target_kanji or not is_all_kanji(target_kanji):
            continue  # Skip non-kanji or mixed words

        found_ruby = False

        for sample in samples.values():
            ruby_text = sample.get("ruby", "")
            # Check for full-kanji ruby block
            if f"<ruby>{target_kanji}<rt>" in ruby_text:
                found_ruby = True
                break

        if not found_ruby:
            failed_ids.append((word_id, target_kanji, word_data.get("hiragana", "")))

    for word_id, target_kanji, hiragana in failed_ids:
        print(f"❌ {word_id}: Missing ruby for full-kanji word '{target_kanji}' (hiragana: {hiragana})")

    assert not failed_ids, f"Missing ruby for full-kanji words: {failed_ids}"


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


def test_kanji_and_hiragana_in_samples(n5_part_file_path):
    # Load YAML data from a file
    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Track entries that fail the test
    failed_kanji_ids = []
    failed_hiragana_ids = []

    # Iterate through each word entry safely
    for word_id, word_data in data.items():
        if isinstance(word_data, dict):
            target_kanji = word_data.get("kanji", "")
            target_hiragana = word_data.get("hiragana", "")
            samples = word_data.get("samples", {})

            # --- Check for Kanji existence (at least one sample) ---
            kanji_found_in_any = False
            for sample in samples.values():
                sentence_kanji = sample.get("kanji", "")
                if target_kanji in sentence_kanji:
                    kanji_found_in_any = True
                    break

            if not kanji_found_in_any:
                failed_kanji_ids.append((word_id, target_kanji, target_hiragana, "N/A",
                                         "N/A"))  # No specific sample to report for kanji not found at all

            # --- Check for Hiragana existence (every sample) ---
            for sample_index, sample in samples.items():
                sentence_hiragana = sample.get("hiragana", "")
                sentence_kanji = sample.get("kanji", "")  # Get kanji sentence here too

                if target_hiragana not in sentence_hiragana:
                    failed_hiragana_ids.append(
                        (word_id, target_hiragana, target_kanji, sentence_hiragana, sentence_kanji,
                         f"Sample {sample_index}"))

        else:
            print(f"Warning: Entry {word_id} is not a dictionary. Skipping checks.")

    # --- Print detailed failure reports ---

    if failed_kanji_ids:
        print("\n--- Kanji Not Found in Any Sample ---")
        for word_id, kanji, hiragana, _, _ in failed_kanji_ids:
            print(f"ID: {word_id}, Word Kanji: '{kanji}', Word Hiragana: '{hiragana}'")
            print(f"  Reason: Target kanji '{kanji}' was not found in *any* sample sentence's kanji field.")

    if failed_hiragana_ids:
        print("\n--- Hiragana Not Found in ALL Samples ---")
        for word_id, hiragana, kanji, failed_hiragana_sentence, failed_kanji_sentence, sample_info in failed_hiragana_ids:
            print(f"ID: {word_id}, Word Hiragana: '{hiragana}', Word Kanji: '{kanji}'")
            print(f"  Failed in {sample_info}:")
            print(f"    Hiragana Sentence: '{failed_hiragana_sentence}'")
            print(f"    Kanji Sentence:    '{failed_kanji_sentence}'")
            print(f"  Reason: Target hiragana '{hiragana}' was not found in this sample's hiragana field.")

    # --- Final assertions ---
    assert not failed_kanji_ids, f"Kanji not found in any sample for the following IDs: {failed_kanji_ids}"
    assert not failed_hiragana_ids, f"Hiragana not found in ALL samples for the following IDs: {failed_hiragana_ids}"


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
            if not has_core:
                print(f"❌ missing core: Sample {sample_id} has no core kanji.")
            # print(f"  Sample {sample_id}: {'✅ Contains core kanji' if has_core else '❌ Missing core kanji'}")
            assert has_core, f"Sample {sample_id} has no core kanji."
            # print(f"  Sample {sample_id}: {'✅ Contains core kanji' if has_core else '❌ Missing core kanji'}")


# Unicode ranges for Japanese characters
# Hiragana: U+3040 – U+309F
HIRAGANA_RANGE = (0x3040, 0x309F)
# Katakana: U+30A0 – U+30FF
KATAKANA_RANGE = (0x30A0, 0x30FF)
# Common CJK Unified Ideographs (Kanji): U+4E00 – U+9FFF
KANJI_RANGE = (0x4E00, 0x9FFF)


def contains_kanji(text):
    """
    Checks if a string contains any Kanji characters.
    This function specifically looks for characters within the common CJK Unified Ideographs range.
    """
    # Create the regex pattern string using chr() for unicode characters
    # This avoids the f-string unicode escape issue.
    kanji_pattern_str = f'[{chr(KANJI_RANGE[0])}-{chr(KANJI_RANGE[1])}]'
    kanji_pattern = re.compile(kanji_pattern_str)

    return bool(kanji_pattern.search(text))




def test_hiragana_field_purity(n5_part_file_path):
    """
    Tests that the 'hiragana' field in sample sentences contains only hiragana
    (and other allowed characters like punctuation/spaces/numbers/katakana, if applicable),
    and specifically does NOT contain any Kanji.
    """
    with open(n5_part_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    failed_hiragana_purity_ids = []

    for word_id, word_data in data.items():
        if isinstance(word_data, dict):
            samples = word_data.get("samples", {})

            for sample_index, sample in samples.items():
                sentence_hiragana = sample.get("hiragana", "")
                sentence_kanji_original = sample.get("kanji", "")  # For better error reporting

                # Check if the hiragana sentence contains any Kanji
                if contains_kanji(sentence_hiragana):
                    failed_hiragana_purity_ids.append(
                        (word_id, f"Sample {sample_index}", sentence_hiragana, sentence_kanji_original,
                         "Contains Kanji"))

        else:
            print(f"Warning: Entry {word_id} is not a dictionary. Skipping purity check.")

    if failed_hiragana_purity_ids:
        print("\n--- Hiragana Field Purity Check Failures (Contains Kanji) ---")
        for word_id, sample_info, hiragana_sentence, kanji_sentence_original, reason in failed_hiragana_purity_ids:
            print(f"ID: {word_id}, {sample_info}")
            print(f"  Hiragana Sentence (failed): '{hiragana_sentence}'")
            print(f"  Original Kanji Sentence:  '{kanji_sentence_original}'")
            print(f"  Reason: {reason}")

    assert not failed_hiragana_purity_ids, f"Hiragana samples contain Kanji characters for the following: {failed_hiragana_purity_ids}"





