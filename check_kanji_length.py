from pathlib import Path
from statistics import median

import yaml


def check_kanji_length(path: Path) -> None:
    kanji_length_list = list()
    with open(path, "r") as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v:
                for _, sample in v["samples"].items():
                    kanji_length_list.append(len(sample["kanji"]))
                    if len(sample["kanji"]) > 30:
                        print(sample["kanji"])

    # print(kanji_length_list)
    max_value = max(kanji_length_list)
    min_value = min(kanji_length_list)
    median_value = median(kanji_length_list)
    print(max_value, min_value, median_value)


if __name__ == "__main__":
    kanji_length_list = list()
    with open(Path("kanji_example_sentences.yml"), "r") as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v:
                for _, sample in v["samples"].items():
                    kanji_length_list.append(len(sample["kanji"]))
                    if len(sample["kanji"]) > 30:
                        print(sample["kanji"])

    max_value = max(kanji_length_list)
    min_value = min(kanji_length_list)
    median_value = median(kanji_length_list)
    print("max:", max_value)
    print("min:", min_value)
    print("median:", median_value)
