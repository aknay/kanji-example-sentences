from pathlib import Path
from typing import Callable

import yaml

from check_empty_ruby_tags import RubyTagCheckResult

EMPTY_RUBY_RT_TAG = "<ruby><rt></rt></ruby>"


def has_empty_ruby_rt_tag(path: Path) -> list[RubyTagCheckResult]:
    results = list()
    with open(path, "r") as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v:
                for index, sample in v["samples"].items():
                    if  sample is not None:
                        assert "ruby" in sample
                        if EMPTY_RUBY_RT_TAG in sample["ruby"]:
                            print("found", sample["ruby"])
                            result = RubyTagCheckResult(
                                kanji_word_seq_number=k, sample_location=index
                            )
                            results.append(result)

    return results


def replace_empty_ruby_rt_tag(
        path: Path, missing_ruby_tags: list[RubyTagCheckResult]
) -> None:
    with open(path, "r") as file:
        yml_content = yaml.safe_load(file)
        for m in missing_ruby_tags:
            sample_location_value = yml_content[m.kanji_word_seq_number]["samples"][
                m.sample_location
            ]
            ruby_tag: str = sample_location_value["ruby"]
            replaced_text = ruby_tag.replace(EMPTY_RUBY_RT_TAG, '')
            sample_location_value["ruby"] = replaced_text

        with open(path, "w") as file:
            yaml.safe_dump(yml_content, file, allow_unicode=True)


def replace_text(path: Path, results: list[RubyTagCheckResult], tag: str, replace_with: Callable[[str], str]) -> None:
    with open(path, "r") as file:
        yml_content = yaml.safe_load(file)
        for m in results:
            sample_location_value = yml_content[m.kanji_word_seq_number]["samples"][
                m.sample_location
            ]
            ruby_tag: str = sample_location_value[tag]
            replaced_text = replace_with(ruby_tag)
            print("replace", replaced_text)
            sample_location_value[tag] = replaced_text

        with open(path, "w") as file:
            yaml.safe_dump(yml_content, file, allow_unicode=True)


def has_this_issue(path: Path, callable: Callable[[dict], bool]) -> list[RubyTagCheckResult]:
    results = list()
    with open(path, "r") as file:
        kanjiInfo = yaml.safe_load(file)
        for k, v in kanjiInfo.items():
            if "samples" in v:
                for index, sample in v["samples"].items():
                    if sample is not None:
                        assert "ruby" in sample
                        if callable(sample):
                            print("found", sample)
                            result = RubyTagCheckResult(
                                kanji_word_seq_number=k, sample_location=index
                            )
                            results.append(result)

    return results
