import glob
import os

import yaml

# Directory containing the split YAML files
input_dir = "assets/split_jlpt_files"

# Dictionary to hold all combined data
all_combined_data = {}

# Find all YAML files in the specified directory
yaml_files = glob.glob(os.path.join(input_dir, "*.yaml"))

# Process each file
for filename in sorted(yaml_files):
    with open(filename, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict):
            all_combined_data.update(data)
        else:
            print(f"Warning: {filename} does not contain a dictionary.")

# Save the fully combined data to a single YAML file
with open("assets/generated_all_jlpt_combined.yaml", "w", encoding="utf-8") as f:
    yaml.dump(all_combined_data, f, allow_unicode=True)

print("✅ All JLPT-level YAML files have been combined into generated_all_jlpt_combined.yaml.")
