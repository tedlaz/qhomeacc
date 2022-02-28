"""
Class Account
"""
from collections import namedtuple

account_types = {
    '1': 'pagia',
    '2': 'apothemata',
    '3': 'apaitiseis',
    '4': 'kefalaio',
    '5': 'ypoxreoseis',
    '6': 'ejoda',
    '7': 'esoda',
    '8': 'anorgana',
    '54.00': 'fpa'

}


class LogistikoSxedio:

    kats = (
        'pagia',
        'apothemata',
        'apaitiseis',
        'kefalaio',
        'ypoxreoseis',
        'esoda',
        'ejoda',
        'anorgana',
        'fpa'
    )

    def __init__(self, name, types: dict):
        self.name = name
        self.types = types
        assert all([i in self.kats for i in types.values()])
        self.accounts = {}

    def account(self, account_name: str):
        if not account_name.startswith(tuple(self.types.keys())):
            raise ValueError(f'Error account name: {account_name}')
        if account_name not in self.accounts:
            self.accounts[account_name] = Account(account_name, self)
        return self.accounts[account_name]

    def is_valid_account(self, account_name: str) -> bool:
        return account_name in self.accounts.keys()

    def account_type(self, account):
        typs = []
        for acc_start, typ in self.types.items():
            if account.name.startswith(acc_start):
                typs.append(typ)
        return typs

    def __str__(self):
        sta = '\n'.join([str(i) for i in self.accounts.values()])
        return sta


class Account:
    splitter = "."
    __slots__ = [
        'chart',
        "name"
    ]

    def __init__(self, name: str, chart: LogistikoSxedio):
        self.chart: LogistikoSxedio = chart
        self.name = name

    @property
    def is_fpa(self):
        return 'fpa' in self.chart.account_type(self)

    @property
    def is_reverse(self):
        return 'esoda' in self.chart.account_type(self)

    @property
    def name_length(self):
        return len(self.name)

    @property
    def tree(self) -> list:
        spl = self.name.split(self.splitter)
        lvls = [self.splitter.join(spl[: i + 1]) for i, _ in enumerate(spl)]
        return lvls

    @property
    def tree_reversed(self) -> list:
        lvls = self.tree
        lvls.reverse()
        return lvls

    def __repr__(self) -> str:
        return f"Account(name={self.name!r})"

    def __str__(self) -> str:
        return f"{self.name}"

    def __format__(self, format_spec) -> str:
        return f"{self.name:{format_spec}}"


class BookNew:

    def __init__(self, name, trans, lsx: LogistikoSxedio):
        self.name = name
        self.chart = lsx
        self.transactions = trans

    def kartella(self, account_name):
        total = 0
        lines = []
        for trn in self.transactions.values():
            for line in trn.lines_full_filtered(account_name):
                total += line['value']
                line['total'] = total
                lines.append(line)
        return lines
