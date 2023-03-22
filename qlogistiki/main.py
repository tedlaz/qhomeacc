import os
import sys
from datetime import date
from faulthandler import is_enabled

from PySide6 import QtCharts, QtCore, QtGui, QtPrintSupport, QtWidgets

from . import date_groups as dgroup
from . import rc_main
from .model import Model
from .parser_text import parse
from .ui_main import Ui_MainWindow
from .utils import f2gr


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = QtCore.QSettings()
        self.book_path = str(self.settings.value("filename", defaultValue=""))
        self.book = None
        self.checked_account = ""
        self.eos = None
        self.selected_account = ""

        today = date.today()
        self.date_filter.setDate(today)

        self.btn_open.clicked.connect(self.handle_btn_open)
        self.tbl_kartella.doubleClicked.connect(self.show_arthro)
        self.chk_filter_enable.clicked.connect(self.apply_date_filter)
        self.date_filter.dateChanged.connect(self.apply_date_filter)
        self.btn_check_rest.clicked.connect(self.validate)
        self.rbminas.clicked.connect(self.rbminas_selected)
        self.rbtrimino.clicked.connect(self.rbtrimino_selected)
        self.rbejamino.clicked.connect(self.rbejamino_selected)
        self.rbetos.clicked.connect(self.rbetos_selected)

        if self.book_path:
            self.open_book(self.book_path)

    def rbminas_selected(self):
        self.plot(self.selected_account, dgroup.date2year_month)

    def rbtrimino_selected(self):
        self.plot(self.selected_account, dgroup.date2trimino)

    def rbejamino_selected(self):
        self.plot(self.selected_account, dgroup.date2ejamino)

    def rbetos_selected(self):
        self.plot(self.selected_account, dgroup.date2year)

    def group_function_selector(self):
        if self.rbminas.isChecked():
            return dgroup.date2year_month
        elif self.rbtrimino.isChecked():
            return dgroup.date2trimino
        elif self.rbejamino.isChecked():
            return dgroup.date2ejamino
        elif self.rbetos.isChecked():
            return dgroup.date2year
        return dgroup.date2year

    def validate(self):
        if not self.book:
            return

        val_array = []
        # checks = len(self.book.validations)
        for val in self.book.validations:
            dat, acc, poso = val
            book_ypoloipo = self.book.ypoloipo(acc, dat)
            if book_ypoloipo != poso:
                val_array.append(
                    (dat, acc, book_ypoloipo, poso, round(book_ypoloipo - poso, 2), "🛑")
                )
            else:
                val_array.append(
                    (dat, acc, book_ypoloipo, poso, round(book_ypoloipo - poso, 2), "👍")
                )

        fst = (
            "<style>table, td, th {border: 1px solid black;text-align: right;padding: 5px; border-collapse: collapse;}</style>"
            "<table><tr><th>Ημ/νία</th><th>Λογ/μός</th><th>Ποσό</th><th>Έλεγχος</th><th>Διαφ.</th><th></th></tr>"
        )
        for lin in val_array:
            fst += f"<tr><td>{lin[0]}</td><td>{lin[1]}</td><td>{f2gr(lin[2])}</td><td>{f2gr(lin[3])}</td><td>{f2gr(lin[4])}</td><td>{lin[5]}</td></tr>"
        fst += "</table>"
        QtWidgets.QMessageBox.information(self, "Ελεγχος υπολοίπων", fst)
        # return
        # QtWidgets.QMessageBox.information(
        #     self, f'Έλεγχος υπολοίπων', f'Έγιναν {checks} έλεγχοι υπολοίπων\nΌλα καλά 👍')

    def apply_date_filter(self):
        if self.chk_filter_enable.isChecked():
            self.date_filter.setEnabled(True)
            self.eos = self.date_filter.date().toString(QtCore.Qt.ISODate)
            self.tbl_isozygio.setModel(Model(self.book.model_isozygio(eos=self.eos)))
        else:
            self.eos = None
            self.date_filter.setEnabled(False)
            self.tbl_isozygio.setModel(Model(self.book.model_isozygio()))
        self.isozygio2kartella_connection()

    def isozygio2kartella_connection(self):
        selection = self.tbl_isozygio.selectionModel()
        selection.selectionChanged.connect(self.refresh_kartella_model)
        self.tbl_kartella.setModel(None)
        self.gr_view.setVisible(False)
        self.lbl_account.setText("")
        self.checked_account = ""

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
        opt = (
            QtWidgets.QFileDialog.Option.DontResolveSymlinks
            | QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        book_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open", self.book_path, opt
        )
        if not book_path:
            return
        self.open_book(book_path)

    def open_book(self, book_path):
        if not os.path.exists(book_path):
            QtWidgets.QMessageBox.critical(
                self,
                "Υπάρχουν λάθη",
                f"Η διαδρομή \n{book_path}\n δεν είναι προσβάσιμη.",
            )
            return
        book, errors = parse(book_path)
        if errors:
            QtWidgets.QMessageBox.critical(self, "Υπάρχουν λάθη", "\n".join(errors))
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
            self.tbl_kartella.setStyleSheet("alternate-background-color: #FFDEE3;")

        elif account.startswith(lgreen_color):
            self.tbl_kartella.setStyleSheet("alternate-background-color: #deffde;")

        elif account.startswith(lblue_color):
            self.tbl_kartella.setStyleSheet("alternate-background-color: #DEF3FF;")

        else:
            self.tbl_kartella.setStyleSheet("alternate-background-color: #CCCCCC;")

    def plot(self, account: str, group_function):
        set0 = QtCharts.QBarSet("n")

        series = QtCharts.QBarSeries()
        series.setBarWidth(1)

        # data = self.book.montly_aggregation(account, self.eos)
        data = self.book.time_series(account, self.group_function_selector())
        ym = []
        vl = []
        if account.startswith(
            ("Ταμείο", "Χρεώστες", "Προμηθευτές", "Πάγια", "Αποθεματικό", "Πιστωτές")
        ):
            for el in data:
                ym.append(el[0])
                set0.append(el[1])
                vl.append(el[1])
        else:
            for el in data:
                ym.append(el[0])
                set0.append(el[2])
                vl.append(el[2])
        series.append(set0)

        if account.startswith(("Εξοδα", "Πιστωτές")):
            set0.setColor(QtGui.QColor(210, 40, 0, 180))
            set0.setBorderColor(QtGui.QColor(210, 40, 0, 180))

        if account.startswith(("Εσοδα", "Χρεώστες")):
            set0.setColor(QtGui.QColor(0, 180, 0, 210))
            set0.setBorderColor(QtGui.QColor(0, 180, 0, 180))

        if account.startswith(("Ταμείο", "Πάγια")):
            set0.setColor(QtGui.QColor(0, 140, 200, 180))
            set0.setBorderColor(QtGui.QColor(0, 140, 200, 180))

        chart = QtCharts.QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        axisX = QtCharts.QBarCategoryAxis()
        axisX.setGridLineVisible(False)
        font = QtGui.QFont()
        font.setPixelSize(8)
        axisX.setLabelsFont(font)
        axisX.append(ym)

        axisY = QtCharts.QValueAxis()
        axisY.setRange(min(min(vl), 0), max(max(vl), 0))
        # axisY.setGridLineVisible(False)
        axisX.setLabelsAngle(270)

        chart.addAxis(axisX, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.gr_view.setChart(chart)
        self.gr_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gr_view.setVisible(True)

    def refresh_kartella_model(self, selected, deselected):
        row = selected.first().topLeft()
        account = row.sibling(row.row(), 0).data()
        self.selected_account = account
        if not self.selected_account:
            return
        if account == self.checked_account:
            return

        self.plot(account, dgroup.date2ejamino)

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
    app.setWindowIcon(QtGui.QIcon(":img/images/homeacc.svg"))
    window = MainWindow()
    window.show()
    app.exec()
