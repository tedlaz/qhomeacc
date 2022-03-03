from datetime import date
from typing import Optional
from unicodedata import name

from .account import LogistikoSxedio
from .transaction import Transaction
from .utils import f2gr


class Book:

    def __init__(self, name, lsx: LogistikoSxedio):
        self.name: str = name
        self.chart: LogistikoSxedio = lsx
        self.transactions: dict[int, Transaction] = {}  # {id: Transaction}
        self._last_id = 0

    def transactions_filter(self, apo=None, eos=None):
        for transaction in self.transactions.values():

            if apo and transaction.date < date.fromisoformat(apo):
                continue

            if eos and transaction.date > date.fromisoformat(eos):
                continue

            yield transaction

    def kartella(self, account_name: str, apo=None, eos=None) -> list:
        tvalue = tdebit = tcredit = tdelta = 0
        lines = []

        transactions = self.transactions_filter(apo, eos)

        for trn in sorted(transactions):
            for line in trn.lines_by_account_name(account_name):

                tvalue += line['value']
                line['tvalue'] = tvalue

                tdebit += line['debit']
                line['tdebit'] = tdebit

                tcredit += line['credit']
                line['tcredit'] = tcredit

                tdelta += line['delta']
                line['tdelta'] = tdelta

                lines.append(line)

        return lines

    def model_kartella(self, account_name: str, apo=None, eos=None):
        lines = self.kartella(account_name, apo, eos)
        headers = [
            'Νο',
            'Ημ/νία',
            'Χρέωση',
            'Πίστωση',
            'Υπόλοιπο',
            'Περιγραφή',
            'Σχόλιο',
            'Παρ/κό',
        ]
        aligns = [3, 1, 3, 3, 3, 1, 1, 1]
        data = []
        for lin in lines:
            data.append(
                [
                    lin['id'],
                    lin['date'],
                    f2gr(lin['debit']),
                    f2gr(lin['credit']),
                    f2gr(lin['tvalue']),
                    lin['perigrafi'],
                    lin['sxolio'],
                    lin['parastatiko'],
                ]
            )
        data.reverse()
        return headers, aligns, data

    def isozygio_plain(self, apo=None, eos=None) -> dict:
        transactions = self.transactions_filter(apo, eos)
        iso = {}

        for trn in transactions:
            for lin in trn.lines:

                ac_name = lin.account.name

                iso[ac_name] = iso.get(
                    ac_name,
                    {'tvalue': 0, 'tdebit': 0, 'tcredit': 0, 'tdelta': 0}
                )

                isn = iso[ac_name]
                isn['tvalue'] += lin.value
                isn['tdebit'] += lin.debit
                isn['tcredit'] += lin.credit
                isn['tdelta'] += lin.delta

        return iso

    def isozygio_tree(self, apo=None, eos=None) -> dict:
        fis = {}

        for acc, vls in self.isozygio_plain(apo, eos).items():
            objacc = self.chart.get_account(acc)

            if not objacc:
                raise ValueError(
                    f"Account {acc} not fount in chart of accounts")

            for rac in objacc.tree:

                fis[rac] = fis.get(
                    rac,
                    {'tvalue': 0, 'tdebit': 0, 'tcredit': 0, 'tdelta': 0}
                )

                isn = fis[rac]
                isn['tvalue'] = round(vls['tvalue'] + isn['tvalue'], 2)
                isn['tdebit'] = round(vls['tdebit'] + isn['tdebit'], 2)
                isn['tcredit'] = round(vls['tcredit'] + isn['tcredit'], 2)
                isn['tdelta'] = round(vls['tdelta'] + isn['tdelta'], 2)
        return fis

    def model_isozygio(self, apo=None, eos=None) -> tuple:
        headers = ['Λογαριασμός', 'Χρέωση', 'Πίστωση', 'Υπόλοιπο']
        aligns = [1, 3, 3, 3]
        data = []
        for key, v in sorted(self.isozygio_tree(apo, eos).items()):
            data.append(
                [
                    key,
                    f2gr(v['tdebit']),
                    f2gr(v['tcredit']),
                    f2gr(v['tvalue'])
                ]
            )
        return headers, aligns, data

    @property
    def is_balanced(self) -> bool:
        for trn in self.transactions.values():
            if not trn.is_balanced:
                raise ValueError(f'Transaction {trn} is not balanced')
        return True

    def add_transaction(self, transaction: Transaction) -> int:
        self._last_id += 1
        transaction.set_id(self._last_id)
        self.transactions[self._last_id] = transaction
        return self._last_id

    def get_transaction(self, idv) -> Optional[Transaction]:
        return self.transactions.get(idv, None)
