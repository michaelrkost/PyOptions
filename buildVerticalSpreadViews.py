
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from ib_insync import *

from localUtilities import errorHandler, configIB, buildOptionMatrices, dateUtils
import optionSpreadsClass

# All the trimmings for the Vertical Spread View

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
#
#
def doExpiry(comboBox_Expiry, a_translate):
    """Create a list of 18 Months of Option Fridays
    for the Expiry DropDown: comboBox_Expiry

    Keyword arguments:
    none
    """
    orderNum = 0
    expiry_list = dateUtils.getMonthExpiries()
    for anExpiry in expiry_list:
        comboBox_Expiry.addItem("")
        comboBox_Expiry.setItemText(orderNum, a_translate("MainWindow", anExpiry))
        orderNum += 1

def get_underlying_info(aTableWidget):
    #TODO drop/queue history/ any existing instance of contracts if new instance is created
    #TODO filter out or combine Weekly or Monthly at the UI level
    aTableWidget.statusbar.clearMessage()

    #clear contents for feed back to user - new call
    aTableWidget.tableWidget.clearContents()
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    aTableWidget.tableWidget_BullSpread.clearContents()
    aTableWidget.spinBox_numberOfContracts.setValue(1)

    the_underlying = aTableWidget.underlyingText.text()
    the_exchange = aTableWidget.comboBoxExchange.currentText()
    theStrikePriceRange = int(aTableWidget.comboBox_StrikePriceRange.currentText())
    theStrikePriceMultiple = int(aTableWidget.comboBox_StrikePriceMultiple.currentText())

    # set the type of Price Data to receive
    #   - Frozen market data is the last data recorded at market close.
    #   - Last market data is the last data set, which may be empty after hours
    aTableWidget.ib.reqMarketDataType(aTableWidget.marketDataType())

    # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
    # and create a Contract
    aSecurityType=aTableWidget.security_type(the_underlying, the_exchange)

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
        aTableWidget.an_option_spread = optionSpreadsClass.OptionSpreads(a_qualified_contract, aTableWidget.ib)
        # Fully qualify the option
        aTableWidget.an_option_spread.qualify_option_chain(aTableWidget.right(), theExpiry,
                                                           theStrikePriceRange, theStrikePriceMultiple)

        # Display the contracts
        aTableWidget.displayContracts(aTableWidget.an_option_spread.optionContracts)

        the_underlyingOutput = ' {} / Last Price: {:>7.2f}'.format(aTableWidget.an_option_spread.a_Contract.symbol,
                                                                   aTableWidget.an_option_spread.theUnderlyingReqTickerData.last)

        # Display Underlying price
        aTableWidget.lineEdit_underlying.setText(the_underlyingOutput)
        # logger.logger.info("Build Greeks")
        aTableWidget.an_option_spread.buildGreeks()

        # logger.logger.info("Display Greeks")
        aTableWidget.displayGreeks(aTableWidget.an_option_spread)
        aTableWidget.an_option_spread.buildBullPandas()
        aTableWidget.displayBullSpread(aTableWidget.an_option_spread)
        aTableWidget.an_option_spread.buildCallRatioSpread()

