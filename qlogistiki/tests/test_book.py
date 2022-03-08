import os

from qlogistiki.book import Book
from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))
bfile = os.path.join(dir_path, "book01")


# def test_book_creation():
#     b01, err = parse(bfile)
#     b01.get_transaction(2).lines_by_account_name('Χρεώστες')
