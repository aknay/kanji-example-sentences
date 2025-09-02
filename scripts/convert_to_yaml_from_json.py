import json

import yaml

from assets.char.get_path import get_kanji_dic_json_file, get_kanji_dic_yaml_saving_file

try:
    with open(get_kanji_dic_json_file(), 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Process your data here
        print("Successfully read the JSON file.")
        print(data['characters']['亜'])

        yaml_data = yaml.dump(data, allow_unicode=True, default_flow_style=False)

        with open(get_kanji_dic_yaml_saving_file(), 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

except FileNotFoundError:
    print(f"Error: The file was not found at")
except json.JSONDecodeError:
    print("Error: The file is not a valid JSON.")
