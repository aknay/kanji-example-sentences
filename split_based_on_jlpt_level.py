from collections import defaultdict

import yaml

from assets.get_example_sentences_file_path import get_example_sentence_file_path

# Load your YAML file
with open(get_example_sentence_file_path(), "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
grouped_data = defaultdict(dict)
for key, value in data.items():
    if isinstance(value, dict):
        jlpt_level = value.get('jisho_info', {}).get('jlpt_level')
        jlpt_key = jlpt_level if jlpt_level else 'null'
        grouped_data[jlpt_key][key] = value
    else:
        print(f"Skipping key {key} {value} because its value is not a dictionary.")

# Save each group into separate YAML files, splitting further if more than 1000 items
for jlpt_level, entries in grouped_data.items():
    keys = list(entries.keys())
    total = len(keys)
    if total <= 1000:
        filename = f"assets/splited_jlpt_files/{jlpt_level}.yaml"
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(entries, f, allow_unicode=True)
    else:
        for i in range(0, total, 1000):
            chunk = {k: entries[k] for k in keys[i:i + 1000]}
            filename = f"assets/splited_jlpt_files/{jlpt_level}_part{i // 1000 + 1}.yaml"
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump(chunk, f, allow_unicode=True)

print("JLPT-level YAML files have been created and split if necessary.")
