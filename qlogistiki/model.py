from PySide6 import QtCore as qc


class Model(qc.QAbstractTableModel):
    """
    book_data: (headers, aligns, data)
    headers : list of Header titles
    aligns  : list of (1=left, 2=center, 3=right)
    data    : [val1, val2, ...]
    """

    def __init__(self, book_data, parent=None):
        super().__init__(parent)
        self.set_data(book_data)

    def set_data(self, book_data):
        self.headers, self.aligns, self.rows = book_data

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.headers)

    def headerData(self, section, orientation, role):

        if role == qc.Qt.DisplayRole:

            if orientation == qc.Qt.Orientation.Horizontal:
                return self.headers[section]

        if role == qc.Qt.TextAlignmentRole:
            return qc.Qt.AlignCenter

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == qc.Qt.DisplayRole:
            return str(self.rows[index.row()][index.column()])

        if role == qc.Qt.TextAlignmentRole:

            if self.aligns[index.column()] == 1:
                return int(qc.Qt.AlignLeft | qc.Qt.AlignVCenter)

            if self.aligns[index.column()] == 2:
                return int(qc.Qt.AlignCenter | qc.Qt.AlignVCenter)

            if self.aligns[index.column()] == 3:
                return int(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
