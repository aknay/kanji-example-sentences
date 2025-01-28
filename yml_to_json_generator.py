import datetime
import json

import yaml

from assets.get_example_sentences_file_path import getExampleSentenceFilePath


def remove_none_values(d):
    if isinstance(d, dict):
        return {k: remove_none_values(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [remove_none_values(item) for item in d if item is not None]
    else:
        return d


def are_samples_and_meaning_empty(d):
    return not d.get('samples') and not d.get('simple_meaning')


with open(getExampleSentenceFilePath(), 'r') as file:
    kanjiInfo = yaml.safe_load(file)
    new_kanji_info = {}
    with open('example_sentences.json', 'w') as f:
        for k, v in kanjiInfo.items():
            """we want to remove it because we already have jisho_info in another database. added in yml for viewing purpose"""
            if 'jisho_info' in v:
                del v['jisho_info']
            v = remove_none_values(v)

            """just want to make file size smaller"""
            is_empty_samples_and_meanings = are_samples_and_meaning_empty(v)

            if not is_empty_samples_and_meanings:
                new_kanji_info[k] = v

        f.write(json.dumps(new_kanji_info, ensure_ascii=False))

    with open('example_sentences_version.json', 'w') as f:
        version = {}
        now = datetime.datetime.now()

        dt = datetime.datetime.now()
        truncatedUnixTime = int(dt.timestamp())
        version["unix_build_time"] = truncatedUnixTime
        f.write(json.dumps(version, ensure_ascii=False))
