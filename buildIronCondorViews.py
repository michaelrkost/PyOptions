
from PyQt5 import QtGui, QtWidgets
from ib_insync import *

from localUtilities import configIB, dateUtils, ibPyUtils, ibPyViewUtils
import optionSpreadsClass


def updateConnectIC(aTableWidget, _translate):
    aTableWidget.qualifyIronCondor.clicked.connect(lambda: get_underlying_info(aTableWidget))

    ibPyUtils.doExpiry(aTableWidget.comboBox_Expiry_IC, _translate)
    # aTableWidget.pushButton_updateNumberOfContracts.clicked.connect(lambda: updateBullContracts(aTableWidget))
    #
    # aTableWidget.connectToIB.triggered.connect(lambda: onConnectButtonClicked(aTableWidget))
    aTableWidget.actionIron_Condor.triggered.connect(lambda: aTableWidget.stackedWidget.setCurrentIndex(ibPyViewUtils.stackedWidgetView_IronCondor))

def get_underlying_info(aTableWidget):
    #TODO drop/queue history/ any existing instance of contracts if new instance is created
    #TODO filter out or combine Weekly or Monthly at the UI level
    aTableWidget.statusbar.clearMessage()

    the_underlying = aTableWidget.underlyingText_IC.text()
    the_exchange = aTableWidget.comboBoxExchange_IC.currentText()
    theStrikePriceRange = int(aTableWidget.comboBox_StrikePriceRange_IC.currentText())
    theStrikePriceMultiple = int(aTableWidget.comboBox_StrikePriceMultiple_IC.currentText())

    # set the type of Price Data to receive
    #   - Frozen market data is the last data recorded at market close.
    #   - Last market data is the last data set, which may be empty after hours
    aTableWidget.ib.reqMarketDataType(ibPyUtils.marketDataType(aTableWidget.radioButton_MktDataType_Frozen_IC))
    print("frozenIC: ", aTableWidget.radioButton_MktDataType_Frozen_IC.isChecked())

    # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
    # and create a Contract
    aSecurityType = ibPyUtils.security_type(aTableWidget, the_underlying, the_exchange)

    # then if securityType == Stock get Friday Expiry if Index get Thursday Expiry
    theExpiry = aTableWidget.comboBox_Expiry_IC.currentText()
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
        aTableWidget.an_option_spread.qualify_option_chain(theExpiry, theStrikePriceRange, theStrikePriceMultiple)

        print("a_qualified_contract:  " , a_qualified_contract)