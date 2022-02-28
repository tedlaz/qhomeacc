import os

from qlogistiki.parser_text import parse

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_parse():
    file_path = os.path.join(dir_path, "koinoxrista")
    mybook = parse(file_path)
    # print(mybook.transactions)
    # print(mybook.kartella('Εσοδα'))
    # print(mybook.chart)
    # print(mybook.transactions[1])
    assert mybook.is_balanced
    print(mybook.isozygio())
