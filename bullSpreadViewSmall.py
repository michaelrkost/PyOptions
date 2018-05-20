# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bullSpreadViewSmall.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
# todo change the name of this module from bullSpreadViewSmall to QTmgnt or something
# todo use return key to activate "Qualify Contracts"

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from ib_insync import *

# need to give QT the async from ib_insync
util.useQt()

# Option management class for PyOptions - mrk
import optionSpreadsClass

from localUtilities import errorHandler, configIB, buildOptionMatrices, dateUtils, logger

class Ui_MainPyOptionsWindow(object):
    """
    an_option_spread is the created option spread
    """
    def __init__(self):
        self.ib = IB()
        self.ib.setCallback('error', errorHandler.onError)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< def setup Ui      -- goes here:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def setupUi(self, MainPyOptionsWindow):
        MainPyOptionsWindow.setObjectName("MainPyOptionsWindow")
        MainPyOptionsWindow.resize(963, 838)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/icons/ib.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainPyOptionsWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainPyOptionsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_Contracts = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Contracts.setGeometry(QtCore.QRect(0, 60, 951, 691))
        self.tabWidget_Contracts.setObjectName("tabWidget_Contracts")
        self.qualifyContracts_tab = QtWidgets.QWidget()
        self.qualifyContracts_tab.setObjectName("qualifyContracts_tab")
        self.groupBox_2 = QtWidgets.QGroupBox(self.qualifyContracts_tab)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 291, 261))
        self.groupBox_2.setObjectName("groupBox_2")
        self.qualifyContracts = QtWidgets.QPushButton(self.groupBox_2)
        self.qualifyContracts.setGeometry(QtCore.QRect(160, 220, 111, 23))
        self.qualifyContracts.setObjectName("qualifyContracts")
        self.splitter = QtWidgets.QSplitter(self.groupBox_2)
        self.splitter.setGeometry(QtCore.QRect(20, 30, 185, 17))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.radioButton_Index = QtWidgets.QRadioButton(self.splitter)
        self.radioButton_Index.setChecked(True)
        self.radioButton_Index.setObjectName("radioButton_Index")
        self.radioButton_Stock = QtWidgets.QRadioButton(self.splitter)
        self.radioButton_Stock.setObjectName("radioButton_Stock")
        self.radioButton_Option = QtWidgets.QRadioButton(self.splitter)
        self.radioButton_Option.setObjectName("radioButton_Option")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(17, 81, 250, 50))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.labelExchange = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.labelExchange.setFont(font)
        self.labelExchange.setWhatsThis("")
        self.labelExchange.setObjectName("labelExchange")
        self.gridLayout.addWidget(self.labelExchange, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.underlyingText = QtWidgets.QLineEdit(self.layoutWidget)
        self.underlyingText.setObjectName("underlyingText")
        self.gridLayout.addWidget(self.underlyingText, 1, 0, 1, 1)
        self.comboBoxExchange = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBoxExchange.setToolTip("")
        self.comboBoxExchange.setObjectName("comboBoxExchange")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.comboBoxExchange.addItem("")
        self.gridLayout.addWidget(self.comboBoxExchange, 1, 1, 1, 1)
        self.comboBox_Expiry = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.comboBox_Expiry.setFont(font)
        self.comboBox_Expiry.setObjectName("comboBox_Expiry")
        self.gridLayout.addWidget(self.comboBox_Expiry, 1, 2, 1, 1)
        self.groupBox_StrikePrice = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_StrikePrice.setGeometry(QtCore.QRect(17, 140, 251, 51))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.groupBox_StrikePrice.setFont(font)
        self.groupBox_StrikePrice.setObjectName("groupBox_StrikePrice")
        self.label_4 = QtWidgets.QLabel(self.groupBox_StrikePrice)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 41, 16))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_StrikePrice)
        self.label_3.setGeometry(QtCore.QRect(120, 30, 51, 16))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBox_StrikePriceRange = QtWidgets.QComboBox(self.groupBox_StrikePrice)
        self.comboBox_StrikePriceRange.setGeometry(QtCore.QRect(50, 30, 51, 16))
        self.comboBox_StrikePriceRange.setObjectName("comboBox_StrikePriceRange")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceRange.addItem("")
        self.comboBox_StrikePriceMultiple = QtWidgets.QComboBox(self.groupBox_StrikePrice)
        self.comboBox_StrikePriceMultiple.setGeometry(QtCore.QRect(170, 30, 51, 16))
        self.comboBox_StrikePriceMultiple.setObjectName("comboBox_StrikePriceMultiple")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(19, 50, 121, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_CallPut = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_CallPut.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_CallPut.setObjectName("gridLayout_CallPut")
        self.radioButton_Call = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton_Call.setChecked(True)
        self.radioButton_Call.setObjectName("radioButton_Call")
        self.gridLayout_CallPut.addWidget(self.radioButton_Call, 0, 0, 1, 1)
        self.radioButton_Put = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton_Put.setObjectName("radioButton_Put")
        self.gridLayout_CallPut.addWidget(self.radioButton_Put, 0, 1, 1, 1)
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(17, 220, 120, 25))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_CallPut_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_CallPut_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_CallPut_2.setObjectName("gridLayout_CallPut_2")
        self.radioButton_MktDataType_Frozen = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.radioButton_MktDataType_Frozen.setChecked(True)
        self.radioButton_MktDataType_Frozen.setObjectName("radioButton_MktDataType_Frozen")
        self.gridLayout_CallPut_2.addWidget(self.radioButton_MktDataType_Frozen, 0, 0, 1, 1)
        self.radioButton_MktDataType_Live = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.radioButton_MktDataType_Live.setObjectName("radioButton_MktDataType_Live")
        self.gridLayout_CallPut_2.addWidget(self.radioButton_MktDataType_Live, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.groupBox_2)
        self.line_2.setGeometry(QtCore.QRect(20, 40, 191, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 200, 111, 17))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.tableWidget = QtWidgets.QTableWidget(self.qualifyContracts_tab)
        self.tableWidget.setGeometry(QtCore.QRect(320, 30, 461, 221))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(19)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget_OptionGreeks = QtWidgets.QTableWidget(self.qualifyContracts_tab)
        self.tableWidget_OptionGreeks.setGeometry(QtCore.QRect(30, 310, 841, 341))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        self.tableWidget_OptionGreeks.setFont(font)
        self.tableWidget_OptionGreeks.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_OptionGreeks.setAlternatingRowColors(True)
        self.tableWidget_OptionGreeks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_OptionGreeks.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_OptionGreeks.setRowCount(6)
        self.tableWidget_OptionGreeks.setColumnCount(9)
        self.tableWidget_OptionGreeks.setObjectName("tableWidget_OptionGreeks")
        self.tableWidget_OptionGreeks.horizontalHeader().setDefaultSectionSize(90)
        self.tableWidget_OptionGreeks.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget_OptionGreeks.verticalHeader().setVisible(False)
        self.tableWidget_OptionGreeks.verticalHeader().setDefaultSectionSize(19)
        self.label_2 = QtWidgets.QLabel(self.qualifyContracts_tab)
        self.label_2.setGeometry(QtCore.QRect(30, 290, 101, 17))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        font.setPointSize(14)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(self.qualifyContracts_tab)
        self.label_7.setGeometry(QtCore.QRect(320, 10, 101, 17))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        font.setPointSize(14)
        font.setItalic(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.tabWidget_Contracts.addTab(self.qualifyContracts_tab, "")
        self.bullSpread_tab = QtWidgets.QWidget()
        self.bullSpread_tab.setObjectName("bullSpread_tab")
        self.tableWidget_BullSpread = QtWidgets.QTableWidget(self.bullSpread_tab)
        self.tableWidget_BullSpread.setGeometry(QtCore.QRect(20, 70, 451, 571))
        self.tableWidget_BullSpread.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_BullSpread.setAlternatingRowColors(True)
        self.tableWidget_BullSpread.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_BullSpread.setRowCount(5)
        self.tableWidget_BullSpread.setColumnCount(4)
        self.tableWidget_BullSpread.setObjectName("tableWidget_BullSpread")
        self.tableWidget_BullSpread.horizontalHeader().setDefaultSectionSize(105)
        self.tableWidget_BullSpread.horizontalHeader().setMinimumSectionSize(11)
        self.tableWidget_BullSpread.verticalHeader().setDefaultSectionSize(25)
        self.layoutWidget2 = QtWidgets.QWidget(self.bullSpread_tab)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 10, 260, 28))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.spinBox_numberOfContracts = QtWidgets.QSpinBox(self.layoutWidget2)
        self.spinBox_numberOfContracts.setMinimum(1)
        self.spinBox_numberOfContracts.setMaximum(15)
        self.spinBox_numberOfContracts.setObjectName("spinBox_numberOfContracts")
        self.horizontalLayout.addWidget(self.spinBox_numberOfContracts)
        self.pushButton_updateNumberOfContracts = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_updateNumberOfContracts.setObjectName("pushButton_updateNumberOfContracts")
        self.horizontalLayout.addWidget(self.pushButton_updateNumberOfContracts)
        self.label_9 = QtWidgets.QLabel(self.bullSpread_tab)
        self.label_9.setGeometry(QtCore.QRect(480, 50, 191, 20))
        self.label_9.setStyleSheet("font: 75 italic 11pt \"aakar\";\n"
                                   "color: rgb(32, 74, 135);")
        self.label_9.setObjectName("label_9")
        self.tableWidget_FrontRatioCallSpread = QtWidgets.QTableWidget(self.bullSpread_tab)
        self.tableWidget_FrontRatioCallSpread.setGeometry(QtCore.QRect(480, 70, 451, 571))
        self.tableWidget_FrontRatioCallSpread.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_FrontRatioCallSpread.setAlternatingRowColors(True)
        self.tableWidget_FrontRatioCallSpread.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_FrontRatioCallSpread.setRowCount(5)
        self.tableWidget_FrontRatioCallSpread.setColumnCount(4)
        self.tableWidget_FrontRatioCallSpread.setObjectName("tableWidget_FrontRatioCallSpread")
        self.tableWidget_FrontRatioCallSpread.horizontalHeader().setDefaultSectionSize(105)
        self.tableWidget_FrontRatioCallSpread.horizontalHeader().setMinimumSectionSize(11)
        self.tableWidget_FrontRatioCallSpread.verticalHeader().setDefaultSectionSize(25)
        self.label_10 = QtWidgets.QLabel(self.bullSpread_tab)
        self.label_10.setGeometry(QtCore.QRect(20, 50, 191, 20))
        self.label_10.setStyleSheet("font: 75 italic 11pt \"aakar\";\n"
                                    "color: rgb(32, 74, 135);")
        self.label_10.setObjectName("label_10")
        self.line = QtWidgets.QFrame(self.bullSpread_tab)
        self.line.setGeometry(QtCore.QRect(20, 35, 271, 20))
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.tabWidget_Contracts.addTab(self.bullSpread_tab, "")
        self.bearSpread_tab = QtWidgets.QWidget()
        self.bearSpread_tab.setObjectName("bearSpread_tab")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.bearSpread_tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 10, 751, 561))
        self.tableWidget_2.setRowCount(10)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tabWidget_Contracts.addTab(self.bearSpread_tab, "")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 20, 241, 27))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setStyleSheet("font: 75 italic 12pt \"Ubuntu Mono\";\n"
                                    "color: rgb(32, 74, 135);")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11)
        self.lineEdit_underlying = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_underlying.setReadOnly(True)
        self.lineEdit_underlying.setObjectName("lineEdit_underlying")
        self.horizontalLayout_2.addWidget(self.lineEdit_underlying)
        MainPyOptionsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainPyOptionsWindow)
        font = QtGui.QFont()
        font.setFamily("Chandas")
        font.setPointSize(10)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainPyOptionsWindow.setStatusBar(self.statusbar)
        self.actionIBToolbar = QtWidgets.QToolBar(MainPyOptionsWindow)
        self.actionIBToolbar.setMovable(False)
        self.actionIBToolbar.setFloatable(False)
        self.actionIBToolbar.setObjectName("actionIBToolbar")
        MainPyOptionsWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.actionIBToolbar)
        self.connectToIB = QtWidgets.QAction(MainPyOptionsWindow)
        self.connectToIB.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/icons/ConnectNo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/resources/icons/ConnectEstablished.ico"), QtGui.QIcon.Normal,
                        QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(":/resources/icons/ConnectCreating.ico"), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(":/resources/icons/ConnectCreating.ico"), QtGui.QIcon.Selected,
                        QtGui.QIcon.On)
        self.connectToIB.setIcon(icon1)
        self.connectToIB.setObjectName("connectToIB")
        self.actiontestIB = QtWidgets.QAction(MainPyOptionsWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../../../local-packages/localUtilities/icons/py_pic.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiontestIB.setIcon(icon2)
        self.actiontestIB.setObjectName("actiontestIB")
        self.actiontestCheckableIB = QtWidgets.QAction(MainPyOptionsWindow)
        self.actiontestCheckableIB.setCheckable(True)
        self.actiontestCheckableIB.setChecked(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../../../../local-packages/localUtilities/icons/about.gif"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiontestCheckableIB.setIcon(icon3)
        self.actiontestCheckableIB.setObjectName("actiontestCheckableIB")
        self.actionIBToolbar.addAction(self.connectToIB)
        self.actionIBToolbar.addSeparator()

        self.retranslateUi(MainPyOptionsWindow)
        self.tabWidget_Contracts.setCurrentIndex(0)
        self.tableWidget.cellClicked['int', 'int'].connect(self.tableWidget_OptionGreeks.selectRow)
        self.tableWidget_OptionGreeks.cellClicked['int', 'int'].connect(self.tableWidget.selectRow)
        QtCore.QMetaObject.connectSlotsByName(MainPyOptionsWindow)
        MainPyOptionsWindow.setTabOrder(self.tabWidget_Contracts, self.underlyingText)
        MainPyOptionsWindow.setTabOrder(self.underlyingText, self.radioButton_Index)
        MainPyOptionsWindow.setTabOrder(self.radioButton_Index, self.radioButton_Stock)
        MainPyOptionsWindow.setTabOrder(self.radioButton_Stock, self.radioButton_Option)
        MainPyOptionsWindow.setTabOrder(self.radioButton_Option, self.comboBoxExchange)
        MainPyOptionsWindow.setTabOrder(self.comboBoxExchange, self.comboBox_Expiry)
        MainPyOptionsWindow.setTabOrder(self.comboBox_Expiry, self.radioButton_Call)
        MainPyOptionsWindow.setTabOrder(self.radioButton_Call, self.radioButton_Put)
        MainPyOptionsWindow.setTabOrder(self.radioButton_Put, self.comboBox_StrikePriceRange)
        MainPyOptionsWindow.setTabOrder(self.comboBox_StrikePriceRange, self.comboBox_StrikePriceMultiple)
        MainPyOptionsWindow.setTabOrder(self.comboBox_StrikePriceMultiple, self.qualifyContracts)
        MainPyOptionsWindow.setTabOrder(self.qualifyContracts, self.tableWidget)
        MainPyOptionsWindow.setTabOrder(self.tableWidget, self.tableWidget_2)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< def setup Ui --goes to here:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # ===================this is not part of the QT Creator for setupUi()===================
        # These are the function connectors
        self.updateConnect()

        # don't forget these from QT
        self.retranslateUi(MainPyOptionsWindow)
        self.tabWidget_Contracts.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainPyOptionsWindow)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< def retranslateUi -- goes here:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def retranslateUi(self, MainPyOptionsWindow):
        _translate = QtCore.QCoreApplication.translate
        MainPyOptionsWindow.setWindowTitle(_translate("MainPyOptionsWindow", "IB Options"))
        self.groupBox_2.setTitle(_translate("MainPyOptionsWindow", "Underlying"))
        self.qualifyContracts.setText(_translate("MainPyOptionsWindow", "Qualify Contracts"))
        self.radioButton_Index.setText(_translate("MainPyOptionsWindow", "Index"))
        self.radioButton_Stock.setText(_translate("MainPyOptionsWindow", "Stock "))
        self.radioButton_Option.setText(_translate("MainPyOptionsWindow", "Option"))
        self.label_8.setText(_translate("MainPyOptionsWindow", "Underlying:"))
        self.labelExchange.setText(_translate("MainPyOptionsWindow", "Exchange:"))
        self.label.setText(_translate("MainPyOptionsWindow", "Expiry"))
        self.comboBoxExchange.setItemText(0, _translate("MainPyOptionsWindow", "CBOE"))
        self.comboBoxExchange.setItemText(1, _translate("MainPyOptionsWindow", "NASDAQ"))
        self.comboBoxExchange.setItemText(2, _translate("MainPyOptionsWindow", "SMART"))
        self.comboBoxExchange.setItemText(3, _translate("MainPyOptionsWindow", "ISLAND"))
        self.comboBoxExchange.setItemText(4, _translate("MainPyOptionsWindow", "NYSE"))
        self.comboBoxExchange.setItemText(5, _translate("MainPyOptionsWindow", "AMEX"))
        self.comboBoxExchange.setItemText(6, _translate("MainPyOptionsWindow", "IDEAL"))
        self.comboBoxExchange.setItemText(7, _translate("MainPyOptionsWindow", "PHLX"))
        self.groupBox_StrikePrice.setTitle(_translate("MainPyOptionsWindow", "Strike Price"))
        self.label_4.setText(_translate("MainPyOptionsWindow", "Range"))
        self.label_3.setText(_translate("MainPyOptionsWindow", "Multiple"))
        self.comboBox_StrikePriceRange.setItemText(0, _translate("MainPyOptionsWindow", "5"))
        self.comboBox_StrikePriceRange.setItemText(1, _translate("MainPyOptionsWindow", "10"))
        self.comboBox_StrikePriceRange.setItemText(2, _translate("MainPyOptionsWindow", "15"))
        self.comboBox_StrikePriceRange.setItemText(3, _translate("MainPyOptionsWindow", "20"))
        self.comboBox_StrikePriceRange.setItemText(4, _translate("MainPyOptionsWindow", "25"))
        self.comboBox_StrikePriceRange.setItemText(5, _translate("MainPyOptionsWindow", "30"))
        self.comboBox_StrikePriceRange.setItemText(6, _translate("MainPyOptionsWindow", "35"))
        self.comboBox_StrikePriceRange.setItemText(7, _translate("MainPyOptionsWindow", "40"))
        self.comboBox_StrikePriceRange.setItemText(8, _translate("MainPyOptionsWindow", "45"))
        self.comboBox_StrikePriceRange.setItemText(9, _translate("MainPyOptionsWindow", "50"))
        self.comboBox_StrikePriceMultiple.setItemText(0, _translate("MainPyOptionsWindow", "5"))
        self.comboBox_StrikePriceMultiple.setItemText(1, _translate("MainPyOptionsWindow", "10"))
        self.comboBox_StrikePriceMultiple.setItemText(2, _translate("MainPyOptionsWindow", "15"))
        self.comboBox_StrikePriceMultiple.setItemText(3, _translate("MainPyOptionsWindow", "20"))
        self.radioButton_Call.setText(_translate("MainPyOptionsWindow", "Call"))
        self.radioButton_Put.setText(_translate("MainPyOptionsWindow", "Put"))
        self.radioButton_MktDataType_Frozen.setText(_translate("MainPyOptionsWindow", "Frozen"))
        self.radioButton_MktDataType_Live.setText(_translate("MainPyOptionsWindow", "Live"))
        self.label_5.setText(_translate("MainPyOptionsWindow", "Market Data Type"))
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget_OptionGreeks.setSortingEnabled(False)
        self.label_2.setText(_translate("MainPyOptionsWindow", "The Greeks"))
        self.label_7.setText(_translate("MainPyOptionsWindow", "Contracts"))
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.qualifyContracts_tab),
                                            _translate("MainPyOptionsWindow", "Option Contracts / Greeks"))
        self.label_6.setText(_translate("MainPyOptionsWindow", "Number Of Contracts"))
        self.pushButton_updateNumberOfContracts.setText(_translate("MainPyOptionsWindow", "Update"))
        self.label_9.setText(_translate("MainPyOptionsWindow", "Front Ratio Call Spread "))
        self.label_10.setText(_translate("MainPyOptionsWindow", "Bull Call Spread "))
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.bullSpread_tab),
                                            _translate("MainPyOptionsWindow", "Bull Spread"))
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.bearSpread_tab),
                                            _translate("MainPyOptionsWindow", "Bear Spread"))
        self.label_11.setText(_translate("MainPyOptionsWindow", "Underlying: "))
        self.actionIBToolbar.setWindowTitle(_translate("MainPyOptionsWindow", "toolBar_2"))
        self.connectToIB.setText(_translate("MainPyOptionsWindow", "Connect to IB "))
        self.connectToIB.setToolTip(_translate("MainPyOptionsWindow", "Connect to IB api"))
        self.actiontestIB.setText(_translate("MainPyOptionsWindow", "test"))
        self.actiontestIB.setToolTip(_translate("MainPyOptionsWindow", "Bark"))
        self.actiontestCheckableIB.setText(_translate("MainPyOptionsWindow", "testCheckable"))
        self.actiontestCheckableIB.setToolTip(_translate("MainPyOptionsWindow", "Meow"))

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< def retranslateUi -- to here:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # ================this is not part of the QT Creator for retranslateUi()===================
        self.doExpiry(_translate)
        self.trimTable(_translate)

    def trimTable(self, _translate):
        headers = ['ID', 'Symbol', 'Expriy', 'Strike', 'Right']
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setAlternatingRowColors(True)

        headerGreeks = ['ID', 'Right', 'Expiry','Strike', 'Price', 'ImpliedVol', 'Gamma',
                        'Delta', 'TimeVal']
        self.tableWidget_OptionGreeks.setHorizontalHeaderLabels(headerGreeks)
        self.tableWidget_OptionGreeks.setAlternatingRowColors(True)

        headerBullSpread = ['Strike Low/Buy', 'Strike High/Sell', 'Max$ Loss','Max$ Profit']
        self.tableWidget_BullSpread.setHorizontalHeaderLabels(headerBullSpread)
        self.tableWidget_BullSpread.setAlternatingRowColors(True)


    def doExpiry(self, _translate):
        """Create a list of 18 Months of Option Fridays
        for the Expiry DropDown: comboBox_Expiry

        Keyword arguments:
        none
        """
        orderNum = 0
        expiry_list = dateUtils.getMonthExpiries()
        for anExpiry in expiry_list:
            self.comboBox_Expiry.addItem("")
            self.comboBox_Expiry.setItemText(orderNum, _translate("MainPyOptionsWindow", anExpiry))
            orderNum += 1

    def get_underlying_info(self):
        #TODO drop/queue history/ any existing instance of contracts if new instance is created
        #TODO filter out or combine Weekly or Monthly at the UI level
        self.statusbar.clearMessage()

        #clear contents for feed back to user - new call
        self.tableWidget.clearContents()
        self.tableWidget_OptionGreeks.clearContents()
        self.tableWidget_BullSpread.clearContents()
        self.spinBox_numberOfContracts.setValue(1)

        the_underlying = self.underlyingText.text()
        the_exchange = self.comboBoxExchange.currentText()
        theStrikePriceRange = int(self.comboBox_StrikePriceRange.currentText())
        theStrikePriceMultiple = int(self.comboBox_StrikePriceMultiple.currentText())

        # set the type of Price Data to receive
        #   - Frozen market data is the last data recorded at market close.
        #   - Last market data is the last data set, which may be empty after hours
        self.ib.reqMarketDataType(self.marketDataType())

        # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
        # and create a Contract
        aSecurityType=self.security_type(the_underlying, the_exchange)

        # then if securityType == Stock get Friday Expiry if Index get Thursday Expiry
        theExpiry = self.comboBox_Expiry.currentText()
        expiryDate = dateUtils.getDateFromMonthYear(theExpiry)
        if self.securityType == configIB.STOCK_TYPE:
            theExpiry = dateUtils.getDateString(dateUtils.third_friday(expiryDate.year, expiryDate.month))
        else: #Index
            theExpiry = dateUtils.getDateString(dateUtils.third_Thursday(expiryDate.year, expiryDate.month))

        # Fully qualify the given contracts in-place.
        # This will fill in the missing fields in the contract, especially the conId.
        # Returns a list of contracts that have been successfully qualified.
        try:
            get_underlying = self.ib.qualifyContracts(aSecurityType)
        except ConnectionError: # are we connected?
            self.statusbar.showMessage("NOT CONNECTED!!! Knucklehead!!!")
            return
        if not get_underlying:  # empty list - failed qualifyContract
            self.statusbar.showMessage("Underlying: " + the_underlying + " not recognized!")
        else:
            a_qualified_contract = get_underlying.pop()
            self.statusbar.showMessage(str(a_qualified_contract))

            # create a new optionClass instance
            self.an_option_spread = optionSpreadsClass.OptionSpreads(a_qualified_contract, self.ib)
            # Fully qualify the option
            self.an_option_spread.qualify_option_chain(self.right(), theExpiry, theStrikePriceRange, theStrikePriceMultiple)

            # Display the contracts
            self.displayContracts(self.an_option_spread.optionContracts)

            the_underlyingOutput = ' {} / Last Price: {:>7.2f}'.format(self.an_option_spread.a_Contract.symbol,
                self.an_option_spread.theUnderlyingReqTickerData.last)

            # Display Underlying price
            self.lineEdit_underlying.setText(the_underlyingOutput)
            logger.logger.info("Build Greeks")
            self.an_option_spread.buildGreeks()

            logger.logger.info("Display Greeks")
            self.displayGreeks(self.an_option_spread)
            self.an_option_spread.buildBullPandas()
            self.displayBullSpread(self.an_option_spread)
            self.an_option_spread.buildCallRatioSpread()


    def displayContracts(self, contracts):
        contractsLen = len(contracts)
        self.tableWidget.setRowCount(contractsLen)

        # clear the tables for new data...
        self.tableWidget.clearContents()
        self.tableWidget_OptionGreeks.clearContents()
        # Items are created outside the table (with no parent widget)
        # and inserted into the table with setItem():
        theRow = 0
        for aContract in contracts:
            # if Contract ID is 0 the Not Valid
            if aContract.conId == 0:
                self.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem('Not Valid Contract'))
            else:
                self.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem(str(aContract.conId)))
            # set the remaining data
            self.tableWidget.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aContract.symbol))
            self.tableWidget.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
                dateUtils.month3Format(aContract.lastTradeDateOrContractMonth)))
            self.tableWidget.setItem(theRow, 3, QtWidgets.QTableWidgetItem('{:>7.0f}'.format(aContract.strike)))
            self.tableWidget.setItem(theRow, 4, QtWidgets.QTableWidgetItem(aContract.right))
            #
            theRow = theRow + 1

    def displayGreeks(self, contracts):

        greeksLen = len(contracts.right) * ( len(contracts.theStrikes * len(contracts.theExpiration)))
        self.tableWidget_OptionGreeks.setRowCount(greeksLen)
        self.tableWidget_OptionGreeks.clearContents()
        # Items are created outside the table (with no parent widget)
        # and inserted into the table with setItem():
        theRow = 0
        anExpriy = contracts.theExpiration
        for aRight in contracts.right:
            for aStrike in contracts.theStrikes:
                self.tableWidget_OptionGreeks.setItem(theRow, 0, QtWidgets.QTableWidgetItem(
                    '{:d}'.format(int(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'ID']))))
                self.tableWidget_OptionGreeks.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aRight))
                self.tableWidget_OptionGreeks.setItem(theRow, 2,
                                                      QtWidgets.QTableWidgetItem(dateUtils.month3Format(anExpriy)))
                self.tableWidget_OptionGreeks.setItem(theRow, 3, QtWidgets.QTableWidgetItem(str(aStrike)))
                self.tableWidget_OptionGreeks.setItem(theRow, 4, QtWidgets.QTableWidgetItem(
                    '{:>7.2f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'Price'])))
                self.tableWidget_OptionGreeks.setItem(theRow, 5, QtWidgets.QTableWidgetItem(
                    '{:>2.2%}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'ImpliedVol'])))
                self.tableWidget_OptionGreeks.setItem(theRow, 6, QtWidgets.QTableWidgetItem(
                    '{:>.6f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'Gamma'])))
                self.tableWidget_OptionGreeks.setItem(theRow, 7, QtWidgets.QTableWidgetItem(
                    '{:>.6f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'Delta'])))
                self.tableWidget_OptionGreeks.setItem(theRow, 8, QtWidgets.QTableWidgetItem(
                    '{:>7.2f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'TimeVal'])))

                theRow += 1

    def displayBullSpread(self, contracts):
        # todo does this work for Puts??

        self.tableWidget_BullSpread.setRowCount(contracts.bullCallSpreads.shape[0])

        self.tableWidget_BullSpread.clearContents()

        theRow = 0
        for aStrikeL in contracts.theStrikes:
            self.tableWidget_BullSpread.setItem(theRow, 0, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeL)))
            self.tableWidget_BullSpread.item(theRow, 0).setBackground(QtGui.QColor("lightBlue"))
            for aStrikeH in contracts.theStrikes:
                if aStrikeL < aStrikeH:
                    self.tableWidget_BullSpread.setItem(theRow, 1, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeH)))
                    self.tableWidget_BullSpread.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
                                                        '{:>7.2f}'.format(contracts.bullCallSpreads.loc[(aStrikeL,
                                                                                                         aStrikeH),
                                                                                                        'Loss$'])))
                    self.tableWidget_BullSpread.setItem(theRow, 3,QtWidgets.QTableWidgetItem(
                                                        '{:>7.2f}'.format(contracts.bullCallSpreads.loc[(aStrikeL,
                                                                                                         aStrikeH),
                                                                                                        'Max$'])))
                    theRow += 1

    def right(self):
        if self.radioButton_Call.isChecked():
            return configIB.CALL_RIGHT
        else:
            return configIB.PUT_RIGHT

    def marketDataType(self):
        if self.radioButton_MktDataType_Frozen.isChecked():
            return configIB.MARKET_DATA_TYPE_FROZEN
        else:
            return configIB.MARKET_DATA_TYPE_LIVE

    def priceDataType(self):
        if self.radioButton_TradeClose.isChecked():
            return configIB.CLOSE_PRICE
        else:
            return configIB.LAST_PRICE

    def security_type(self, the_underlying, the_exchange):
        """ from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying.
        Create Contract.
        :param the_underlying: Stock/Index
        :param the_exchange: CBOE etc
        :return:
        """
        if self.radioButton_Index.isChecked():
            a_underlying = Index(the_underlying, the_exchange, 'USD')
            self.securityType = "IND"
        elif self.radioButton_Stock.isChecked():
            a_underlying = Stock(the_underlying, the_exchange, 'USD')
            self.securityType = "STK"
        else:
            logger.logger.info('<<<< in bullSpreadViewSmall.get_underlying_info(self)>>>>> Option Radio not !completed!')
        return a_underlying

    def updateConnect(self):
        self.qualifyContracts.clicked.connect(self.get_underlying_info)
        self.connectToIB.triggered.connect(self.onConnectButtonClicked)
        self.pushButton_updateNumberOfContracts.clicked.connect(self.updateBullContracts)
        # line 315
        #         self.pushButton_updateNumberOfContracts.clicked.connect(self.tableWidget_BullSpread.update)

    def updateBullContracts(self):
        try:
            self.an_option_spread
        except NameError:
            self.statusbar.showMessage(".....need to get a contract first.....")
        else:
            theContractCount = self.spinBox_numberOfContracts.value()
            self.an_option_spread.updateBullSpreads(theContractCount)
            self.displayBullSpread(self.an_option_spread)
            self.an_option_spread.updateCallRatioSpread(theContractCount)



    def onConnectButtonClicked(self):
        if self.connectToIB.isChecked():
            self.ib.connect(configIB.IB_API_HOST,
                        configIB.IB_PAPER_TRADE_PORT,
                        configIB.IB_API_CLIENTID_1)
            # TODO automate the Close/Frozen data from the GUI and the Client ID
            # todo add clientID to menu
            self.statusbar.showMessage("Connected to IB Paper and client #1")
        else:
            self.ib.disconnect()
            self.statusbar.showMessage("Disconnected from IB")

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainPyOptionsWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

