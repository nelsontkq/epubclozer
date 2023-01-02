import argparse
from pathlib import Path
import genanki
import random
import sys
from pathlib import Path
from ebooklib import ITEM_DOCUMENT
from ebooklib.epub import EpubBook, read_epub
import spacy
from bs4 import BeautifulSoup
import time


def parse_epub(ebook: EpubBook) -> list[str]:
    # img = None
    # try:
    #     img = next(ebook.get_items_of_type(ebooklib.ITEM_COVER)).content
    # except StopIteration:
    #     try:
    #         img = next(ebook.get_items_of_type(ebooklib.ITEM_IMAGE)).content
    #     except StopIteration:
    #         pass

    title = ebook.title

    lines = []
    for doc in ebook.get_items_of_type(ITEM_DOCUMENT):
        if doc.id == "titlepage":
            continue

        soup = BeautifulSoup(doc.get_content(), "html.parser")
        [lines.append(p.get_text()) for p in soup.find_all("p")]

    return lines


def get_all_lines(paragraphs: list[list[str]], nlp: spacy.Language, exclude_stop: bool):
    unique_words = {}
    for p in paragraphs:
        doc = nlp(p)
        for sentence in doc.sents:
            for token in sentence:
                if exclude_stop and token.is_stop:
                    continue
                if token.is_alpha:
                    if not token.lower_ in unique_words or len(unique_words) < len(
                        sentence.text
                    ):
                        unique_words[token.lower_] = sentence.text
    return unique_words


def process_epub(
    epub_path: str,
    lang: str,
    exclude_stop: bool,
):
    nlp = spacy.blank(lang)
    nlp.add_pipe("sentencizer")
    epub = read_epub(epub_path)
    parsed_paragraphs = parse_epub(epub)
    unique_word_sentences = get_all_lines(parsed_paragraphs, nlp, exclude_stop)
    print(len(unique_word_sentences.keys()))
    return unique_word_sentences


parser = argparse.ArgumentParser(
    prog="epubclozer",
    description="Turn an epub into Anki cloze flashcards",
)
parser.add_argument("-e", "--epub", required=True, help="The epub file to process")
parser.add_argument("-o", "--out-file")
parser.add_argument(
    "-l",
    "--lang",
    default="en",
    help="Any supported language seen here: https://spacy.io/usage/models#languages",
)
parser.add_argument(
    "-i",
    "--id",
    default=int(time.time()),
    help="What id you want the anki deck to have. Default is based on the current time",
)

parser.add_argument(
    "--exclude-stop-words",
    help="Exclude the 'stop' words, for example in english 'the', 'and', 'is'. This won't work unless you also provide the '-l' argument",
    action="store_true",
)


def main():
    args = parser.parse_args()
    unique_word_sentences = process_epub(args.epub, args.lang, args.exclude_stop_words)
    deck = genanki.Deck(args.id, Path(args.epub).stem)

    for word, sentence in unique_word_sentences.items():
        
        note = genanki.Note(
            model=genanki.CLOZE_MODEL,
            fields=[sentence.replace(word, "{{c1::" + word + "}}")],
        )
        deck.add_note(note)

    if args.out_file:
        out_path = Path(args.out_file)
    else:
        out_path = Path(args.epub).parent

    if out_path.is_dir():
        filename = Path(args.epub).stem + ".apkg"
        out_path = out_path.joinpath(filename)
    genanki.Package(deck).write_to_file(out_path, 0)


if __name__ == "__main__":
    main()
