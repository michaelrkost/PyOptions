from localUtilities import configIB, dateUtils, ibPyUtils, ibPyViewUtils
import optionSpreadsClass, displayVerticalSpreadViews as displayVS

# Main function to get data from "Underlying Table Widget"
# then build the Bull/Bear Spread tabs in the Vertical Spreads
def get_underlying_info(aTableWidget):
    #TODO drop/queue history/ any existing instance of contracts if new instance is created
    aTableWidget.statusbar.clearMessage()

    #clear contents for display feed back to user with a new call
    aTableWidget.tableWidget.clearContents()
    aTableWidget.tableWidget_OptionGreeks.clearContents()
    aTableWidget.tableWidget_BullCallSpread.clearContents()
    displayVS.displayProjectedVolDetailsClear(aTableWidget)

    # Set number of Contracts to 1 - this is the first calculation / 100 Units
    # 0 (Zero) should show 1 stock contract not 100
    # Todo Check if 0 is defined for one stock not 100
    aTableWidget.spinBox_numberOfContracts_BullSpread.setValue(1)

    # Get Underlying info
    the_underlying = aTableWidget.underlyingText.text()
    the_exchange = aTableWidget.comboBoxExchange.currentText()
    theStrikePriceRange = int(aTableWidget.comboBox_StrikePriceRange.currentText())
    theStrikePriceMultiple = int(aTableWidget.comboBox_StrikePriceMultiple.currentText())

    # set the type of Price Data to receive - defaults to Frozen Data
    #todo - this needs to use live or frozen - it is only set up for frozen
    ibPyUtils.reqMarketData_Setup(aTableWidget)

    # from the GUI radio buttons determine if this a Stock/Index/Option and get the underlying
    # and create a Contract
    aSecurityType = ibPyUtils.security_type(aTableWidget, the_underlying, the_exchange)

    # then if securityType == Stock get Friday Expiry if Index get Thursday Expiry
    theExpiryStr = aTableWidget.comboBox_Expiry.currentText()
    expiryDate = dateUtils.getDateFromMonthYear(theExpiryStr)
    if aTableWidget.securityType == configIB.STOCK_TYPE: #Stock - Friday Expiry
        theExpiry = dateUtils.getDateString(dateUtils.third_friday(expiryDate.year, expiryDate.month))
    else: #Index - Thurday Expiry
        theExpiry = dateUtils.getDateString(dateUtils.third_Thursday(expiryDate.year, expiryDate.month))

    # Fully qualify the given contracts in-place.
    # This will fill in the missing fields in the contract, especially the conId.
    # Returns a list of contracts that have been successfully qualified.
    try:
        # get underlying
        get_underlying = aTableWidget.ib.qualifyContracts(aSecurityType)
    except ConnectionError: # are we connected?
        aTableWidget.statusbar.showMessage("NOT CONNECTED!!! Knucklehead!!!")
        return
    if not get_underlying:  # empty list - failed qualifyContract
        aTableWidget.statusbar.showMessage("Underlying: " + the_underlying + " not recognized!")
    else:
        # display current underlying
        a_qualified_contract = get_underlying.pop()
        aTableWidget.statusbar.showMessage(str(a_qualified_contract))

        # create a new optionSpreadClass instance with the qualified contract
        aTableWidget.an_option_spread = optionSpreadsClass.OptionVerticalSpreads(a_qualified_contract, aTableWidget.ib)

        # Fully qualify the option chain
        aTableWidget.an_option_spread.qualify_option_chain(theExpiry, theStrikePriceRange, theStrikePriceMultiple)

        # Display the contracts
        displayVS.displayContracts(aTableWidget, aTableWidget.an_option_spread.optionContracts)

        # Set the Last Price for the Underlying
        the_underlyingOutput = ' {} / Last Price: {:>7.2f} // Expiry:  {}'.format(aTableWidget.an_option_spread.a_Contract.symbol,
                                                                   aTableWidget.an_option_spread.theUnderlyingReqTickerData.last,
                                                                     dateUtils.month3Format(aTableWidget.an_option_spread.theExpiration))

        # Now Display the Underlying / the Last Price / Expiration
        aTableWidget.lineEdit_underlying.setText(the_underlyingOutput)

        # Display Underlying Widget details
        displayVS.displayUnderlyingDetails(aTableWidget, theExpiry)

        # Display Projected Volatility Widget details
        displayVS.displayProjectedVolDetails(aTableWidget, theExpiry)

        # Build the Greeks in optionSpreadClass then Display
        aTableWidget.an_option_spread.buildGreeks()
        displayVS.displayGreeks(aTableWidget, aTableWidget.an_option_spread)

        # in optionSpreadClass build in the Pandas for BullVerticalSpreads & BearVerticalSpreads then Display
        aTableWidget.an_option_spread.buildPandasVerticalSpreads()
        displayVS.displayVerticalSpreads(aTableWidget, aTableWidget.an_option_spread)

        #todo buildCallRationSpread
        #aTableWidget.an_option_spread.buildCallRatioSpread()


def updateConnectVS(aTableWidget, _translate):
    """
    This sets up the button connectors i.e. QT5 connect
    lambda provides button action routine

    :param aTableWidget:
    :param _translate:
    :return:
    """

    # The button "Qualify Contracts" connects to get_underlying_info
    # which in turn builds the Spreads and populates the Widgets
    aTableWidget.qualifyContracts.clicked.connect(lambda: get_underlying_info(aTableWidget))

    # Buttons for updating Bull/Bear Spreads
    aTableWidget.pushButton_updateNumberOfContracts_BullSpread.clicked.connect(lambda: updateBullContracts(aTableWidget))
    aTableWidget.pushButton_updateNumberOfContracts_BearSpread.clicked.connect(lambda: updateBearContracts(aTableWidget))

    #Create a list of 5 Months of Option Fridays
    #for the Expiry DropDown: comboBox_Expiry
    ibPyUtils.doExpiry(aTableWidget.comboBox_Expiry, _translate)

    # Button to Connect to IB Gateway
    # todo - should be in another module it is the connection to IB Gateway?
    aTableWidget.connectToIB.triggered.connect(lambda: onConnectButtonClicked(aTableWidget))
    aTableWidget.actionVertical_Spreads.triggered.connect(lambda: aTableWidget.stackedWidget.setCurrentIndex(ibPyViewUtils.stackedWidgetView_VerticalSpread))


def updateBullContracts(aTableWidget):
    """
    Update Bull Contracts

    :param aTableWidget:
    :return:
    """
    try:
        aTableWidget.an_option_spread
    except AttributeError:
        aTableWidget.statusbar.showMessage(".....To update Bull Contracts you need to get a contract first.....")
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
    except  AttributeError:
        aTableWidget.statusbar.showMessage(".....To update Bear Contracts you need to get a contract first.....")
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

