import os

from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_parse():
    book_dir = os.path.join(dir_path, "book01")
    mybook = parse(book_dir)
    # print(mybook.transactions)
    # print(mybook.kartella('Εσοδα'))
    # print(mybook.chart)
    # print(mybook.transactions[1])
    assert mybook.is_balanced
    # print(mybook.isozygio())
