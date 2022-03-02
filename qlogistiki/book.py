from datetime import date

from .account import LogistikoSxedio
from .transaction import Transaction


class Book:

    def __init__(self, name, lsx: LogistikoSxedio):
        self.name: str = name
        self.chart: LogistikoSxedio = lsx
        self.transactions: dict[int, Transaction] = {}  # {id: Transaction}

    def transactions_filter(self, apo=None, eos=None):
        for transaction in self.transactions.values():
            if apo and transaction.date < date.fromisoformat(apo):
                continue
            if eos and transaction.date > date.fromisoformat(eos):
                continue
            yield transaction

    def kartella(self, account_name: str, apo=None, eos=None):
        tvalue = tdebit = tcredit = tdelta = 0
        lines = []
        transactions = self.transactions_filter(apo, eos)
        for trn in sorted(transactions):
            for line in trn.lines_full_filtered(account_name):

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

    def isozygio_plain(self, apo=None, eos=None):

        transactions = self.transactions_filter(apo, eos)

        iso = {}

        for trn in transactions:

            for lin in trn.lines:
                ac_name = lin.account.name
                iso[ac_name] = iso.get(
                    ac_name, {'tvalue': 0, 'tdebit': 0, 'tcredit': 0, 'tdelta': 0})
                isn = iso[ac_name]
                isn['tvalue'] += lin.value
                isn['tdebit'] += lin.debit
                isn['tcredit'] += lin.credit
                isn['tdelta'] += lin.delta

        return iso

    def isozygio(self, apo=None, eos=None):

        fis = {}

        for acc, vls in self.isozygio_plain(apo, eos).items():

            objacc = self.chart.account(acc)

            for rac in objacc.tree:

                fis[rac] = fis.get(
                    rac, {'tvalue': 0, 'tdebit': 0, 'tcredit': 0, 'tdelta': 0})

                isn = fis[rac]
                isn['tvalue'] = round(vls['tvalue'] + isn['tvalue'], 2)
                isn['tdebit'] = round(vls['tdebit'] + isn['tdebit'], 2)
                isn['tcredit'] = round(vls['tcredit'] + isn['tcredit'], 2)
                isn['tdelta'] = round(vls['tdelta'] + isn['tdelta'], 2)

        return fis

    @property
    def is_balanced(self):

        for trn in self.transactions.values():

            if not trn.is_balanced:
                raise ValueError(f'Transaction {trn} is not balanced')

        return True

    def add_transaction(self, idv, transaction: Transaction):
        assert idv not in self.transactions.keys()
        self.transactions[idv] = transaction

    def get_transaction(self, idv) -> Transaction:
        try:
            return self.transactions[idv]
        except KeyError:
            raise KeyError(f'transaction key No:{idv} does not exist')

    def results(self, apo, eos) -> float:
        return 0
