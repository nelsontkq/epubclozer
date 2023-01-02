
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

From the command line:

Create a close for each unique word in epub:

```shell
epubclozer --lang "en" --path "C:/path/to/book.epub"
```

Ignore specific words by creating an ignore file

`ignore.txt`
```
be
to
of
and
a
in
that
have
I
it
for
not
on
with
...
```

```shell
epubclozer --lang "es" --path "C:/path/to/book.epub" --ignore-file "C:/path/to/ignore.txt"
```

See `epubclozer --help` for all options

Your Anki package will be put in the same location as the epub.
