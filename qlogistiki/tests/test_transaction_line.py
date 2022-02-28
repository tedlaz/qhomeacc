from qlogistiki.account import Account, LogistikoSxedio, account_types
from qlogistiki.transaction_line import TransactionLine


def test_tr001():
    ls1 = LogistikoSxedio('gr', account_types)
    tl1 = TransactionLine(Account("Aa.Bb.Cc", ls1), -100)
    tl2 = TransactionLine(Account("Aa.Bb.Cc", ls1), -100)
    assert tl1 == tl2
    assert tl1.debit == 0
    assert tl1.credit == 100
    assert tl1.delta == -100
    assert tl1 * -2 == TransactionLine(Account("Aa.Bb.Cc", ls1), 200)
    assert 1.5 * tl2 == tl2 * 1.5
