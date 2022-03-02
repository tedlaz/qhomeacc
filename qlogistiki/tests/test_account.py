from qlogistiki.account import Account, LogistikoSxedio

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


def test_ls1():
    ls1 = LogistikoSxedio('gr', account_types)
    assert ls1.account_type(Account('54.00.00.013', ls1)) == [
        'ypoxreoseis', 'fpa']


def test_acc_tree():
    ls1 = LogistikoSxedio('gr', account_types)
    acc = Account("Aa.Bb.Cc", ls1)
    ls1.account('20.00.00')
    assert acc.tree == ["Aa", "Aa.Bb", "Aa.Bb.Cc"]
    assert acc.tree_reversed == ["Aa.Bb.Cc", "Aa.Bb", "Aa"]


def test_acc_reverse():
    ls1 = LogistikoSxedio('gr', account_types)
    acc = Account("70.01.013", ls1)
