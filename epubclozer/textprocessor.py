from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from ebooklib import ITEM_DOCUMENT
from ebooklib.epub import EpubBook, read_epub
import spacy
from bs4 import BeautifulSoup


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
        
        soup = BeautifulSoup(doc.get_content(), 'html.parser')
        [lines.append(p.get_text()) for p in soup.find_all('p')]

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
                    if not token.lower_ in unique_words or len(unique_words) < len(sentence.text):
                        unique_words[token.lower_] = sentence.text
    return unique_words

def process_epub(
    epub_path: str,
    lang: str,
    exclude_stop: bool,
):
    nlp = spacy.blank(lang)
    nlp.add_pipe('sentencizer')
    epub = read_epub(epub_path)
    parsed_paragraphs = parse_epub(epub)
    unique_word_sentences = get_all_lines(parsed_paragraphs, nlp, exclude_stop)
    print(len(unique_word_sentences.keys()))
    return unique_word_sentences
    