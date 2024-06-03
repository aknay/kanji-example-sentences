# kanji-example-sentences

The example sentences are generated using ChatGPT (prompt: N5 level and as simple as possible). These example sentences are used in the Kanji Flashcards App for educational purposes. 

#### Mobile Apps
[<img src="resources/images/google-play-badge.png" height="50">](https://play.google.com/store/apps/details?id=io.maker.kanjiflashcards)

Disclaimer: I am not responsible for the accuracy of the generated example sentences since they are created by ChatGPT.

#### Development
1. The sequence number and kanji word come from the [JMdict](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) Project. 

2. ChatGPT will generate based on kanji word provided by the user.

```
kanji: 紙
samples:
  0:
    english: Please give me a piece of paper.
    hiragana: かみ を いちまい ください。
    kanji: 紙を一枚ください。
  1:
    english: This paper is very thin.
    hiragana: この かみ は とても うすい です。
    kanji: この紙はとても薄いです。
  2:
    english: He wrote his name on the paper.
    hiragana: かれ は かみ に なまえ を かきました。
    kanji: 彼は紙に名前を書きました。
simple_meaning:
  1: paper
  2: sheet (of paper)
```

3. The `check_empty_ruby_tags.py` script will check and add necessary ruby tags to the existing `kanji_example_sentences.yml`. The result can be seen below for the key `1311530`.
```
'1311530':
  kanji: 紙
  samples:
    0:
      english: Please give me a piece of paper.
      hiragana: かみ を いちまい ください。
      kanji: 紙を一枚ください。
      ruby: <ruby>紙<rt>かみ</rt></ruby>を<ruby>一<rt>いち</rt></ruby><ruby>枚<rt>まい</rt></ruby>ください。
    1:
      english: This paper is very thin.
      hiragana: この かみ は とても うすい です。
      kanji: この紙はとても薄いです。
      ruby: この<ruby>紙<rt>かみ</rt></ruby>はとても<ruby>薄<rt>うす</rt></ruby>いです。
    2:
      english: He wrote his name on the paper.
      hiragana: かれ は かみ に なまえ を かきました。
      kanji: 彼は紙に名前を書きました。
      ruby: <ruby>彼<rt>かれ</rt></ruby>は<ruby>紙<rt>かみ</rt></ruby>に<ruby>名前<rt>なまえ</rt></ruby>を<ruby>書<rt>か</rt></ruby>きました。
  simple_meaning:
    1: paper
    2: sheet (of paper)
```