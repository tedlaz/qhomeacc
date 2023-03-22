"""
Συναρτήσεις για την μετατροπή της ημερομηνίας σε text-αριθμό
(Κείμενο που με την function int γίνεται ακέραιος)
"""
from datetime import date


def date2date(dat: date) -> str:
    return dat.isoformat().replace("-", "")


def date2year_month(dat: date) -> str:
    yyy, mmm, _ = dat.isoformat().split("-")
    return f"{yyy[2:]}{mmm}"


def date2year(dat: date) -> str:
    yyy, _, _ = dat.isoformat().split("-")
    return yyy


def date2trimino(dat: date) -> str:
    tri = {
        "01": 1,
        "02": 1,
        "03": 1,
        "04": 2,
        "05": 2,
        "06": 2,
        "07": 3,
        "08": 3,
        "09": 3,
        "10": 4,
        "11": 4,
        "12": 4,
    }
    yyy, mmm, _ = dat.isoformat().split("-")
    return f"{yyy[2:]}{tri[mmm]}"


def date2tetramino(dat: date) -> str:
    tri = {
        "01": 1,
        "02": 1,
        "03": 1,
        "04": 1,
        "05": 2,
        "06": 2,
        "07": 2,
        "08": 2,
        "09": 3,
        "10": 3,
        "11": 3,
        "12": 3,
    }
    yyy, mmm, _ = dat.isoformat().split("-")
    return f"{yyy[2:]}{tri[mmm]}"


def date2ejamino(dat: date) -> str:
    tri = {
        "01": 1,
        "02": 1,
        "03": 1,
        "04": 1,
        "05": 1,
        "06": 1,
        "07": 2,
        "08": 2,
        "09": 2,
        "10": 2,
        "11": 2,
        "12": 2,
    }
    yyy, mmm, _ = dat.isoformat().split("-")
    return f"{yyy[2:]}{tri[mmm]}"
