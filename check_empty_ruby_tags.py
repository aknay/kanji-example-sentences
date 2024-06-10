from dataclasses import dataclass
from pathlib import Path

import yaml
from pyrigana import pyrigana


@dataclass(frozen=True)
class RubyTagCheckResult:
    kanji_word_seq_number: str
    sample_location: int


def check_empty_ruby_tag(path: Path) -> list[RubyTagCheckResult]:
    results = list()
    with open(path, "r") as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v:
                for index, sample in v["samples"].items():
                    if "ruby" not in sample:
                        result = RubyTagCheckResult(
                            kanji_word_seq_number=k, sample_location=index
                        )
                        results.append(result)
                    else:
                        pass

        return results


def replace_empty_ruby_tag(
    path: Path, missing_ruby_tags: list[RubyTagCheckResult]
) -> None:
    with open(path, "r") as file:
        yml_content = yaml.safe_load(file)
        for m in missing_ruby_tags:
            sample_location_value = yml_content[m.kanji_word_seq_number]["samples"][m.sample_location]
            assert 'ruby' not in sample_location_value
            kanji_sentence = sample_location_value["kanji"]
            sample_location_value["ruby"] = {}
            sample_location_value["ruby"] = pyrigana.get_furigana_html(kanji_sentence)

        with open(path, "w") as file:
            yaml.safe_dump(yml_content, file, allow_unicode=True)


if __name__ == "__main__":
    results = check_empty_ruby_tag(path=Path("assets/kanji_example_sentences.yml"))
    if len(results) != 0:
        replace_empty_ruby_tag(
            path=Path("assets/kanji_example_sentences.yml"), missing_ruby_tags=results
        )
    else:
        print("🥳 there is no empty ruby tag")
