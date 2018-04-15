# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bullSpreadViewSmall.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ib_insync import *

# Neeed to disconnect
# see note in function // onConnectButtonClicked
import asyncio

from localUtilities import errorHandler, configIB, buildOptionMatrices, dateUtils

class Ui_MainWindow(object):
    def __init__(self):
        self.ib = IB()
        self.ib.setCallback('error', errorHandler.onError)

    # def setup Ui -- goes below:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(546, 319)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/ib.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 331, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.updatePushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.updatePushButton.setGeometry(QtCore.QRect(250, 110, 75, 23))
        self.updatePushButton.setObjectName("updatePushButton")
        self.splitter = QtWidgets.QSplitter(self.groupBox_2)
        self.splitter.setGeometry(QtCore.QRect(10, 80, 185, 17))
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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 231, 43))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.labelExchange = QtWidgets.QLabel(self.layoutWidget)
        self.labelExchange.setWhatsThis("")
        self.labelExchange.setObjectName("labelExchange")
        self.gridLayout.addWidget(self.labelExchange, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout.addWidget(self.comboBoxExchange, 1, 1, 1, 1)
        self.comboBox_Expiry = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.comboBox_Expiry.setFont(font)
        self.comboBox_Expiry.setObjectName("comboBox_Expiry")
        self.gridLayout.addWidget(self.comboBox_Expiry, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionIBToolbar = QtWidgets.QToolBar(MainWindow)
        self.actionIBToolbar.setMovable(False)
        self.actionIBToolbar.setFloatable(False)
        self.actionIBToolbar.setObjectName("actionIBToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.actionIBToolbar)
        self.connectToIB = QtWidgets.QAction(MainWindow)
        self.connectToIB.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/ConnectNo.ico"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/ConnectEstablished.ico"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/ConnectCreating.ico"),
                        QtGui.QIcon.Active, QtGui.QIcon.On)
        self.connectToIB.setIcon(icon1)
        self.connectToIB.setObjectName("connectToIB")
        self.actiontestIB = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/py_pic.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actiontestIB.setIcon(icon2)
        self.actiontestIB.setObjectName("actiontestIB")
        self.actiontestCheckableIB = QtWidgets.QAction(MainWindow)
        self.actiontestCheckableIB.setCheckable(True)
        self.actiontestCheckableIB.setChecked(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("P:/local-packages/localUtilities/icons/about.gif"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actiontestCheckableIB.setIcon(icon3)
        self.actiontestCheckableIB.setObjectName("actiontestCheckableIB")
        self.actionIBToolbar.addAction(self.connectToIB)

        # this is not part of the QT Creator for setupUi()
        # These are the function connectors
        self.updateConnect()

        # don't forget these from QT
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IB Options"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Underlying Info"))
        self.updatePushButton.setText(_translate("MainWindow", "Qualify"))
        self.radioButton_Index.setText(_translate("MainWindow", "Index"))
        self.radioButton_Stock.setText(_translate("MainWindow", "Stock "))
        self.radioButton_Option.setText(_translate("MainWindow", "Option"))
        self.label_8.setText(_translate("MainWindow", "Underlying:"))
        self.labelExchange.setText(_translate("MainWindow", "Exchange:"))
        self.label.setText(_translate("MainWindow", "Expiry"))
        self.comboBoxExchange.setItemText(0, _translate("MainWindow", "CBOE"))
        self.comboBoxExchange.setItemText(1, _translate("MainWindow", "SMART"))
        self.comboBoxExchange.setItemText(2, _translate("MainWindow", "ISLAND"))
        self.comboBoxExchange.setItemText(3, _translate("MainWindow", "NYSE"))
        self.comboBoxExchange.setItemText(4, _translate("MainWindow", "AMEX"))
        self.comboBoxExchange.setItemText(5, _translate("MainWindow", "IDEAL"))
        self.comboBoxExchange.setItemText(6, _translate("MainWindow", "PHLX"))
        self.actionIBToolbar.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.connectToIB.setText(_translate("MainWindow", "Connect to IB "))
        self.connectToIB.setToolTip(_translate("MainWindow", "Connect to IB api"))
        self.actiontestIB.setText(_translate("MainWindow", "test"))
        self.actiontestIB.setToolTip(_translate("MainWindow", "Bark"))
        self.actiontestCheckableIB.setText(_translate("MainWindow", "testCheckable"))
        self.actiontestCheckableIB.setToolTip(_translate("MainWindow", "Meow"))

        # this is not part of the QT Creator for retranslateUi()
        self.doExpiry(_translate)

    def doExpiry(self, _translate):
        """Create a list of 18 Months of Option Fridays
        for the Expiry DropDown: comboBox_Expiry

        Keyword arguments:
        none
        """
        orderNum = 0
        expiry_list = dateUtils.getExpiries()
        for anExpiry in expiry_list:
            self.comboBox_Expiry.addItem("")
            self.comboBox_Expiry.setItemText(orderNum, _translate("MainWindow", anExpiry))
            orderNum += 1

    def get_underlying_info(self):
        self.statusbar.clearMessage()
        the_underlying = self.underlyingText.text()
        the_exchange = self.comboBoxExchange.currentText()
        if self.radioButton_Index.isChecked():
            a_underlying = Index(the_underlying, the_exchange)
        elif self.radioButton_Stock.isChecked():
            a_underlying = Stock(the_underlying, the_exchange)
        else:
            print('<<<< in bullSpreadViewSmall.get_underlying_info(self)>>>>> Option Radio not compeletd')
        get_underlying = self.ib.qualifyContracts(a_underlying)
        if not get_underlying:  # empty list - failed qualifyContract
            self.statusbar.showMessage("Underlying: " + the_underlying + " not recognized!")
        else:
            a_qualified_contract = get_underlying.pop()
            self.statusbar.showMessage(str(a_qualified_contract))
            buildOptionMatrices.qualify_index_option_chain(self.ib, a_qualified_contract)


    def updateConnect(self):
        self.updatePushButton.clicked.connect(self.get_underlying_info)
        self.connectToIB.triggered.connect(self.onConnectButtonClicked)


    def onConnectButtonClicked(self):
        if self.connectToIB.isChecked():
            self.ib.connect(configIB.IB_API_HOST,
                        configIB.IB_PAPER_TRADE_PORT,
                        configIB.IB_API_CLIENTID_1)
            self.statusbar.showMessage("Connected to IB")
        else:
            self.ib.disconnect()
            # had an issue with disconnecting
            # as disconnect is not accure on the IB Gateway
            # but was disconnected in my code found this thread
            # https://github.com/erdewit/ib_insync/issues/10
            # adding the loop works - not sure why 4/15/18 - mrk
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.sleep(0))
            self.statusbar.showMessage("Disconnected from IB")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

