"""Module for Transaction_line"""
from .account import Account


class TransactionLine:
    __slots__ = ["account", "value", "sxolio"]

    def __init__(self, account_code: str, value: float, sxolio: str = ""):
        self.account = Account(account_code)
        self.value = round(value, 2)
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
        """For compatibility reasons only"""
        return self.value

    def __eq__(self, other) -> bool:
        return (self.value == other.value) and (self.account.name == other.account.name)

    def __lt__(self, other) -> bool:
        if self.account.name == other.account.name:
            return self.value < other.value
        return self.account.name < other.account.name

    def __mul__(self, number):
        return TransactionLine(self.account.name, self.value * number)

    def __rmul__(self, number):
        return TransactionLine(self.account.name, self.value * number)

    def __add__(self, other):
        if self.account.name != other.account.name:
            raise ValueError("For addition accounts must me the same")
        return TransactionLine(self.account.name, self.value + other.value)

    def __repr__(self) -> str:
        return (
            "TransactionLine(" f"account={self.account!r}, " f"value={self.value!r}" ")"
        )

    def __str__(self) -> str:
        return f"{self.account:<30} {self.debit:>14} {self.credit:>14}"
