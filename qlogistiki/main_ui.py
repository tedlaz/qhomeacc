# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateEdit,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSplitter,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1004, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fr1_top = QFrame(self.centralwidget)
        self.fr1_top.setObjectName(u"fr1_top")
        self.fr1_top.setMaximumSize(QSize(16777215, 30))
        self.fr1_top.setFrameShape(QFrame.NoFrame)
        self.fr1_top.setFrameShadow(QFrame.Plain)
        self.fr1_top.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.fr1_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_4.addWidget(self.fr1_top, 0, Qt.AlignLeft)

        self.fr2_main = QFrame(self.centralwidget)
        self.fr2_main.setObjectName(u"fr2_main")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr2_main.sizePolicy().hasHeightForWidth())
        self.fr2_main.setSizePolicy(sizePolicy)
        self.fr2_main.setFrameShape(QFrame.NoFrame)
        self.fr2_main.setFrameShadow(QFrame.Plain)
        self.fr2_main.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.fr2_main)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.fr2_main)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setLineWidth(2)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)
        self.fr_left = QFrame(self.splitter)
        self.fr_left.setObjectName(u"fr_left")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fr_left.sizePolicy().hasHeightForWidth())
        self.fr_left.setSizePolicy(sizePolicy2)
        self.fr_left.setMaximumSize(QSize(16777215, 16777215))
        self.fr_left.setFrameShape(QFrame.NoFrame)
        self.fr_left.setFrameShadow(QFrame.Plain)
        self.fr_left.setLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.fr_left)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tbl_isozygio = QTableView(self.fr_left)
        self.tbl_isozygio.setObjectName(u"tbl_isozygio")
        self.tbl_isozygio.setMinimumSize(QSize(0, 0))
        self.tbl_isozygio.setBaseSize(QSize(0, 0))
        self.tbl_isozygio.setFrameShape(QFrame.NoFrame)
        self.tbl_isozygio.setFrameShadow(QFrame.Plain)
        self.tbl_isozygio.setLineWidth(0)
        self.tbl_isozygio.setAlternatingRowColors(True)
        self.tbl_isozygio.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_isozygio.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_isozygio.setShowGrid(False)
        self.tbl_isozygio.setGridStyle(Qt.NoPen)
        self.tbl_isozygio.setCornerButtonEnabled(False)
        self.tbl_isozygio.horizontalHeader().setStretchLastSection(False)
        self.tbl_isozygio.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.tbl_isozygio)

        self.splitter.addWidget(self.fr_left)
        self.fr_right = QFrame(self.splitter)
        self.fr_right.setObjectName(u"fr_right")
        self.fr_right.setFrameShape(QFrame.NoFrame)
        self.fr_right.setFrameShadow(QFrame.Plain)
        self.fr_right.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.fr_right)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lbl_account = QLabel(self.fr_right)
        self.lbl_account.setObjectName(u"lbl_account")
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.lbl_account.setFont(font)
        self.lbl_account.setLineWidth(0)

        self.verticalLayout_2.addWidget(self.lbl_account, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.tbl_kartella = QTableView(self.fr_right)
        self.tbl_kartella.setObjectName(u"tbl_kartella")
        self.tbl_kartella.setMinimumSize(QSize(10, 0))
        self.tbl_kartella.setFrameShape(QFrame.NoFrame)
        self.tbl_kartella.setFrameShadow(QFrame.Plain)
        self.tbl_kartella.setLineWidth(0)
        self.tbl_kartella.setAlternatingRowColors(True)
        self.tbl_kartella.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_kartella.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_kartella.setShowGrid(False)
        self.tbl_kartella.setGridStyle(Qt.NoPen)
        self.tbl_kartella.setCornerButtonEnabled(False)
        self.tbl_kartella.horizontalHeader().setStretchLastSection(False)
        self.tbl_kartella.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tbl_kartella)

        self.gr_view = QChartView(self.fr_right)
        self.gr_view.setObjectName(u"gr_view")
        self.gr_view.setMinimumSize(QSize(0, 200))
        self.gr_view.setMaximumSize(QSize(16777215, 200))
        self.gr_view.setFrameShape(QFrame.NoFrame)
        self.gr_view.setFrameShadow(QFrame.Plain)
        self.gr_view.setLineWidth(0)

        self.verticalLayout_2.addWidget(self.gr_view)

        self.splitter.addWidget(self.fr_right)

        self.verticalLayout_3.addWidget(self.splitter)


        self.verticalLayout_4.addWidget(self.fr2_main)

        self.fr3_bottom = QFrame(self.centralwidget)
        self.fr3_bottom.setObjectName(u"fr3_bottom")
        self.fr3_bottom.setMaximumSize(QSize(16777215, 30))
        self.fr3_bottom.setFrameShape(QFrame.NoFrame)
        self.fr3_bottom.setFrameShadow(QFrame.Plain)
        self.fr3_bottom.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.fr3_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_open = QPushButton(self.fr3_bottom)
        self.btn_open.setObjectName(u"btn_open")

        self.horizontalLayout_2.addWidget(self.btn_open, 0, Qt.AlignLeft|Qt.AlignBottom)

        self.date_filter = QDateEdit(self.fr3_bottom)
        self.date_filter.setObjectName(u"date_filter")
        self.date_filter.setEnabled(False)
        self.date_filter.setMaximumSize(QSize(100, 16777215))
        self.date_filter.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.date_filter)

        self.chk_filter_enable = QCheckBox(self.fr3_bottom)
        self.chk_filter_enable.setObjectName(u"chk_filter_enable")
        self.chk_filter_enable.setMaximumSize(QSize(20, 16777215))
        self.chk_filter_enable.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_2.addWidget(self.chk_filter_enable)

        self.btn_check_rest = QPushButton(self.fr3_bottom)
        self.btn_check_rest.setObjectName(u"btn_check_rest")

        self.horizontalLayout_2.addWidget(self.btn_check_rest, 0, Qt.AlignRight)


        self.verticalLayout_4.addWidget(self.fr3_bottom, 0, Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbl_account.setText(QCoreApplication.translate("MainWindow", u":)", None))
        self.btn_open.setText(QCoreApplication.translate("MainWindow", u"open", None))
        self.chk_filter_enable.setText("")
        self.btn_check_rest.setText(QCoreApplication.translate("MainWindow", u"\u0388\u03bb\u03b5\u03b3\u03c7\u03bf\u03c2 \u03c5\u03c0\u03bf\u03bb\u03bf\u03af\u03c0\u03c9\u03bd", None))
    # retranslateUi
