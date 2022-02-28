from . import transaction as trn

# class HmerologioType:
#     def __init__(self):
#         self.


class Hmerologio:
    def __init__(self):
        self.type = 1
        self.transactions = []

    def add_transaction(self, trans: trn.Transaction):
        self.transactions.append(trans)
