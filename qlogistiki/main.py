import os
import sys

from PySide6 import QtCore, QtGui, QtPrintSupport, QtWidgets

from .main_ui import Ui_MainWindow
from .model import Model
from .parser_text import parse


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = QtCore.QSettings()
        self.book_path = str(self.settings.value("filename", defaultValue=''))
        self.book = None
        self.checked_account = ''
        self.btn_open.clicked.connect(self.handle_btn_open)
        self.tbl_kartella.doubleClicked.connect(self.show_arthro)
        if self.book_path:
            self.open_book(self.book_path)

    def show_arthro(self, val):
        # fixed_font = qg.QFontDatabase.systemFont(qg.QFontDatabase.FixedFont)
        num = val.sibling(val.row(), 0).data()
        tr1 = self.book.get_transaction(int(num))
        msb = QtWidgets.QMessageBox()
        # font = QtWidgets.QFont()
        # font.setFamily("Courier")
        # msb.setFont(font)
        msb.setWindowTitle(f"Άρθρο: {num}")
        msb.setText(str(tr1))
        msb.show()
        returnValue = msb.exec()

    def handle_btn_open(self):
        opt = QtWidgets.QFileDialog.Option.DontResolveSymlinks | QtWidgets.QFileDialog.Option.ShowDirsOnly
        book_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open", self.book_path, opt)
        if not book_path:
            return
        self.settings.setValue("filename", book_path)
        self.open_book(book_path)

    def open_book(self, book_path):
        self.book = parse(book_path)
        self.tbl_isozygio.setModel(Model(self.book.model_isozygio()))
        self.tbl_isozygio.resizeColumnsToContents()
        self.tbl_isozygio.resizeRowsToContents()
        twi = sum([self.tbl_isozygio.columnWidth(i) for i in range(5)]) + 30
        self.fr_left.setMaximumWidth(twi)
        selection = self.tbl_isozygio.selectionModel()
        selection.selectionChanged.connect(self.refresh_kartella_model)
        self.tbl_kartella.setModel(None)
        self.lbl_account.setText('')

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
            self.tbl_kartella.setStyleSheet(
                "alternate-background-color: #FFDEE3;")

        elif account.startswith(lgreen_color):
            self.tbl_kartella.setStyleSheet(
                "alternate-background-color: #deffde;")

        elif account.startswith(lblue_color):
            self.tbl_kartella.setStyleSheet(
                "alternate-background-color: #DEF3FF;")

        else:
            self.tbl_kartella.setStyleSheet(
                "alternate-background-color: #CCCCCC;")

    def refresh_kartella_model(self, selected, deselected):
        row = selected.first().topLeft()
        account = row.sibling(row.row(), 0).data()

        if account == self.checked_account:
            return

        self.checked_account = account
        self.lbl_account.setText(account)
        self.set_grid_color(account)
        self.model_lmos = Model(self.book.model_kartella(account))

        self.tbl_kartella.setModel(self.model_lmos)
        self.tbl_kartella.verticalScrollBar().setValue(0)  # reset scrollbar position

        self.tbl_kartella.resizeColumnsToContents()
        for i in range(8):
            if self.tbl_kartella.columnWidth(i) > 300:
                self.tbl_kartella.setColumnWidth(i, 300)
        self.tbl_kartella.resizeRowsToContents()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("qhomeacc")
    # app.setWindowIcon(qg.QIcon('homeacc.png'))
    window = MainWindow()
    window.show()
    app.exec()
