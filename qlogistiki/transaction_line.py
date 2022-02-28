"""Module for Transaction_line"""
from .account import Account
from .utils import f2gr


class TransactionLine:
    __slots__ = ["account", "value", "sxolio"]

    def __init__(self, account: Account, value: float, sxolio: str = ""):
        self.account: Account = account
        self.value: float = round(value, 2)
        self.sxolio = sxolio.strip()

    @property
    def debit(self) -> float:
        if self.value > 0:
            return self.value
        return 0.0

    @property
    def credit(self) -> float:
        if self.value < 0:
            return -self.value
        return 0.0

    @property
    def delta(self) -> float:
        if self.account.is_reverse:
            return -self.value
        return self.value

    @property
    def delta_str(self):
        return f'{self.value:.2}'

    def __eq__(self, other) -> bool:
        return (self.value == other.value) and (self.account.name == other.account.name)

    def __lt__(self, other) -> bool:
        if self.account.name == other.account.name:
            return self.value < other.value
        return self.account.name < other.account.name

    def __mul__(self, number):
        return TransactionLine(self.account, self.value * number)

    def __rmul__(self, number):
        return TransactionLine(self.account, self.value * number)

    def __add__(self, other):
        if self.account.name != other.account.name:
            raise ValueError("For addition accounts must me the same")
        return TransactionLine(self.account, self.value + other.value)

    def __repr__(self) -> str:
        return (
            "TransactionLine(" f"account={self.account!r}, " f"value={self.value!r}" ")"
        )

    def __str__(self) -> str:
        return f"{self.account:<30} {self.sxolio[:30]:<30} {f2gr(self.debit):>14} {f2gr(self.credit):>14}"
