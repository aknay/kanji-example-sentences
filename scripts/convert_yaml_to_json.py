import json

import yaml

from assets.char.get_path import get_kanji_dic_generated_json_saving_file, get_kanji_dic_yaml_saving_file

try:
    # 1. Read the YAML file
    with open(get_kanji_dic_yaml_saving_file(), 'r', encoding='utf-8') as f:
        # Load the YAML data into a Python dictionary
        data = yaml.safe_load(f)
        print("Successfully read the YAML file.")

    # 2. Save the data back to a JSON file
    with open(get_kanji_dic_generated_json_saving_file(), 'w', encoding='utf-8') as f:
        # Dump the Python dictionary as JSON
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("Successfully saved the data to a JSON file.")

except FileNotFoundError:
    print("Error: The file was not found.")
except yaml.YAMLError as e:
    print(f"Error: There was an issue with the YAML file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
