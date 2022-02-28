import qlogistiki.account as acc
import qlogistiki.transaction as trn


def test_new_from_delta():
    cht = acc.LogistikoSxedio('gr', acc.account_types)
    li1 = trn.TransactionLine(acc.Account("Ταμείο", cht), -100.26)
    assert li1.debit == 0
    assert li1.credit == 100.26
    assert li1.value == -100.26
    assert li1.delta == -100.26
    li2 = trn.TransactionLine(acc.Account("Ταμείο", cht), 35.234)
    assert li2.debit == 35.23
    assert li2.credit == 0
    assert li2.value == 35.23
    assert li2.delta == 35.23


def test_transaction_01():
    cht = acc.LogistikoSxedio('gr', acc.account_types)
    tr1 = trn.Transaction("2020-01-10", "", "Σουπερμαρκετ πόπη")
    tr1.add_line(cht.account("20.00.00.024"), 100)
    tr1.add_line(cht.account("54.00.20.024"), 24)
    tr1.add_last_line(cht.account("50.00.00.001"))
    # print('\n', tr1.as_str())
    # print(tr1)
    assert tr1.uid == "202001101240"
    assert tr1.value == 124
    # tr1.afm = "123123123"
    # assert tr1.uid == "2020011012312312312400"
