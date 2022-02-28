"""Module to parse text accounting books"""
from collections import defaultdict, namedtuple

from .account import Account, LogistikoSxedio, omades_types_gr
from .transaction import Transaction
from .utils import gr2float

ValPoint = namedtuple("ValPoint", "date account delta")
Anoigma = namedtuple("Anoigma", "date account value")
FPA_PREFIX = "ΦΠΑ"


def parse(file):
    """
    Parser for accounting text files
    """
    # trn = Transaction("1000-01-01", "", "", "")
    # Transaction.cid = 0  # Πολύ βασικό γιατι αλλιώς η αρίθμιση έχει θέμα
    lsx = LogistikoSxedio('gr', omades_types_gr)
    dat = ""
    company_afm = ""
    company_name = ""
    transactions = []
    validations = []
    anoigma = []
    valid_accounts = set()
    accounts = defaultdict(float)
    tran_total = 0

    with open(file, encoding='utf8') as fil:
        lines = fil.read().split("\n")

    for line in lines:
        rline = line.rstrip()

        # Αγνόησε τις κενές γραμμές
        if len(rline) == 0:
            continue

        # Αγνόησε τις γραμμές σχολίων
        elif rline.startswith("#"):
            continue

        # Στοιχεία εταιρείας (ΑΦΜ, Επωνυμία)
        elif rline.startswith("$"):
            _, co_afm, *co_name = rline.split()
            company_afm = co_afm
            company_name = " ".join(co_name)

        # Λογαριασμοί ισχύοντες
        elif rline.startswith('+'):
            _, valid_account = rline.split()
            valid_accounts.add(valid_account)

        # Λογαριασμοί που καταργούνται
        elif rline.startswith('-'):
            _, account2remove = rline.split()
            valid_accounts.remove(account2remove)

        # Εγγραφές ανοίγματος
        elif rline.startswith("<"):
            _, adate, accounta, value = rline.split()
            anoigma.append(Anoigma(adate, accounta, gr2float(value)))

        # Γραμμή επιβεβαίωσης υπολοίπου
        elif rline.startswith(("@")):
            # @ 2020-05-10 Αγορές.Εμπορευμάτων.εσωτερικού -120,32
            _, cdat, cacc, cval = rline.split()
            validations.append(ValPoint(cdat, cacc, gr2float(cval)))

        # Γραμμή Head (Ημερομηνία EEEE-MM-DD γίνεται EEEEMMDD αριθμητικό)
        elif rline[:10].replace("-", "").isnumeric():
            # if status == LINE:
            #     self.add_transaction(trn)
            try:
                dat, par, _, per, *afma = rline.split('"')
            except:
                raise ValueError(f"Error parsing line: {rline}")
            dat = dat.strip()
            par = par.strip()
            per = per.strip()
            # afm = afma[0].strip() if afma else ""
            trn = Transaction(dat, par, per)  # , afm)
            transactions.append(trn)
            tran_total = 0

        # Γραμμή λεπτομέρειας
        elif rline[:2] == "  ":  # Line detail
            accval, *sxolio = rline.split("#")
            sxolio = sxolio[0].strip() if sxolio else ""
            account, *txtval = accval.split()
            val = gr2float(txtval[0]) if txtval else 0
            if account not in valid_accounts:
                raise ValueError(f"Invalid account: {account}, date: {dat}")
            if val:
                trn.add_line(Account(account, lsx), val, sxolio)
                tran_total += val
            else:
                val = -tran_total
                trn.add_last_line(Account(account, lsx), sxolio)
            accounts[account] += val
        else:  # Υπάρχουν γραμμές που ξεκινούν με μη αποδεκτό χαρακτήρα
            pass
    return company_afm, company_name, transactions, validations, accounts, anoigma
