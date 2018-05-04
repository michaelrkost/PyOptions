# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bullSpreadViewSmall.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from ib_insync import *
util.useQt()

# Option management class for PyOptions - mrk
import optionClass

from localUtilities import errorHandler, configIB, buildOptionMatrices, dateUtils

class Ui_MainPyOptionsWindow(object):
    def __init__(self):
        self.ib = IB()
        self.ib.setCallback('error', errorHandler.onError)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< def setup Ui      -- goes here:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def setupUi(self, MainPyOptionsWindow):
        MainPyOptionsWindow.setObjectName("MainPyOptionsWindow")
        MainPyOptionsWindow.resize(1196, 742)
        MainPyOptionsWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/icons/ib.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainPyOptionsWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainPyOptionsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_Contracts = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Contracts.setGeometry(QtCore.QRect(0, 0, 1111, 661))
        self.tabWidget_Contracts.setObjectName("tabWidget_Contracts")
        self.getStuff_tab = QtWidgets.QWidget()
        self.getStuff_tab.setObjectName("getStuff_tab")
        self.groupBox_2 = QtWidgets.QGroupBox(self.getStuff_tab)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 10, 291, 321))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.updateQualifyClose = QtWidgets.QPushButton(self.groupBox_2)
        self.updateQualifyClose.setGeometry(QtCore.QRect(170, 290, 111, 23))
        self.updateQualifyClose.setObjectName("updateQualifyClose")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 70, 250, 50))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_underlying = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_underlying.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_underlying.setObjectName("gridLayout_underlying")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_underlying.addWidget(self.label_8, 0, 0, 1, 1)
        self.labelExchange = QtWidgets.QLabel(self.layoutWidget)
        self.labelExchange.setWhatsThis("")
        self.labelExchange.setObjectName("labelExchange")
        self.gridLayout_underlying.addWidget(self.labelExchange, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_underlying.addWidget(self.label, 0, 2, 1, 1)
        self.underlyingText = QtWidgets.QLineEdit(self.layoutWidget)
        self.underlyingText.setObjectName("underlyingText")
        self.gridLayout_underlying.addWidget(self.underlyingText, 1, 0, 1, 1)
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
        self.gridLayout_underlying.addWidget(self.comboBoxExchange, 1, 1, 1, 1)
        self.comboBox_Expiry = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.comboBox_Expiry.setFont(font)
        self.comboBox_Expiry.setObjectName("comboBox_Expiry")
        self.gridLayout_underlying.addWidget(self.comboBox_Expiry, 1, 2, 1, 1)
        self.groupBox_StrikePrice = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_StrikePrice.setGeometry(QtCore.QRect(20, 220, 131, 91))
        self.groupBox_StrikePrice.setObjectName("groupBox_StrikePrice")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_StrikePrice)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_StrikePrice)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_StrikePrice)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox_StrikePriceRange = QtWidgets.QComboBox(self.groupBox_StrikePrice)
        self.comboBox_StrikePriceRange.setStatusTip("")
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
        self.gridLayout_2.addWidget(self.comboBox_StrikePriceRange, 0, 1, 1, 1)
        self.comboBox_StrikePriceMultiple = QtWidgets.QComboBox(self.groupBox_StrikePrice)
        self.comboBox_StrikePriceMultiple.setStatusTip("")
        self.comboBox_StrikePriceMultiple.setObjectName("comboBox_StrikePriceMultiple")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.comboBox_StrikePriceMultiple.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_StrikePriceMultiple, 1, 1, 1, 1)
        self.layoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget_3.setGeometry(QtCore.QRect(20, 30, 195, 25))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout_UnderType = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout_UnderType.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_UnderType.setObjectName("gridLayout_UnderType")
        self.radioButton_Index = QtWidgets.QRadioButton(self.layoutWidget_3)
        self.radioButton_Index.setChecked(True)
        self.radioButton_Index.setObjectName("radioButton_Index")
        self.gridLayout_UnderType.addWidget(self.radioButton_Index, 0, 0, 1, 1)
        self.radioButton_Stock = QtWidgets.QRadioButton(self.layoutWidget_3)
        self.radioButton_Stock.setObjectName("radioButton_Stock")
        self.gridLayout_UnderType.addWidget(self.radioButton_Stock, 0, 1, 1, 1)
        self.radioButton_Option = QtWidgets.QRadioButton(self.layoutWidget_3)
        self.radioButton_Option.setObjectName("radioButton_Option")
        self.gridLayout_UnderType.addWidget(self.radioButton_Option, 0, 2, 1, 1)
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(20, 132, 251, 71))
        self.widget.setObjectName("widget")
        self.gridLayout_Type = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_Type.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Type.setObjectName("gridLayout_Type")
        self.frameType = QtWidgets.QFrame(self.widget)
        self.frameType.setFrameShape(QtWidgets.QFrame.Box)
        self.frameType.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameType.setObjectName("frameType")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frameType)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.radioButton_MktDataType_Frozen = QtWidgets.QRadioButton(self.frameType)
        self.radioButton_MktDataType_Frozen.setChecked(True)
        self.radioButton_MktDataType_Frozen.setObjectName("radioButton_MktDataType_Frozen")
        self.gridLayout_5.addWidget(self.radioButton_MktDataType_Frozen, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frameType)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.radioButton_MktDataType_Live = QtWidgets.QRadioButton(self.frameType)
        self.radioButton_MktDataType_Live.setChecked(False)
        self.radioButton_MktDataType_Live.setObjectName("radioButton_MktDataType_Live")
        self.gridLayout_5.addWidget(self.radioButton_MktDataType_Live, 1, 0, 1, 1)
        self.gridLayout_Type.addWidget(self.frameType, 0, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 0, 0, 1, 1)
        self.radioButton_Call = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_Call.setChecked(True)
        self.radioButton_Call.setObjectName("radioButton_Call")
        self.gridLayout_7.addWidget(self.radioButton_Call, 1, 0, 1, 1)
        self.radioButton_Put = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_Put.setObjectName("radioButton_Put")
        self.gridLayout_7.addWidget(self.radioButton_Put, 2, 0, 1, 1)
        self.gridLayout_Type.addWidget(self.frame_2, 0, 0, 1, 1)
        self.Frame1 = QtWidgets.QFrame(self.widget)
        self.Frame1.setFrameShape(QtWidgets.QFrame.Panel)
        self.Frame1.setObjectName("Frame1")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.Frame1)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.radioButton_TradeClose = QtWidgets.QRadioButton(self.Frame1)
        self.radioButton_TradeClose.setChecked(False)
        self.radioButton_TradeClose.setObjectName("radioButton_TradeClose")
        self.gridLayout_6.addWidget(self.radioButton_TradeClose, 2, 0, 1, 1)
        self.radioButton_TradeLast = QtWidgets.QRadioButton(self.Frame1)
        self.radioButton_TradeLast.setChecked(True)
        self.radioButton_TradeLast.setObjectName("radioButton_TradeLast")
        self.gridLayout_6.addWidget(self.radioButton_TradeLast, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.Frame1)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)
        self.gridLayout_Type.addWidget(self.Frame1, 0, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.getStuff_tab)
        self.tableWidget.setGeometry(QtCore.QRect(410, 10, 481, 601))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(19)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tabWidget_Contracts.addTab(self.getStuff_tab, "")
        self.greek_tab = QtWidgets.QWidget()
        self.greek_tab.setObjectName("greek_tab")
        self.tableWidget_OptionGreeks = QtWidgets.QTableWidget(self.greek_tab)
        self.tableWidget_OptionGreeks.setGeometry(QtCore.QRect(40, 20, 1051, 581))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        self.tableWidget_OptionGreeks.setFont(font)
        self.tableWidget_OptionGreeks.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tableWidget_OptionGreeks.setAlternatingRowColors(True)
        self.tableWidget_OptionGreeks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_OptionGreeks.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget_OptionGreeks.setRowCount(6)
        self.tableWidget_OptionGreeks.setColumnCount(10)
        self.tableWidget_OptionGreeks.setObjectName("tableWidget_OptionGreeks")
        self.tabWidget_Contracts.addTab(self.greek_tab, "")
        self.bullSpread_tab = QtWidgets.QWidget()
        self.bullSpread_tab.setObjectName("bullSpread_tab")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.bullSpread_tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 10, 751, 561))
        self.tableWidget_2.setRowCount(10)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tabWidget_Contracts.addTab(self.bullSpread_tab, "")
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

        self.retranslateUi(MainPyOptionsWindow)
        self.tabWidget_Contracts.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainPyOptionsWindow)
        MainPyOptionsWindow.setTabOrder(self.tabWidget_Contracts, self.underlyingText)
        MainPyOptionsWindow.setTabOrder(self.underlyingText, self.comboBoxExchange)
        MainPyOptionsWindow.setTabOrder(self.comboBoxExchange, self.comboBox_Expiry)
        MainPyOptionsWindow.setTabOrder(self.comboBox_Expiry, self.updateQualifyClose)
        MainPyOptionsWindow.setTabOrder(self.updateQualifyClose, self.tableWidget)
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
        MainPyOptionsWindow.setWindowTitle(_translate("MainPyOptionsWindow", "IB PyOptions"))
        self.groupBox_2.setTitle(_translate("MainPyOptionsWindow", "Underlying"))
        self.updateQualifyClose.setText(_translate("MainPyOptionsWindow", "Qualify Contracts"))
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
        self.groupBox_StrikePrice.setTitle(_translate("MainPyOptionsWindow", "Strkie Price"))
        self.label_3.setText(_translate("MainPyOptionsWindow", "Multiple"))
        self.label_4.setText(_translate("MainPyOptionsWindow", "Range"))
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
        self.radioButton_Index.setText(_translate("MainPyOptionsWindow", "Index"))
        self.radioButton_Stock.setText(_translate("MainPyOptionsWindow", "Stock "))
        self.radioButton_Option.setText(_translate("MainPyOptionsWindow", "Option"))
        self.radioButton_MktDataType_Frozen.setText(_translate("MainPyOptionsWindow", "Frozen"))
        self.label_5.setText(_translate("MainPyOptionsWindow", "Market Data Type "))
        self.radioButton_MktDataType_Live.setText(_translate("MainPyOptionsWindow", "Live"))
        self.label_7.setText(_translate("MainPyOptionsWindow", "Right"))
        self.radioButton_Call.setText(_translate("MainPyOptionsWindow", "Call"))
        self.radioButton_Put.setText(_translate("MainPyOptionsWindow", "Put"))
        self.radioButton_TradeClose.setText(_translate("MainPyOptionsWindow", "Close"))
        self.radioButton_TradeLast.setText(_translate("MainPyOptionsWindow", "Last"))
        self.label_6.setText(_translate("MainPyOptionsWindow", "Price Type"))
        self.tableWidget.setSortingEnabled(True)
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.getStuff_tab),
                                            _translate("MainPyOptionsWindow", "Option Contracts "))
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.greek_tab),
                                            _translate("MainPyOptionsWindow", "The Greeks"))
        self.tabWidget_Contracts.setTabText(self.tabWidget_Contracts.indexOf(self.bullSpread_tab),
                                            _translate("MainPyOptionsWindow", "Bear Spreads"))
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
        headers = ['Id', 'Symbol', 'Expriy', 'Strike', 'Right']
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setAlternatingRowColors(True)

        headerGreeks = ['Right', 'Expiry','Strike', 'Price', 'ImpliedVol', 'Gamma',
                        'Delta', 'TimeVal', 'conId']
        self.tableWidget_OptionGreeks.setHorizontalHeaderLabels(headerGreeks)
        self.tableWidget_OptionGreeks.setAlternatingRowColors(True)


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


        # To Use the Close price or Last price
        #thePriceType = self.priceDataType()


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

            #TODO: add check for time and date - whether to use close(market closed) or last(active market)

            # create a new optionClass instance
            an_option_spread = optionClass.OptionSpreads(a_qualified_contract, self.ib)
            # Fully qualify the option
            an_option_spread.qualify_option_chain(self.right(), theExpiry, theStrikePriceRange, theStrikePriceMultiple)

            # Display the contracts
            self.displayContracts(an_option_spread.optionContracts)

            an_option_spread.buildGreeks()
            # todo -- this is next!
            self.displayGreeks(an_option_spread)
            #an_option_spread.buildBullPandas()


    def displayContracts(self, contracts):
        contractsLen = len(contracts)
        self.tableWidget.setRowCount(contractsLen)
        self.tableWidget.clearContents()
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
            self.tableWidget.setItem(theRow, 3, QtWidgets.QTableWidgetItem(str(aContract.strike)))
            self.tableWidget.setItem(theRow, 4, QtWidgets.QTableWidgetItem(aContract.right))
            #
            theRow = theRow + 1

    def displayGreeks(self, contracts):
        # contractsLen = len(contracts)
        greeksLen = len(contracts.right) * ( len(contracts.theStrikes * len(contracts.theExpiration)))
        self.tableWidget_OptionGreeks.setRowCount(greeksLen)
        self.tableWidget_OptionGreeks.clearContents()
        # Items are created outside the table (with no parent widget)
        # and inserted into the table with setItem():
        theRow = 0
        anExpriy = contracts.theExpiration
        for aRight in contracts.right:
            for aStrike in contracts.theStrikes:

                    # todo use .format to get the proper formatting...
                    self.tableWidget_OptionGreeks.setItem(theRow, 0, QtWidgets.QTableWidgetItem(aRight))
                    self.tableWidget_OptionGreeks.setItem(theRow, 2, QtWidgets.QTableWidgetItem(str(aStrike)))
                    self.tableWidget_OptionGreeks.setItem(theRow, 1,
                                                          QtWidgets.QTableWidgetItem(dateUtils.month3Format(anExpriy)))
                    self.tableWidget_OptionGreeks.setItem(theRow, 3, QtWidgets.QTableWidgetItem(
                        '{:>7.2f}'.format(contracts.closeOptionPrices.loc[(aRight, anExpriy, aStrike),'Price'])))
                    self.tableWidget_OptionGreeks.setItem(theRow, 4, QtWidgets.QTableWidgetItem(
                        '{:.6f}'.format(contracts.closeOptionPrices.loc[(aRight, anExpriy, aStrike),'ImpliedVol'])))
                    self.tableWidget_OptionGreeks.setItem(theRow, 5, QtWidgets.QTableWidgetItem(
                        '{:.6f}'.format(contracts.closeOptionPrices.loc[(aRight, anExpriy, aStrike), 'Gamma'])))
                    self.tableWidget_OptionGreeks.setItem(theRow, 6, QtWidgets.QTableWidgetItem(
                        '{:.6f}'.format(contracts.closeOptionPrices.loc[(aRight, anExpriy, aStrike), 'Delta'])))
                    self.tableWidget_OptionGreeks.setItem(theRow, 7, QtWidgets.QTableWidgetItem(
                        '{:>7.2f}'.format(contracts.closeOptionPrices.loc[(aRight, anExpriy, aStrike),'TimeVal'])))
                    
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
            print('<<<< in bullSpreadViewSmall.get_underlying_info(self)>>>>> Option Radio not !completed!')
        return a_underlying

    def updateConnect(self):
        self.updateQualifyClose.clicked.connect(self.get_underlying_info)
        self.connectToIB.triggered.connect(self.onConnectButtonClicked)

    def onConnectButtonClicked(self):
        if self.connectToIB.isChecked():
            self.ib.connect(configIB.IB_API_HOST,
                        configIB.IB_PAPER_TRADE_PORT,
                        configIB.IB_API_CLIENTID_1)
            # TODO automate the Close/Frozen data from the GUI and the Client ID
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

