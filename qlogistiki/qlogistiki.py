"""GUI for logistiki"""
import os
import sys

from PySide6 import QtCore as qc
from PySide6 import QtGui as qg
from PySide6 import QtWidgets as qw

from . import data_operations_text as dot


class Dmodel(qc.QAbstractTableModel):
    """
    We pass a dictionary of values as data source
    headers : list of Header titles
    vals    : list of [list of column values]
    align   : list of (1=left, 2=center, 3=right)
    typos   : list of (1=decimal, ...)
    """

    def __init__(self, model_data, parent=None):
        super().__init__(parent)
        self.mdata = model_data

    def set_data(self, model_data):
        self.mdata = model_data
        # self.headers, self.vals, self.align, self.typos, self.siz = model_data

    def rowCount(self, parent):
        return len(self.mdata.values)

    def columnCount(self, parent):
        return len(self.mdata.headers)

    def headerData(self, section, orientation, role):

        if role == qc.Qt.DisplayRole:

            if orientation == qc.Qt.Orientation.Horizontal:
                return self.mdata.headers[section]

            else:
                pass
                # return section + 1

        if role == qc.Qt.TextAlignmentRole:
            return qc.Qt.AlignCenter

    # def index(self, row, column, parent):
    #     return qc.QModelIndex()

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == qc.Qt.DisplayRole:

            if self.mdata.types[index.column()] == 1:
                return str(self.mdata.values[index.row()][index.column()])

            else:
                return self.mdata.values[index.row()][index.column()]

        if role == qc.Qt.TextAlignmentRole:

            if self.mdata.aligns[index.column()] == 1:
                return int(qc.Qt.AlignLeft | qc.Qt.AlignVCenter)

            if self.mdata.aligns[index.column()] == 2:
                return int(qc.Qt.AlignCenter | qc.Qt.AlignVCenter)

            if self.mdata.aligns[index.column()] == 3:
                return int(qc.Qt.AlignRight | qc.Qt.AlignVCenter)


