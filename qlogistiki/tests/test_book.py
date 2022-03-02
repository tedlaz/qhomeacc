import os

from qlogistiki.book import Book
from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))
bfile = os.path.join(dir_path, "book01")


def test_book_creation():
    b01 = parse('Test Book', bfile)
    print(b01.isozygio())
