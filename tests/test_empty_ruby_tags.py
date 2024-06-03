from pathlib import Path
from check_empty_ruby_tags import check_empty_ruby_tag


def test_compare_list():
    results = check_empty_ruby_tag(path=Path("kanji_example_sentences.yml"))
    assert len(results) == 0