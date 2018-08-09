
from PyQt5 import QtGui, QtWidgets
from ib_insync import *

from localUtilities import configIB, dateUtils, ibPyUtils, ibPyViewUtils
import optionSpreadsClass

# All the table trimmings for the Vertical Spread View

def trimTable(tableWidget, tableWidget_OptionGreeks, tableWidget_BullSpread):
    headers = ['ID', 'Symbol', 'Expriy', 'Strike', 'Right']
    tableWidget.setColumnCount(len(headers))
    tableWidget.setHorizontalHeaderLabels(headers)
    tableWidget.setAlternatingRowColors(True)

    headerGreeks = ['ID', 'Right', 'Expiry', 'Strike', 'Price', 'ImpliedVol', 'Gamma',
                    'Delta', 'TimeVal']
    tableWidget_OptionGreeks.setHorizontalHeaderLabels(headerGreeks)
    tableWidget_OptionGreeks.setAlternatingRowColors(True)

    headerBullSpread = ['Strike Low/Buy', 'Strike High/Sell', 'Max$ Loss', 'Max$ Profit']
    tableWidget_BullSpread.setHorizontalHeaderLabels(headerBullSpread)
    tableWidget_BullSpread.setAlternatingRowColors(True)


def get_underlying_info(aTableWidget):
    #TODO drop/queue history/ any existing instance of contracts if new instance is created
    #TODO filter out or combine Weekly or Monthly at the UI level
    aTableWidget.statusbar.clearMessage()

    #clear contents for feed back to user - new call
    aTableWidget.tableWidget.clearContents()
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    aTableWidget.tableWidget_BullCallSpread.clearContents()
    aTableWidget.spinBox_numberOfContracts.setValue(1)

    the_underlying = aTableWidget.underlyingText.text()
    the_exchange = aTableWidget.comboBoxExchange.currentText()
    theStrikePriceRange = int(aTableWidget.comboBox_StrikePriceRange.currentText())
    theStrikePriceMultiple = int(aTableWidget.comboBox_StrikePriceMultiple.currentText())

    # set the type of Price Data to receive
    #   - Frozen market data is the last data recorded at market close.
    #   - Last market data is the last data set, which may be empty after hours
    aTableWidget.ib.reqMarketDataType(ibPyUtils.marketDataType(aTableWidget.radioButton_MktDataType_Frozen))
    print("frozenVS: ", aTableWidget.radioButton_MktDataType_Frozen.isChecked())

    # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
    # and create a Contract
    aSecurityType = ibPyUtils.security_type(aTableWidget, the_underlying, the_exchange)

    # then if securityType == Stock get Friday Expiry if Index get Thursday Expiry
    theExpiry = aTableWidget.comboBox_Expiry.currentText()
    expiryDate = dateUtils.getDateFromMonthYear(theExpiry)
    if aTableWidget.securityType == configIB.STOCK_TYPE:
        theExpiry = dateUtils.getDateString(dateUtils.third_friday(expiryDate.year, expiryDate.month))
    else: #Index
        theExpiry = dateUtils.getDateString(dateUtils.third_Thursday(expiryDate.year, expiryDate.month))

    # Fully qualify the given contracts in-place.
    # This will fill in the missing fields in the contract, especially the conId.
    # Returns a list of contracts that have been successfully qualified.
    try:
        get_underlying = aTableWidget.ib.qualifyContracts(aSecurityType)
    except ConnectionError: # are we connected?
        aTableWidget.statusbar.showMessage("NOT CONNECTED!!! Knucklehead!!!")
        return
    if not get_underlying:  # empty list - failed qualifyContract
        aTableWidget.statusbar.showMessage("Underlying: " + the_underlying + " not recognized!")
    else:
        a_qualified_contract = get_underlying.pop()
        aTableWidget.statusbar.showMessage(str(a_qualified_contract))

        # create a new optionClass instance
        aTableWidget.an_option_spread = optionSpreadsClass.OptionVerticalSpreads(a_qualified_contract, aTableWidget.ib)
        # Fully qualify the option
        aTableWidget.an_option_spread.qualify_option_chain(ibPyUtils.right(aTableWidget), theExpiry,
                                                           theStrikePriceRange, theStrikePriceMultiple)

        # Display the contracts
        displayContracts(aTableWidget, aTableWidget.an_option_spread.optionContracts)

        the_underlyingOutput = ' {} / Last Price: {:>7.2f}'.format(aTableWidget.an_option_spread.a_Contract.symbol,
                                                                   aTableWidget.an_option_spread.theUnderlyingReqTickerData.last)

        # Display Underlying price
        aTableWidget.lineEdit_underlying.setText(the_underlyingOutput)
        # logger.logger.info("Build Greeks")
        aTableWidget.an_option_spread.buildGreeks()

        # logger.logger.info("Display Greeks")
        displayGreeks(aTableWidget, aTableWidget.an_option_spread)
        aTableWidget.an_option_spread.buildPandasBullVerticalSpreads()
        displayBullSpread(aTableWidget, aTableWidget.an_option_spread)
        aTableWidget.an_option_spread.buildCallRatioSpread()

