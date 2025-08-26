import yaml
import re

from assets.get_example_sentences_file_path import get_n5_part_file_path
#
# # Load the YAML file
# with open(get_n5_part_file_path(), "r", encoding="utf-8") as f:
#     data = yaml.safe_load(f)

import yaml
import re

import yaml
import re

# Load YAML data
# with open(get_n5_part_file_path(), "r", encoding="utf-8") as f:
#     data = yaml.safe_load(f)


# Function to check if a ruby tag exists for kanji_part and its reading
import yaml
import re

# Load YAML data


import yaml
import re

# Load the YAML data
# with open("your_file.yaml", "r", encoding="utf-8") as f:
#     data = yaml.safe_load(f)

# Check if character is kanji
def is_kanji(char):
    return '\u4e00' <= char <= '\u9faf'

# Trim matching prefix
def trim_prefix(kanji, hira):
    i = 0
    while i < min(len(kanji), len(hira)) and kanji[i] == hira[i]:
        i += 1
    return kanji[i:], hira[i:]

# Trim matching suffix
def trim_suffix(kanji, hira):
    i = 0
    while i < min(len(kanji), len(hira)) and kanji[-(i+1)] == hira[-(i+1)]:
        i += 1
    return kanji[:len(kanji)-i] if i else kanji, hira[:len(hira)-i] if i else hira

# Main function to extract kanji-reading pair
def extract_target_kanji_reading(kanji_text, hira_text):
    # Step 1: drop matching prefix
    kanji_trimmed, hira_trimmed = trim_prefix(kanji_text, hira_text)
    # Step 2: drop matching suffix
    kanji_core, hira_core = trim_suffix(kanji_trimmed, hira_trimmed)

    # Final check: make sure the kanji part is actually kanji
    if not all(is_kanji(c) for c in kanji_core) or not hira_core:
        return None, None

    return kanji_core, hira_core

# Check for expected ruby tag
def _has_valid_ruby(kanji, reading, ruby_text):
    pattern = f"<ruby>{re.escape(kanji)}<rt>{re.escape(reading)}</rt></ruby>"
    return re.search(pattern, ruby_text) is not None

def check_missing_ruby_based_on_kanji(file_path: str):
    found_missing_top = False
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        # Process the entries
        for entry_id, entry in data.items():
            kanji_text = entry.get("kanji", "")
            hira_text = entry.get("hiragana", "")
            samples = entry.get("samples", {})

            if not kanji_text or not hira_text:
                continue

            kanji_part, reading_part = extract_target_kanji_reading(kanji_text, hira_text)

            if not kanji_part or not reading_part:
                continue

            # print(f"\n🔍 Checking ID {entry_id}")
            # print(f"    Kanji: {kanji_text}")
            # print(f"    Hiragana: {hira_text}")
            # print(f"    ➤ Looking for <ruby>{kanji_part}<rt>{reading_part}</rt></ruby>")

            found_missing = False
            for idx, sample in samples.items():
                ruby = sample.get("ruby", "")
                if _has_valid_ruby(kanji_part, reading_part, ruby):
                    pass
                    # print(f"  ✅ Sample {idx}: Valid ruby tag found.")
                else:
                    found_missing = True
                    found_missing_top = True
                    # print(f"  ❌ Sample {idx}: Missing ruby: <ruby>{kanji_part}<rt>{reading_part}</rt></ruby>")

            if found_missing:
                print(f"\n🔍 Checking ID {entry_id}")
                print(f"    Kanji: {kanji_text}")
                print(f"    Hiragana: {hira_text}")
                print(f"    ➤ Looking for <ruby>{kanji_part}<rt>{reading_part}</rt></ruby>")
                for idx, sample in samples.items():
                    ruby = sample.get("ruby", "")
                    if _has_valid_ruby(kanji_part, reading_part, ruby):
                        pass
                        # print(f"  ✅ Sample {idx}: Valid ruby tag found.")
                    else:
                        print(f"  ❌ Sample {idx}: Missing ruby: <ruby>{kanji_part}<rt>{reading_part}</rt></ruby>")

        return found_missing_top





