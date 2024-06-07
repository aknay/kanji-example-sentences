import datetime
import json

import yaml

from assets.get_example_sentences_file_path import getExampleSentenceFilePath

with open(getExampleSentenceFilePath(), 'r') as file:
    kanjiInfo = yaml.safe_load(file)

    with open('example_sentences.json', 'w') as f:
        f.write(json.dumps(kanjiInfo,ensure_ascii=False))

    with open('example_sentences_version.json', 'w') as f:
        version = {}
        now = datetime.datetime.now()

        dt = datetime.datetime.now()
        truncatedUnixTime = int(dt.timestamp())
        version["unix_build_time"] = truncatedUnixTime
        f.write(json.dumps(version,ensure_ascii=False))