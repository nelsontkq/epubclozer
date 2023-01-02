
# Epub Clozer

Turn an epub into Anki cloze flashcards

## Description

This script will take every unique word in an epub and create a anki cloze flashcard using an example found in the book.


## Requirements

Install [python 3.11](https://www.python.org/downloads/)

Install epubclozer

```shell
python -m pip install epubclozer
```

## How to use

Create a cloze for each unique word in epub:

```shell
python -m epubclozer --lang "en" --path "C:/path/to/book.epub"
```

Ignore [stop words](https://en.wikipedia.org/wiki/Stop_word) by adding the `--exclude-stop-words` option. 

Note this will only work effectively in you pass the target language `--lang` as well.

```shell
python -m epubclozer --lang "es" --path "C:/path/to/book.epub" --exclude-stop-words
```

See `epubclozer --help` for all options

Your Anki package will be put in the same location as the epub.
