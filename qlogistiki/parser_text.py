import re

from .account import LogistikoSxedio
from .book import Book
from .transaction import Transaction
from .utils import gr2float

isodate = r"^\d{4}-\d{2}-\d{2}"
detline = r"^  ."

find_date = re.compile(isodate)
find_dlin = re.compile(detline)

account_types = {
    'Πάγια': 'pagia',
    '2': 'apothemata',
    'Ταμείο': 'apaitiseis',
    'Χρεώστες': 'apaitiseis',
    '4': 'kefalaio',
    'Πιστωτές': 'ypoxreoseis',
    'Αποθεματικό': 'ypoxreoseis',
    'Προμηθευτές': 'ypoxreoseis',
    'Εξοδα': 'ejoda',
    'Εσοδα': 'esoda',
    '8': 'anorgana',
    '54.00': 'fpa'
}


def parse(filepath):
    lsx = LogistikoSxedio('home', account_types)
    book = Book('test', lsx)
    trn_id = 0
    with open(filepath, encoding='utf8') as fil:

        for row_line in fil.readlines():

            line = row_line.strip()

            if len(line) < 4:
                continue

            if line.startswith('#'):
                continue

            if line.startswith('+'):
                _, acc, *_ = line.split()
                lsx.account(acc)

            if find_date.findall(line):
                dat, par, _, per, *_ = line.split('"')
                dat = dat.strip()
                par = par.strip()
                per = per.strip()
                trn_id += 1
                book.add_transaction(
                    trn_id, Transaction(dat, par, per, trn_id))
                continue

            if find_dlin.findall(row_line):

                accval, *sxolio = line.split("#")
                sxolio = sxolio[0].strip() if sxolio else ""
                account, *txtval = accval.split()

                if not lsx.is_valid_account(account):
                    raise ValueError(f'Account Error')

                val = gr2float(txtval[0]) if txtval else 0
                trn = book.get_transaction(trn_id)

                if val:
                    trn.add_line(lsx.account(account), val, sxolio)
                else:
                    trn.add_last_line(lsx.account(account), sxolio)

    return book
