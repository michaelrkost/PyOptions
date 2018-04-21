
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from ib_insync import *

from localUtilities import errorHandler, configIB, buildOptionMatrices, dateUtils



def trimTable(self, _translate):
    headers = ['conId', 'symbol', 'lastTradeDate', 'strike', 'right']
    self.tableWidget.setColumnCount(len(headers))
    self.tableWidget.setHorizontalHeaderLabels(headers)
    self.tableWidget.setAlternatingRowColors(True)


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

    a = self.security_type(the_underlying, the_exchange)
    try:
        get_underlying = self.ib.qualifyContracts(a)
    except ConnectionError:
        self.statusbar.showMessage("NOT CONNECTED")
        return
    if not get_underlying:  # empty list - failed qualifyContract
        self.statusbar.showMessage("Underlying: " + the_underlying + " not recognized!")
    else:
        print('self.comboBoxExchange.currentText(): ', self.comboBoxExchange.currentText())
        a_qualified_contract = get_underlying.pop()
        self.statusbar.showMessage(str(a_qualified_contract))
        contracts = buildOptionMatrices.qualify_option_chain_close(self.ib, a_qualified_contract,
                                                                   self.right(), self.comboBoxExchange.currentText())
        print("=================================Contracts: \n", contracts)
        self.displayContracts(contracts)


def displayContracts(self, contracts):
    contractsLen = len(contracts)
    self.tableWidget.setRowCount(contractsLen)
    self.tableWidget.clearContents()
    # Items are created ouside the table (with no parent widget) and inserted into the table with setItem():
    theRow = 0
    for aContract in contracts:
        if aContract.conId == 0:
            self.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem('Not Valid Contract'))
        else:
            self.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem(str(aContract.conId)))

        self.tableWidget.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aContract.symbol))
        self.tableWidget.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
            dateUtils.month3Format(aContract.lastTradeDateOrContractMonth)))
        self.tableWidget.setItem(theRow, 3, QtWidgets.QTableWidgetItem(str(aContract.strike)))
        self.tableWidget.setItem(theRow, 4, QtWidgets.QTableWidgetItem(aContract.right))

        theRow = theRow + 1
        print("row: ", theRow, 'Contract:  ', aContract)
        print(aContract.conId)


def right(self):
    if self.radioButton_Call.isChecked():
        return 'C'
    else:
        return 'P'


def security_type(self, the_underlying, the_exchange):
    if self.radioButton_Index.isChecked():
        a_underlying = Index(the_underlying, the_exchange)
    elif self.radioButton_Stock.isChecked():
        a_underlying = Stock(the_underlying, the_exchange)
    else:
        print('<<<< in bullSpreadViewSmall.get_underlying_info(self)>>>>> Option Radio not !completed!')
    return a_underlying


def onConnectButtonClicked(win):
    if win.connectToIB.isChecked():
        win.ib.connect(configIB.IB_API_HOST,
                        configIB.IB_PAPER_TRADE_PORT,
                        configIB.IB_API_CLIENTID_1)
        win.statusbar.showMessage("Connected to IB")
    else:
        win.ib.disconnect()
        # had an issue with disconnecting
        # as disconnect is not accure on the IB Gateway
        # but was disconnected in my code found this thread
        # https://github.com/erdewit/ib_insync/issues/10
        # adding the loop works - not sure why 4/15/18 - mrk
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.sleep(0))
        win.statusbar.showMessage("Disconnected from IB")
