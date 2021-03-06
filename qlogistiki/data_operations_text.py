import os

from .book import Book
from .parser_text import parse


def load_from_text(text_file):
    try:
        book = Book(*parse(text_file))
        return book, True
    except ValueError as err:
        return None, err


def save2text(book, destination_file):
    if os.path.exists(destination_file):
        raise ValueError("file already exists")
    with open(destination_file, "w", encoding='utf8') as fil:
        fil.write(f"$ {book.afm} {book.company_name}\n")
        for trn in sorted(book.transactions):
            fil.write(trn.as_str())
            fil.write("\n")
    print(f"Book saved to {destination_file}")


def save_dummy(abook):
    txt = f"$ {abook.afm} {abook.company_name}\n"
    for trn in sorted(abook.transactions):
        txt += f"{trn.as_str()}\n"
    return txt
