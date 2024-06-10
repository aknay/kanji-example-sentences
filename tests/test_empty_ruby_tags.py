from pathlib import Path

import pytest

from assets.get_example_sentences_file_path import getExampleSentenceFilePath
from check_empty_ruby_tags import check_empty_ruby_tag
from utils.utils import has_this_issue


@pytest.fixture
def example_sentences_file_path() -> Path:
    return getExampleSentenceFilePath()


def test_empty_ruby_tag(example_sentences_file_path):
    results = check_empty_ruby_tag(path=example_sentences_file_path)
    assert len(results) == 0


def test_should_not_have_any_english_question_mark_for_kanji(example_sentences_file_path):
    b = lambda x: x["kanji"].endswith('?')
    results = has_this_issue(path=getExampleSentenceFilePath(), callable=b)
    assert len(results) == 0


def test_should_not_have_any_english_question_mark_for_ruby(example_sentences_file_path):
    b = lambda x: x["ruby"].endswith('?')
    results = has_this_issue(path=getExampleSentenceFilePath(), callable=b)
    assert len(results) == 0


def test_should_have_japanese_japanese_period_or_question_mark_for_kanji(example_sentences_file_path):
    b = lambda x: not (x["kanji"].endswith('。') or x["kanji"].endswith('？'))
    results = has_this_issue(path=getExampleSentenceFilePath(), callable=b)
    assert len(results) == 0


def test_should_have_japanese_japanese_period_or_question_mark_for_ruby(example_sentences_file_path):
    b = lambda x: not (x["ruby"].endswith('。') or x["ruby"].endswith('？'))
    results = has_this_issue(path=getExampleSentenceFilePath(), callable=b)
    assert len(results) == 0
