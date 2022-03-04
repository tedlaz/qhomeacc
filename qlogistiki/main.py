import os
import sys
from datetime import date

from PySide6 import QtCharts, QtCore, QtGui, QtPrintSupport, QtWidgets

from . import main_rc
from .main_ui import Ui_MainWindow
from .model import Model
from .parser_text import parse
from .utils import f2gr


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = QtCore.QSettings()
        self.book_path = str(self.settings.value("filename", defaultValue=''))
        self.book = None
        self.checked_account = ''

        today = date.today()
        self.date_filter.setDate(today)

        self.btn_open.clicked.connect(self.handle_btn_open)
        self.tbl_kartella.doubleClicked.connect(self.show_arthro)
        self.chk_filter_enable.clicked.connect(self.apply_date_filter)
        self.date_filter.dateChanged.connect(self.apply_date_filter)
        self.btn_check_rest.clicked.connect(self.validate)

        if self.book_path:
            self.open_book(self.book_path)

    def validate(self):
        if not self.book:
            return

        val_errors = []
        checks = len(self.book.validations)
        for val in self.book.validations:
            dat, acc, poso = val
            book_ypoloipo = self.book.ypoloipo(acc, dat)
            if book_ypoloipo != poso:
                val_errors.append(
                    (dat, acc, book_ypoloipo, poso, round(book_ypoloipo-poso, 2)))
        if val_errors:
            fst = (
                '<style>td, th {border: 1px solid #dddddd;text-align: right;padding: 5px;}</style>'
                '<table><tr><th>Ημ/νία</th><th>Λογ/μός</th><th>Ποσό</th><th>Έλεγχος</th><th>Διαφ.</th></tr>'
            )
            for lin in val_errors:
                fst += f"<tr><td>{lin[0]}</td><td>{lin[1]}</td><td>{f2gr(lin[2])}</td><td>{f2gr(lin[3])}</td><td>{f2gr(lin[4])}</td></tr>"
            fst += "</table>"
            QtWidgets.QMessageBox.critical(
                self, 'Βρέθηκαν λάθη', fst)
            return
        QtWidgets.QMessageBox.information(
            self, f'Έλεγχος υπολοίπων', f'Έγιναν {checks} έλεγχοι υπολοίπων\nΌλα καλά 👍')

    def apply_date_filter(self):
        if self.chk_filter_enable.isChecked():
            self.date_filter.setEnabled(True)
            eos = self.date_filter.date().toString(QtCore.Qt.ISODate)
            self.tbl_isozygio.setModel(
                Model(self.book.model_isozygio(eos=eos)))
        else:
            self.date_filter.setEnabled(False)
            self.tbl_isozygio.setModel(Model(self.book.model_isozygio()))
        self.isozygio2kartella_connection()

    def isozygio2kartella_connection(self):
        selection = self.tbl_isozygio.selectionModel()
        selection.selectionChanged.connect(self.refresh_kartella_model)
        self.tbl_kartella.setModel(None)
        self.gr_view.setVisible(False)
        self.lbl_account.setText('')
        self.checked_account = ''

    def show_arthro(self, val):
        # fixed_font = qg.QFontDatabase.systemFont(qg.QFontDatabase.FixedFont)
        num = val.sibling(val.row(), 0).data()
        tr1 = self.book.get_transaction(int(num))
        msb = QtWidgets.QMessageBox()
        # font = QtWidgets.QFont()
        # font.setFamily("Courier")
        # msb.setFont(font)
        msb.setWindowTitle(f"Άρθρο: {num}")
        msb.setText(tr1.html())
        msb.show()
        returnValue = msb.exec()

    def handle_btn_open(self):
        opt = QtWidgets.QFileDialog.Option.DontResolveSymlinks | QtWidgets.QFileDialog.Option.ShowDirsOnly
        book_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open", self.book_path, opt)
        if not book_path:
            return
        self.open_book(book_path)

    def open_book(self, book_path):
        if not os.path.exists(book_path):
            QtWidgets.QMessageBox.critical(
                self,
                'Υπάρχουν λάθη',
                f'Η διαδρομή \n{book_path}\n δεν είναι προσβάσιμη.'
            )
            return
        book, errors = parse(book_path)
        if errors:
            QtWidgets.QMessageBox.critical(
                self, 'Υπάρχουν λάθη', '\n'.join(errors))
            return
        self.settings.setValue("filename", book_path)
        self.book = book
        self.setWindowTitle(f"{self.book.name} - {book_path}")
        self.tbl_isozygio.setModel(Model(self.book.model_isozygio()))
        self.tbl_isozygio.resizeColumnsToContents()
        self.tbl_isozygio.resizeRowsToContents()
        twi = sum([self.tbl_isozygio.columnWidth(i) for i in range(5)]) + 30
        self.fr_left.setMaximumWidth(twi)
        self.isozygio2kartella_connection()

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

    def plot(self, account):
        series = QtCharts.QLineSeries()
        data = self.book.time_series(account)
        if account.startswith(('Ταμείο', 'Χρεώστες', 'Προμηθευτές', 'Πάγια', 'Αποθεματικό')):
            for el in data:
                timestamp = float(el[0].isoformat().replace('-', ''))
                # timestamp = time.mktime(el[0].timetuple())
                series.append(timestamp, el[1])
        else:
            for el in data:
                timestamp = float(el[0].isoformat().replace('-', ''))
                series.append(timestamp, el[2])

        chart = QtCharts.QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle(account)
        self.gr_view.setChart(chart)
        self.gr_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gr_view.setVisible(True)
        # print(self.book.time_series(account))

    def refresh_kartella_model(self, selected, deselected):
        row = selected.first().topLeft()
        account = row.sibling(row.row(), 0).data()

        if account == self.checked_account:
            return

        self.plot(account)

        self.checked_account = account
        self.set_grid_color(account)

        if self.chk_filter_enable.isChecked():
            eos = self.date_filter.date().toString(QtCore.Qt.ISODate)
            self.lbl_account.setText(f"{account} έως {eos}")
            self.model_lmos = Model(self.book.model_kartella(account, eos=eos))
        else:
            self.lbl_account.setText(account)
            self.model_lmos = Model(self.book.model_kartella(account))

        self.tbl_kartella.setModel(self.model_lmos)
        self.tbl_kartella.verticalScrollBar().setValue(0)  # reset scrollbar position

        self.tbl_kartella.resizeColumnsToContents()
        for i in range(8):
            if self.tbl_kartella.columnWidth(i) > 700:
                self.tbl_kartella.setColumnWidth(i, 700)
        self.tbl_kartella.resizeRowsToContents()


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("qhomeacc")
    app.setWindowIcon(QtGui.QIcon(':img/images/homeacc.svg'))
    window = MainWindow()
    window.show()
    app.exec()
