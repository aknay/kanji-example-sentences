from pathlib import Path

import yaml
import pytest

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