class Dialog(qw.QWidget):
    def __init__(self, filename, book, parent=None):
        super().__init__(parent)
        self.parent1 = parent
        self.book = book
        self.checked_account = ""
        mainlayout = qw.QVBoxLayout(self)
        # self.setLayout(mainlayout)
        hlayout = qw.QHBoxLayout()
        mainlayout.addLayout(hlayout)
        leftv = qw.QVBoxLayout()
        rightv = qw.QSplitter()
        rightv.setOrientation(qc.Qt.Orientation.Vertical)
        hlayout.addLayout(leftv)
        hlayout.addWidget(rightv)

        font = qg.QFont()
        font.setFamily("Arial")

        self.set_isozygio(leftv, font)
        bvalidate = qw.QPushButton("Ελεγχος Λογαριασμών")
        leftv.addWidget(bvalidate)
        self.set_label(rightv)
        self.make_table(rightv, font)
        self.setWindowTitle("Ισοζύγιο Λογαριασμών")
        if self.parent1:
            self.parent1.setWindowTitle(f"Ισοζύγιο Λογαριασμών ({filename})")
        # Connections
        bvalidate.clicked.connect(self.validate_ypoloipa)
        # self.sbar.some_acc_clicked.connect(self.refresh_model)
        self.iso.clicked.connect(self.refresh_model_from_iso)
        self.iso.activated.connect(self.refresh_model_from_iso)
        self.tbl.doubleClicked.connect(self.show_arthro)

    def set_isozygio(self, leftv, font):
        self.iso = qw.QTableView()
        self.iso.setFont(font)
        self.iso.setMaximumWidth(350)
        self.iso.setSelectionBehavior(
            qw.QAbstractItemView.SelectionBehavior.SelectRows)
        self.iso.setSelectionMode(
            qw.QAbstractItemView.SelectionMode.SingleSelection)
        self.iso.setModel(Dmodel(self.book.isozygio_model()))
        self.iso.resizeColumnsToContents()
        self.iso.resizeRowsToContents()
        leftv.addWidget(self.iso)

    def set_label(self, rightv):
        self.lbl = qw.QLabel(rightv)
        self.lbl.setAlignment(qc.Qt.AlignCenter)
        bold_font = qg.QFont()
        bold_font.setFamily("Arial")
        bold_font.setBold(True)
        bold_font.setPointSize(16)
        bold_font.setWeight(qg.QFont.Bold)
        self.lbl.setFont(bold_font)
        self.lbl.setMaximumHeight(25)

    def make_table(self, rightv, font):
        self.tbl = qw.QTableView(rightv)
        self.tbl.setFont(font)
        self.tbl.setWordWrap(True)
        self.tbl.setAlternatingRowColors(True)
        # self.tbl.horizontalHeader().setStretchLastSection(True)
        self.tbl.setSelectionBehavior(
            qw.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl.setSelectionMode(
            qw.QAbstractItemView.SelectionMode.SingleSelection)

    def show_arthro(self, val):
        # fixed_font = qg.QFontDatabase.systemFont(qg.QFontDatabase.FixedFont)
        num = val.sibling(val.row(), 0).data()
        tr1 = self.book.get_transaction(num)
        msb = qw.QMessageBox()
        font = qg.QFont()
        font.setFamily("Courier")
        msb.setFont(font)
        msb.setWindowTitle(f"Άρθρο: {num}")
        msb.setText(tr1.as_str())
        msb.show()
        returnValue = msb.exec()
        # qw.QMessageBox.information(self, f"Αρθρο {num}", tr1.as_str())

    def validate_ypoloipa(self):
        correct_no, err, cor = self.book.validate()
        errm = "\n".join(err)
        corm = "\n".join(cor)
        message = f"Number of correct checks: {correct_no}\n"
        message += corm + "\n"
        if err:
            message += f"Errors:\n{errm}"
        else:
            message += "No errors :-)"
        qw.QMessageBox.about(self, "Validations", message)

    def refresh_model_from_iso(self, acc):
        """
        iso means isozygio
        """
        account = acc.sibling(acc.row(), 0).data()
        # Για να μην κάνει refresh όταν επιλέγεται ο ίδιος λογαριασμός
        if account == self.checked_account:
            return
        self.checked_account = account
        self.set_grid_color(account)
        self.refresh_model(account)

    def set_grid_color(self, account):
        lred_color = (
            "Εξοδα",
            "Αγορές",
            "Προμηθευτές",
            "Πιστωτές",
            "ΦΠΑ",
            "Εργαζόμενοι",
        )
        lgreen_color = ("Πωλήσεις", "Πελάτες", "Εσοδα", "Χρεώστες")
        lblue_color = ("Ταμείο", "Μετρητά")

        if account.startswith(lred_color):
            self.tbl.setStyleSheet("alternate-background-color: #FFDEE3;")

        elif account.startswith(lgreen_color):
            self.tbl.setStyleSheet("alternate-background-color: #deffde;")

        elif account.startswith(lblue_color):
            self.tbl.setStyleSheet("alternate-background-color: #DEF3FF;")

        else:
            self.tbl.setStyleSheet("alternate-background-color: #CCCCCC;")

    def refresh_model(self, lmos):
        self.model_lmos = Dmodel(self.book.kartella_model(lmos))
        self.tbl.setModel(self.model_lmos)
        self.tbl.verticalScrollBar().setValue(0)  # reset scrollbar position
        for i, size in enumerate(self.model_lmos.mdata.sizes):
            self.tbl.setColumnWidth(i, size)
        # self.tbl.resizeColumnsToContents()
        self.tbl.resizeRowsToContents()
        self.lbl.setText(f"{lmos}")


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(qc.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.settings = qc.QSettings()
        self.setMinimumSize(1300, 700)
        self.createMenus()
        self.fnam = self.get_filename()

    def get_filename(self):
        filename = str(self.settings.value("filename", defaultValue=''))
        if filename:
            if os.path.isfile(filename):
                book, err = dot.load_from_text(filename)
                if book:
                    self.init_vals(filename, book)
                    return filename
                else:
                    msg = f'file {filename} has errors:\n{err}'
                    qw.QMessageBox.critical(self, "Book Error", msg)
            else:
                self.setWindowTitle(f"Το {filename} δεν είναι διαθέσιμο")
        return ''

    def init_vals(self, filename, book):
        self.dlg = Dialog(filename, book, self)
        self.setCentralWidget(self.dlg)

    def createMenus(self):
        self.openAct = qg.QAction("Open", self)
        self.openAct.triggered.connect(self.open)
        self.filemenu = self.menuBar().addMenu("&File")
        self.filemenu.addAction(self.openAct)

    def open(self):
        fnam, _ = qw.QFileDialog.getOpenFileName(self, "Open", self.fnam, "")
        if fnam:
            self.load_book(fnam)

    def load_book(self, fnam):
        book, err = dot.load_from_text(fnam)
        if book:
            self.init_vals(fnam, book)
            self.settings.setValue("filename", fnam)
        else:
            msg = f'file {fnam} has errors:\n{err}'
            qw.QMessageBox.critical(self, "Book Error", msg)


def main():
    app = qw.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("qlogistiki")
    app.setWindowIcon(qg.QIcon('homeacc.png'))
    dlg = MainWindow()
    dlg.show()
    app.exec()


if __name__ == "__main__":
    main()
