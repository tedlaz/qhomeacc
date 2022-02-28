from .account import LogistikoSxedio
from .transaction import Transaction


class Book:

    def __init__(self, name, lsx: LogistikoSxedio):
        self.name: str = name
        self.chart: LogistikoSxedio = lsx
        self.transactions: dict[int, Transaction] = {}  # {id: Transaction}

    def kartella(self, account_name: str):
        total = 0
        lines = []
        for trn in self.transactions.values():
            for line in trn.lines_full_filtered(account_name):
                total += line['value']
                line['total'] = total
                lines.append(line)
        return lines

    def isozygio(self):
        iso = {}
        for trn in self.transactions.values():
            for lin in trn.lines:
                ac_name = lin.account.name
                iso[ac_name] = round(iso.get(ac_name, 0) + lin.value, 2)
        return iso

    def isozygio_levels(self):
        iso0 = self.isozygio()

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
