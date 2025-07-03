from pathlib import Path

import pytest
import yaml

from assets.get_example_sentences_file_path import get_example_sentence_file_path


# Replace this with loading from a file if needed
@pytest.fixture
def example_sentences_file_path() -> Path:
    return get_example_sentence_file_path()


def test_missing_ids_for_n4(example_sentences_file_path):
    with open(example_sentences_file_path) as file:
        data = yaml.safe_load(file)

        # Function to check if simple_meaning is missing or all null
        def is_meaning_missing(meaning):
            return not meaning or all(v is None for v in meaning.values())

        # Filter and collect kanji and hiragana
        missing_entries = [
            {"kanji": details.get("kanji"), "hiragana": details.get("hiragana")}
            for details in data.values()
            if details.get("jisho_info", {}).get("jlpt_level") == "N4"
               and is_meaning_missing(details.get("simple_meaning", {}))
        ]
        print("missing_entries", len(missing_entries))
        assert len(missing_entries) == 0


def test_missing_samples_for_n4(example_sentences_file_path):
    with open(example_sentences_file_path) as file:

        # Load the YAML content
        data = yaml.safe_load(file)

        # Function to check for empty or null samples
        def check_empty_samples(data):
            empty_samples_entries = []
            for key, value in data.items():
                jlpt_level = value.get('jisho_info', {}).get('jlpt_level')
                samples = value.get('samples')
                if jlpt_level == 'N4' and (samples is None or all(v is None for v in samples.values())):
                    value['id'] = key  # Add ID to the entry
                    empty_samples_entries.append(value)
            return empty_samples_entries

        # Check for empty samples
        empty_samples_entries = check_empty_samples(data)

        # Save to file
        with open("samples_missing_meaning_entries.txt", "w", encoding="utf-8") as f:
            for entry in empty_samples_entries:
                f.write(f"ID: {entry['id']}, Kanji: {entry['kanji']}, Hiragana: {entry['hiragana']}\n")

        print("File saved as missing_meaning_entries.txt")

