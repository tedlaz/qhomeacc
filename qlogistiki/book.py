from datetime import date
from typing import Optional

from .account import LogistikoSxedio
from .transaction import Transaction
from .utils import days_list, f2gr, isodate2ym, months_between_ym


class Book:
    def __init__(self, name, lsx: LogistikoSxedio):
        self.name: str = name
        self.chart: LogistikoSxedio = lsx
        self.transactions: dict[int, Transaction] = {}  # {id: Transaction}
        self.validations = []
        self._last_id = 0

    def transactions_filter(self, apo=None, eos=None):
        for transaction in self.transactions.values():
            if apo and transaction.date < date.fromisoformat(apo):
                continue

            if eos and transaction.date > date.fromisoformat(eos):
                continue

            yield transaction

    def ypoloipo(self, account_name: str, eos=None) -> float:
        transactions = self.transactions_filter(eos=eos)
        ypoloipo = 0
        for trn in sorted(transactions):
            for line in trn.lines_by_account_name(account_name):
                ypoloipo += line["value"]
        return round(ypoloipo, 2)

    def montly_aggregation(self, account_name, eos=None):
        transactions = self.transactions_filter(eos=eos)
        ymv = {}
        total = 0
        final = []
        for trn in transactions:
            for line in trn.lines_by_account_name(account_name):
                year, month, _ = line["date"].isoformat().split("-")
                year_month = f"{year}{month}"
                ymv[year_month] = round(ymv.get(year_month, 0) + line["delta"], 2)
        apon = min(ymv.keys())
        eosn = max(ymv.keys())
        if self.ypoloipo(account_name, eos):
            eosn = isodate2ym(date.today().isoformat())
            if eos:
                eosn = isodate2ym(eos)
        ym_list = months_between_ym(apon, eosn)
        for ym in ym_list:
            total += round(ymv.get(ym, 0), 2)
            final.append((ym, total, ymv.get(ym, 0)))
        return final

    # def time_series(self, account_name, eos=None):
    #     total = 0
    #     # lines = []
    #     ldir = {}
    #     sdir = {}
    #     transactions = self.transactions_filter(eos=eos)
    #     strans = sorted(transactions)

    #     final = []

    #     min_date = date(2099, 12, 31)
    #     max_date = date(1900, 1, 1)
    #     for trn in strans:
    #         for line in trn.lines_by_account_name(account_name):
    #             if line["date"] < min_date:
    #                 min_date = line["date"]
    #             if line["date"] > max_date:
    #                 max_date = line["date"]
    #             ldir[line["date"]] = ldir.get(line["date"], 0) + line["delta"]
    #             sdir[line["date"]] = round(sdir.get(line["date"], 0) + line["delta"], 2)

    #     dlist = days_list(min_date, max_date)

    #     for day in dlist:
    #         total += round(ldir.get(day, 0), 2)
    #         final.append((day, total, sdir.get(day, 0)))

    #     return final

    def acclines(self, account_name, apo=None, eos=None):
        transactions = self.transactions_filter(apo=apo, eos=eos)
        strans = sorted(transactions)
        res = []
        for trn in strans:
            for line in trn.lines_by_account_name(account_name):
                res.append(line)
        return res

    def time_series(self, account_name, groupfn, apo=None, eos=None):
        ldir = {}
        sdir = {}
        res = self.acclines(account_name, apo=apo, eos=eos)
        if not res:
            return
        first_date = res[0]["date"]
        last_date = res[-1]["date"]
        for line in res:
            date_a = groupfn(line["date"])
            ldir[date_a] = ldir.get(date_a, 0) + line["delta"]
            sdir[date_a] = round(sdir.get(date_a, 0) + line["delta"], 2)

        flist = days_list(first_date, last_date)
        dlist = list({groupfn(i) for i in flist})
        dlist.sort()
        total = 0
        final = []
        for day in dlist:
            total += round(ldir.get(day, 0), 2)
            final.append((day, total, sdir.get(day, 0)))

        return final

    def kartella(self, account_name: str, apo=None, eos=None) -> list:
        tvalue = tdebit = tcredit = tdelta = 0
        lines = []

        transactions = self.transactions_filter(apo, eos)

        for trn in sorted(transactions):
            for line in trn.lines_by_account_name(account_name):
                tvalue += line["value"]
                line["tvalue"] = tvalue

                tdebit += line["debit"]
                line["tdebit"] = tdebit

                tcredit += line["credit"]
                line["tcredit"] = tcredit

                tdelta += line["delta"]
                line["tdelta"] = tdelta

                lines.append(line)

        return lines

    def model_kartella(self, account_name: str, apo=None, eos=None):
        lines = self.kartella(account_name, apo, eos)
        headers = [
            "Νο",
            "Ημ/νία",
            "Χρέωση",
            "Πίστωση",
            "Υπόλοιπο",
            "Περιγραφή",
            "Σχόλιο",
            "Παρ/κό",
            "d",
        ]
        aligns = [3, 1, 3, 3, 3, 1, 1, 1, 3]
        data = []
        for lin in lines:
            data.append(
                [
                    lin["id"],
                    lin["date"],
                    f2gr(lin["debit"]),
                    f2gr(lin["credit"]),
                    f2gr(lin["tvalue"]),
                    lin["perigrafi"],
                    lin["sxolio"],
                    lin["parastatiko"],
                    lin["delta"],
                ]
            )
        data.reverse()
        return headers, aligns, data

    def isozygio_plain(self, apo=None, eos=None) -> dict:
        transactions = self.transactions_filter(apo, eos)
        iso = {}

        for trn in transactions:
            for lin in trn.lines:
                ac_name = lin.account.name

                iso[ac_name] = iso.get(
                    ac_name, {"tvalue": 0, "tdebit": 0, "tcredit": 0, "tdelta": 0}
                )

                isn = iso[ac_name]
                isn["tvalue"] += lin.value
                isn["tdebit"] += lin.debit
                isn["tcredit"] += lin.credit
                isn["tdelta"] += lin.delta

        return iso

    def isozygio_tree(self, apo=None, eos=None) -> dict:
        fis = {}

        for acc, vls in self.isozygio_plain(apo, eos).items():
            objacc = self.chart.get_account(acc)

            if not objacc:
                raise ValueError(f"Account {acc} not fount in chart of accounts")

            for rac in objacc.tree:
                fis[rac] = fis.get(
                    rac, {"tvalue": 0, "tdebit": 0, "tcredit": 0, "tdelta": 0}
                )

                isn = fis[rac]
                isn["tvalue"] = round(vls["tvalue"] + isn["tvalue"], 2)
                isn["tdebit"] = round(vls["tdebit"] + isn["tdebit"], 2)
                isn["tcredit"] = round(vls["tcredit"] + isn["tcredit"], 2)
                isn["tdelta"] = round(vls["tdelta"] + isn["tdelta"], 2)
        return fis

    def model_isozygio(self, apo=None, eos=None) -> tuple:
        # 'Χρέωση', 'Πίστωση', 'Υπόλοιπο']
        headers = ["Λογαριασμός", "Υπόλοιπο"]
        aligns = [1, 3]  # , 3, 3]
        data = []
        for key, v in sorted(self.isozygio_tree(apo, eos).items()):
            data.append(
                [
                    key,
                    # f2gr(v['tdebit']),
                    # f2gr(v['tcredit']),
                    f2gr(v["tvalue"]),
                ]
            )
        return headers, aligns, data

    @property
    def is_balanced(self) -> bool:
        for trn in self.transactions.values():
            if not trn.is_balanced:
                raise ValueError(f"Transaction {trn} is not balanced")
        return True

    def add_transaction(self, transaction: Transaction) -> int:
        self._last_id += 1
        transaction.set_id(self._last_id)
        self.transactions[self._last_id] = transaction
        return self._last_id

    def get_transaction(self, idv) -> Optional[Transaction]:
        return self.transactions.get(idv, None)

    def add_validation(self, validation):
        self.validations.append(validation)
