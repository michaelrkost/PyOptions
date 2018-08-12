

from localUtilities import configIB, dateUtils, ibPyUtils, ibPyViewUtils
import optionSpreadsClass, displayVerticalSpreadViews as displayVS


def get_underlying_info(aTableWidget):
    #TODO drop/queue history/ any existing instance of contracts if new instance is created
    #TODO filter out or combine Weekly or Monthly at the UI level
    aTableWidget.statusbar.clearMessage()

    #clear contents for feed back to user - new call
    aTableWidget.tableWidget.clearContents()
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    aTableWidget.tableWidget_BullCallSpread.clearContents()
    aTableWidget.spinBox_numberOfContracts_BullSpread.setValue(1)

    the_underlying = aTableWidget.underlyingText.text()
    the_exchange = aTableWidget.comboBoxExchange.currentText()
    theStrikePriceRange = int(aTableWidget.comboBox_StrikePriceRange.currentText())
    theStrikePriceMultiple = int(aTableWidget.comboBox_StrikePriceMultiple.currentText())

    ibPyUtils.reqMarketData_Setup(aTableWidget)

    # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
    # and create a Contract
    aSecurityType = ibPyUtils.security_type(aTableWidget, the_underlying, the_exchange)

    # then if securityType == Stock get Friday Expiry if Index get Thursday Expiry
    theExpiryStr = aTableWidget.comboBox_Expiry.currentText()
    expiryDate = dateUtils.getDateFromMonthYear(theExpiryStr)
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

        # create a new optionSpreadClass instance
        aTableWidget.an_option_spread = optionSpreadsClass.OptionVerticalSpreads(a_qualified_contract, aTableWidget.ib)

        # Fully qualify the options
        aTableWidget.an_option_spread.qualify_option_chain(theExpiry, theStrikePriceRange, theStrikePriceMultiple)

        # Display the contracts
        displayVS.displayContracts(aTableWidget, aTableWidget.an_option_spread.optionContracts)

        # Get the Last Price for the Underlying
        the_underlyingOutput = ' {} / Last Price: {:>7.2f}'.format(aTableWidget.an_option_spread.a_Contract.symbol,
                                                                   aTableWidget.an_option_spread.theUnderlyingReqTickerData.last)
        # SetText /pyQt5 the Last Price Underlying price
        aTableWidget.lineEdit_underlying.setText(the_underlyingOutput)

        # Display underlying details
        displayVS.displayUnderlyingDetails(aTableWidget, theExpiry)

        # set in str the volPercent30Day
        buildProjectedVolatility(aTableWidget, theExpiry)

        # Build the Greeks in optionSpreadClass then Display
        aTableWidget.an_option_spread.buildGreeks()
        displayVS.displayGreeks(aTableWidget, aTableWidget.an_option_spread)

        # Build the BullVerticalSpreads & BearVerticalSpreads in optionSpreadClass then Display
        aTableWidget.an_option_spread.buildPandasVerticalSpreads()

        displayVS.displayVerticalSpreads(aTableWidget, aTableWidget.an_option_spread)

        #aTableWidget.an_option_spread.buildCallRatioSpread()



def updateConnectVS(aTableWidget, _translate):
    """
    This sets up the button connectors i.e. connect
    lambda provides button action routine

    :param aTableWidget:
    :param _translate:
    :return:
    """

    # Button to Connect to IB Gateway
    aTableWidget.qualifyContracts.clicked.connect(lambda: get_underlying_info(aTableWidget))


    aTableWidget.pushButton_updateNumberOfContracts_BullSpread.clicked.connect(lambda: updateBullContracts(aTableWidget))
    aTableWidget.pushButton_updateNumberOfContracts_BearSpread.clicked.connect(lambda: updateBearContracts(aTableWidget))

    #Create a list of 18 Months of Option Fridays
    #for the Expiry DropDown: comboBox_Expiry
    ibPyUtils.doExpiry(aTableWidget.comboBox_Expiry, _translate)

    # todo - this should be in another module it is IB Connections...
    # Button to Start the program
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
        theContractCount = aTableWidget.spinBox_numberOfContracts_BullSpread.value()
        aTableWidget.an_option_spread.updateBullSpreads(theContractCount)
        displayVS.displayVerticalSpreads(aTableWidget, aTableWidget.an_option_spread)
        #aTableWidget.an_option_spread.updateCallRatioSpread(theContractCount)

def updateBearContracts(aTableWidget):
    """

    :param aTableWidget:
    :return:
    """
    try:
        aTableWidget.an_option_spread
    except NameError:
        aTableWidget.statusbar.showMessage(".....need to get a contract first.....")
    else:
        theContractCount = aTableWidget.spinBox_numberOfContracts_BearSpread.value()
        aTableWidget.an_option_spread.updateBearSpreads(theContractCount)
        displayVS.displayVerticalSpreads(aTableWidget, aTableWidget.an_option_spread)
        #aTableWidget.an_option_spread.updateCallRatioSpread(theContractCount)


def onConnectButtonClicked(self):
    if self.connectToIB.isChecked():
        self.ib.connect(configIB.IB_API_HOST,
                    configIB.IB_PAPER_TRADE_PORT,
                    configIB.IB_API_CLIENTID_1)

        self.statusbar.showMessage("Connected to IB Paper and client #1")
    else:
        self.ib.disconnect()
        self.statusbar.showMessage("Disconnected from IB")

def buildProjectedVolatility(aTableWidget, expiryDate):

    volPercent30Day = '{}'.format(aTableWidget.an_option_spread.a_Contract.symbol)
    aTableWidget.VolPercent_30Day.setText(volPercent30Day)