def displayContracts(aTableWidget, contracts):
    contractsLen = len(contracts)
    aTableWidget.tableWidget.setRowCount(contractsLen)

    # clear the tables for new data...
    aTableWidget.tableWidget.clearContents()
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    # Items are created outside the table (with no parent widget)
    # and inserted into the table with setItem():
    theRow = 0
    for aContract in contracts:
        # if Contract ID is 0 the Not Valid
        if aContract.conId == 0:
            aTableWidget.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem('Not Valid Contract'))
        else:
            aTableWidget.tableWidget.setItem(theRow, 0, QtWidgets.QTableWidgetItem(str(aContract.conId)))
        # set the remaining data
            aTableWidget.tableWidget.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aContract.symbol))
            aTableWidget.tableWidget.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
            dateUtils.month3Format(aContract.lastTradeDateOrContractMonth)))
            aTableWidget.tableWidget.setItem(theRow, 3, QtWidgets.QTableWidgetItem('{:>7.0f}'.format(aContract.strike)))
            aTableWidget.tableWidget.setItem(theRow, 4, QtWidgets.QTableWidgetItem(aContract.right))
        #
        theRow = theRow + 1

def displayGreeks(aTableWidget, contracts):

    greeksLen = len(contracts.right) * ( len(contracts.theStrikes * len(contracts.theExpiration)))
    aTableWidget.tableWidget_OptionGreeks.setRowCount(greeksLen)
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    # Items are created outside the table (with no parent widget)
    # and inserted into the table with setItem():
    theRow = 0
    anExpriy = contracts.theExpiration
    for aRight in contracts.right:
        for aStrike in contracts.theStrikes:
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 0, QtWidgets.QTableWidgetItem(
                '{:d}'.format(int(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'ID']))))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aRight))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 2,
                                                  QtWidgets.QTableWidgetItem(dateUtils.month3Format(anExpriy)))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 3, QtWidgets.QTableWidgetItem(str(aStrike)))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 4, QtWidgets.QTableWidgetItem(
                '{:>7.2f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'Price'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 5, QtWidgets.QTableWidgetItem(
                '{:>2.2%}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'ImpliedVol'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 6, QtWidgets.QTableWidgetItem(
                '{:>.6f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'Gamma'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 7, QtWidgets.QTableWidgetItem(
                '{:>.6f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike), 'Delta'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 8, QtWidgets.QTableWidgetItem(
                '{:>7.2f}'.format(contracts.optionPrices.loc[(aRight, anExpriy, aStrike),'TimeVal'])))

            theRow += 1

def displayBullSpread(aTableWidget, contracts):
    # todo does this work for Puts??

    aTableWidget.tableWidget_BullCallSpread.setRowCount(contracts.pandasBullCallVerticalSpread.shape[0])

    aTableWidget.tableWidget_BullCallSpread.clearContents()

    theRow = 0
    for aStrikeL in contracts.theStrikes:
        aTableWidget.tableWidget_BullCallSpread.setItem(theRow, 0, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeL)))
        aTableWidget.tableWidget_BullCallSpread.item(theRow, 0).setBackground(QtGui.QColor("lightBlue"))
        for aStrikeH in contracts.theStrikes:
            if aStrikeL < aStrikeH:
                aTableWidget.tableWidget_BullCallSpread.setItem(theRow, 1, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeH)))
                aTableWidget.tableWidget_BullCallSpread.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
                                                    '{:>7.2f}'.format(contracts.bullCallSpreads.loc[(aStrikeL,
                                                                                                     aStrikeH),
                                                                                                    'Loss$'])))
                aTableWidget.tableWidget_BullCallSpread.setItem(theRow, 3,QtWidgets.QTableWidgetItem(
                                                    '{:>7.2f}'.format(contracts.bullCallSpreads.loc[(aStrikeL,
                                                                                                     aStrikeH),
                                                                                                    'Max$'])))
                theRow += 1
#

def updateConnectVS(aTableWidget, _translate):
    """
    This sets up the button connectors i.e. connect
    lambda provides button action routine

    :param aTableWidget:
    :param _translate:
    :return:
    """
    aTableWidget.qualifyContracts.clicked.connect(lambda: get_underlying_info(aTableWidget))
    aTableWidget.pushButton_updateNumberOfContracts.clicked.connect(lambda: updateBullContracts(aTableWidget))

    ibPyUtils.doExpiry(aTableWidget.comboBox_Expiry, _translate)

    # todo - this should be in another module it is IB Connections...
    aTableWidget.connectToIB.triggered.connect(lambda: onConnectButtonClicked(aTableWidget))
    aTableWidget.actionVertical_Spreads.triggered.connect(lambda: aTableWidget.stackedWidget.setCurrentIndex(ibPyViewUtils.stackedWidgetView_VerticalSpread))


def updateBullContracts(aTableWidget):
    """

    :param aTableWidget:
    :return:
    """
    try:
        aTableWidget.an_option_spread
    except NameError:
        aTableWidget.statusbar.showMessage(".....need to get a contract first.....")
    else:
        theContractCount = aTableWidget.spinBox_numberOfContracts.value()
        aTableWidget.an_option_spread.updateBullSpreads(theContractCount)
        displayBullSpread(aTableWidget, aTableWidget.an_option_spread)
        aTableWidget.an_option_spread.updateCallRatioSpread(theContractCount)


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

