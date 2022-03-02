import os
import re

from .account import LogistikoSxedio
from .book import Book
from .transaction import Transaction
from .utils import gr2float

isodate = r"^\d{4}-\d{2}-\d{2}"
detline = r"^  ."

find_date = re.compile(isodate)
find_dlin = re.compile(detline)


def parse_000(path000):

    omades = {}
    valid_accounts = []

    with open(path000, encoding='utf8') as fil:

        for line in fil.readlines():

            if line.startswith('+'):
                _, account, *_ = line.split()
                valid_accounts.append(account)

            if line.startswith('>'):
                _, omada, typos, *_ = line.split()
                omades[omada] = typos

    return valid_accounts, omades


def parse_imerologio(lsx, book, errors, filepath):

    trn_id = 0

    with open(filepath, encoding='utf8') as fil:

        first_line = fil.readline().strip()  # first line

        if first_line not in ('j-open', 'j-normal', 'j-close'):
            errors.append(
                f"File {filepath} is not compatible. First line: '{first_line}'")
            return

        for i, row_line in enumerate(fil.readlines()):
            line = row_line.strip()

            if len(line) < 4:
                continue

            if line.startswith('#'):
                continue

            if find_date.findall(line):

                dat, par, _, per, *_ = line.split('"')
                dat = dat.strip()
                par = par.strip()
                per = per.strip()
                trn_id = len(book.transactions) + 1

                book.add_transaction(
                    trn_id, Transaction(dat, par, per, trn_id))

                continue

            if find_dlin.findall(row_line):

                accval, *sxolio = line.split("#")
                sxolio = sxolio[0].strip() if sxolio else ""
                account, *txtval = accval.split()

                if not lsx.is_valid_account(account):
                    errors.append(
                        f"Line {i+2}, account '{account}' is not registered")

                val = gr2float(txtval[0]) if txtval else 0
                trn = book.get_transaction(trn_id)

                if val:
                    trn.add_line(lsx.account(account), val, sxolio)
                else:
                    trn.add_last_line(lsx.account(account), sxolio)


def parse(bookname, bookdirectory):

    filenames = os.listdir(bookdirectory)

    if not '000' in filenames:
        raise ValueError(
            f"directory {bookdirectory} is not a valid accounting book")

    filenames.remove('000')

    valid_accounts, acc_types = parse_000(os.path.join(bookdirectory, '000'))

    lsx = LogistikoSxedio('home', acc_types)

    for acc in valid_accounts:
        lsx.account(acc)

    book = Book(bookname, lsx)

    errors = []
    # print('')
    filenames.sort()

    for filename in filenames:
        filepath = os.path.join(bookdirectory, filename)
        parse_imerologio(lsx, book, errors, filepath)
        # print(f"Finished parsing file: {filepath}")

    # print('\n\nErrors:\n', '\n'.join(errors), '\n\n')

    return book
