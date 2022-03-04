"""Module Transaction"""
from collections import namedtuple
from datetime import date

from .account import Account
from .transaction_line import TransactionLine
from .utils import f2gr

DEBIT, CREDIT = 1, 2
decr = {1: "Χρέωση", 2: "Πίστωση"}

Trl = namedtuple("Trl", "id date par per acc typos val delta debit credit")


class Hmerologio:
    def __init__(self):
        self.name = ''


class Transaction:
    """
    Class dealing with transactions
    """

    __slots__ = [
        "id",
        "date",
        "parastatiko",
        "perigrafi",
        "lines"
    ]

    def __init__(self, iso_date: str, parastatiko: str, perigrafi: str, idv: int = 0):
        self.id = idv
        self.date: date = date.fromisoformat(iso_date)
        self.parastatiko = parastatiko
        self.perigrafi = perigrafi
        self.lines: list[TransactionLine] = []

    def set_id(self, idv: int):
        if self.id != 0:
            raise ValueError(f"Transaction {self} already has id={self.id}")
        self.id = idv

    def lines_full(self) -> list[Trl]:
        return [
            Trl(
                self.id,
                self.date,
                self.parastatiko,
                self.perigrafi,
                l.account,
                l.sxolio,
                l.value,
                l.delta,
                l.debit,
                l.credit
            )
            for l in self.lines
        ]

    def lines_by_account_name(self, account_name: str) -> list[dict]:
        return [
            {
                'id': self.id,
                'date': self.date,
                'parastatiko': self.parastatiko,
                'perigrafi': self.perigrafi,
                'account': l.account,
                'sxolio': l.sxolio,
                'value': l.value,
                'delta': l.delta,
                'debit': l.debit,
                'credit': l.credit
            }
            for l in self.lines if l.account.name.startswith(account_name)
        ]

    @property
    def rest(self) -> float:
        return round(sum(l.value for l in self.lines), 2)

    @property
    def uid(self) -> str:
        """
        Generate a unique id
        """
        date_part = self.date.isoformat().replace("-", "")
        parastatiko_part = self.parastatiko.replace(" ", "")
        val_part = str(self.total).replace(',', '').replace('.', '')
        return f"{date_part}{parastatiko_part}{val_part}"

    @property
    def is_balanced(self) -> bool:
        if len(self.lines) < 2:
            return False
        if self.rest == 0:
            return True
        return False

    @property
    def total(self):
        return sum(l.debit for l in self.lines)

    @property
    def value(self):
        return sum(l.debit for l in self.lines)

    def get_lines_by_account(self, account_part, running_sum, found):
        """
            If a transaction has more than one lines according to account_part
            group them together as one with theyr sum as value
        """
        for line in self.lines:
            if line.account.name.startswith(account_part):
                if line.sxolio:
                    per = self.perigrafi + ", " + line.sxolio
                else:
                    per = self.perigrafi
                running_sum["total"] += line.value
                found.append(
                    (
                        self.id,
                        self.date,
                        self.parastatiko,
                        per,
                        line.debit,
                        line.credit,
                        running_sum["total"],
                    )
                )

    def add_line(self, account: Account, value: float, sxolio: str = ""):
        new_line = TransactionLine(account, value, sxolio)
        self.lines.append(new_line)

    def add_connected_lines(self, acc1: Account, acc2: Account, value: float, pososto: float):
        self.add_line(acc1, value)
        self.add_line(acc2, value * pososto / 100.0)

    def add_last_line(self, account: Account, sxolio: str = ""):
        if self.rest == 0:
            raise ValueError(f"Transaction {self} is already balanced")
        new_line = TransactionLine(account, -self.rest, sxolio)
        self.lines.append(new_line)

    @property
    def last_account(self) -> Account:
        if len(self.lines) == 0:
            raise ValueError("Impossible value")
        return self.lines[-1].account

    @property
    def last_delta(self):
        if len(self.lines) == 0:
            return 0
        return self.lines[-1].delta

    def __repr__(self) -> str:
        lins = ",".join([repr(lin) for lin in self.lines])
        return (
            "Transaction("
            f"date={self.date!r}, "
            f"parastatiko={self.parastatiko!r}, "
            f"perigrafi={self.perigrafi!r}, "
            f"lines=[{lins}]"
            ")"
        )

    def __str__(self) -> str:
        ast = f"\n{self.date} {self.parastatiko} {self.perigrafi}\n"
        for lin in self.lines:
            ast += f"  {lin}\n"
        return ast

    def __eq__(self, oth):
        return self.date == oth.date and self.parastatiko == oth.parastatiko

    def __lt__(self, oth):
        if self.date == oth.date:
            return self.id < oth.id
        return self.date < oth.date

    def __gt__(self, oth):
        if self.date == oth.date:
            return self.id > oth.id
        return self.date > oth.date

    def html(self):
        fst = (
            '<style>table, td, th {border: 1px solid black;text-align: right;padding: 5px; border-collapse: collapse;}</style>'
            f'<table><tr><th colspan="4"><center>{self.date} {self.parastatiko} {self.perigrafi}</center></th></tr>'
            '<tr><th><center>Λογ/μός</center></th><th><center>Περιγραφή</center></th><th><center>Χρέωση</center></th><th><center>Πίστωση</center></th></tr>'
        )
        for lin in self.lines:
            fst += f'<tr><td align="left">{lin.account.name}</td><td align="left">{lin.sxolio}</td><td>{f2gr(lin.debit)}</td><td>{f2gr(lin.credit)}</td></tr>'
        if len(self.lines) > 2:
            tdebit = f2gr(sum([i.debit for i in self.lines]))
            tcredit = f2gr(sum([i.credit for i in self.lines]))
            fst += f'<tr><th colspan="2"><center>Σύνολα</center></th><th>{tdebit}</th><th>{tcredit}</th></tr>'
        fst += '</table>'
        return fst
