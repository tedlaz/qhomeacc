import os
import re

from .account import LogistikoSxedio
from .book import Book
from .transaction import Transaction
from .utils import gr2float

find_date = re.compile(r"^\d{4}-\d{2}-\d{2}")
find_dlin = re.compile(r"^  .")
find_in_curly = re.compile(r"\{(.*?)\}")


def parse_000(path000):

    book_name = ''
    omades = {}
    valid_accounts = []

    with open(path000, encoding='utf8') as fil:

        for line in fil.readlines():

            if line.startswith('@'):
                _, *book_name_list = line.split()
                book_name = ' '.join(book_name_list)

            if line.startswith('+'):
                _, account, *_ = line.split()
                valid_accounts.append(account)

            if line.startswith('>'):
                _, omada, typos, *_ = line.split()
                omades[omada] = typos

    return valid_accounts, omades, book_name


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

            if line.startswith(("@")):
                # @ 2020-05-10 Αγορές.Εμπορευμάτων.εσωτερικού -120,32
                _, cdat, cacc, cval = line.split()
                book.add_validation((cdat, cacc, gr2float(cval)))

            if find_date.findall(line):

                dat, par, _, per, *_ = line.split('"')
                dat = dat.strip()
                par = par.strip()
                per = per.strip()

                trn_id = book.add_transaction(Transaction(dat, par, per))

                continue

            if find_dlin.findall(row_line):

                accval, *sxolia = line.split("#")
                sxolio = sxolia[0].strip() if sxolia else ''
                account, *txtval = accval.split()

                if not lsx.is_valid_account(account):
                    errors.append(
                        f"{filepath}:{i+2}, ο λογαριασμός '{account}' δεν είναι καταχωρημένος")

                val = gr2float(txtval[0]) if txtval else 0
                trn = book.get_transaction(trn_id)

                if val:
                    trn.add_line(lsx.account(account), val, sxolio)
                else:
                    trn.add_last_line(lsx.account(account), sxolio)


def parse(book_dir):
    errors = []
    filenames = os.listdir(book_dir)

    if not '000' in filenames:
        errors.append(
            f"Ο Φάκελος {book_dir} δεν περιέχει βιβλίο εγγραφών λογιστικής")
        return None, errors

    filenames.remove('000')

    valid_accounts, acc_types, bname = parse_000(os.path.join(book_dir, '000'))

    lsx = LogistikoSxedio('home', acc_types)

    for acc in valid_accounts:
        lsx.account(acc)

    book = Book(bname, lsx)

    # print('')
    filenames.sort()

    for filename in filenames:
        filepath = os.path.join(book_dir, filename)
        parse_imerologio(lsx, book, errors, filepath)

    # print('n\nErrors:\n', '\n'.join(errors), '\n')

    return book, errors
