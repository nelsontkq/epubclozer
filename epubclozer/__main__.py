from textprocessor import process_epub
import argparse
from pathlib import Path
import genanki
import random
import sys

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
    default=random.randint(1, sys.maxsize),
    help="What id you want the anki deck to have. Default is random",
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
        deck.add_note(
            genanki.Note(
                model=genanki.CLOZE_MODEL,
                fields=[sentence.replace(word, "{{c1::" + word + "}}")],
            )
        )

    if args.out_file:
        out_path = Path(args.out_file)
    else:
        out_path = Path(args.epub).parent

    if out_path.is_dir():
        filename = Path(args.epub).stem + ".apkg"
        out_path = out_path.joinpath(filename)
    genanki.Package(deck).write_to_file(out_path)


if __name__ == "__main__":
    main()
