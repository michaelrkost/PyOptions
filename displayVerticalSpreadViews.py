
from PyQt5 import QtGui, QtWidgets
from ib_insync import *

from localUtilities import dateUtils


# All the table trimmings for the Vertical Spread View

def trimTable(tableWidget, tableWidget_OptionGreeks, tableWidget_BullPutSpread, tableWidget_BullCallSpread,
              tableWidget_BearCallSpread, tableWidget_BearPutSpread):

    headers = ['ID', 'Symbol', 'Expriy', 'Strike', 'Right']
    tableWidget.setColumnCount(len(headers))
    tableWidget.setHorizontalHeaderLabels(headers)
    tableWidget.setAlternatingRowColors(True)

    headerGreeks = ['ID', 'Right', 'Expiry', 'Strike', 'Price', 'ImpliedVol', 'Gamma',
                    'Delta', 'TimeVal']
    tableWidget_OptionGreeks.setHorizontalHeaderLabels(headerGreeks)
    tableWidget_OptionGreeks.setAlternatingRowColors(True)

    headerBullSpread = ['Strike Low/Buy', 'Strike High/Sell', 'Max$ Loss', 'Max$ Profit']

    tableWidget_BullCallSpread.setHorizontalHeaderLabels(headerBullSpread)
    tableWidget_BullCallSpread.setAlternatingRowColors(True)

    tableWidget_BullPutSpread.setHorizontalHeaderLabels(headerBullSpread)
    tableWidget_BullPutSpread.setAlternatingRowColors(True)

    tableWidget_BearPutSpread.setHorizontalHeaderLabels(headerBullSpread)
    tableWidget_BearPutSpread.setAlternatingRowColors(True)

    tableWidget_BearCallSpread.setHorizontalHeaderLabels(headerBullSpread)
    tableWidget_BearCallSpread.setAlternatingRowColors(True)


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

    # calculate the number of table rows needed
    greeksLen = len(contracts.optionContracts)

    aTableWidget.tableWidget_OptionGreeks.setRowCount(greeksLen)
    aTableWidget.tableWidget_OptionGreeks.clearContents()

    # Items are created outside the table (with no parent widget)
    # and inserted into the table with setItem():
    theRow = 0

    # get the properly formated Expiry "Aug'16'18"
    anExpriy = contracts.theExpiration

    # for P and C in contracts.rights do
    for aRight in contracts.rights:
        for aStrike in contracts.theStrikes:
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 0, QtWidgets.QTableWidgetItem(
                '{:d}'.format(int(contracts.greekValues.loc[(aRight, anExpriy, aStrike), 'ID']))))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 1, QtWidgets.QTableWidgetItem(aRight))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 2,
                                                  QtWidgets.QTableWidgetItem(dateUtils.month3Format(anExpriy)))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 3, QtWidgets.QTableWidgetItem(str(aStrike)))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 4, QtWidgets.QTableWidgetItem(
                '{:>7.2f}'.format(contracts.greekValues.loc[(aRight, anExpriy, aStrike),'Price'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 5, QtWidgets.QTableWidgetItem(
                '{:>2.2%}'.format(contracts.greekValues.loc[(aRight, anExpriy, aStrike),'ImpliedVol'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 6, QtWidgets.QTableWidgetItem(
                '{:>.6f}'.format(contracts.greekValues.loc[(aRight, anExpriy, aStrike), 'Gamma'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 7, QtWidgets.QTableWidgetItem(
                '{:>.6f}'.format(contracts.greekValues.loc[(aRight, anExpriy, aStrike), 'Delta'])))
            aTableWidget.tableWidget_OptionGreeks.setItem(theRow, 8, QtWidgets.QTableWidgetItem(
                '{:>7.2f}'.format(contracts.greekValues.loc[(aRight, anExpriy, aStrike),'TimeVal'])))

            theRow += 1

def displayVerticalSpreads(aTableWidget, contracts):
    """
    Display all Vertical Spreads
    - Bull - Call / Put
    - Bear - Call / Put
    :return:
    """

    displayTheVerticalSpreads(aTableWidget.tableWidget_BullCallSpread, contracts.pandasBullCallVerticalSpread,
                           contracts.theStrikes)

    displayTheVerticalSpreads(aTableWidget.tableWidget_BullPutSpread, contracts.pandasBullPutVerticalSpread,
                           contracts.theStrikes)

    displayTheVerticalSpreads(aTableWidget.tableWidget_BearCallSpread, contracts.pandasBearCallVerticalSpread,
                           contracts.theStrikes)

    displayTheVerticalSpreads(aTableWidget.tableWidget_BearPutSpread, contracts.pandasBearPutVerticalSpread,
                           contracts.theStrikes)

    # displayBullCallVerticalSpread(aTableWidget, contracts)
    # displayBullPutVerticalSpread(aTableWidget, contracts)
    #
    # displayBearCallVerticalSpread(aTableWidget, contracts)
    # displayBearPutVerticalSpread(aTableWidget, contracts)

def displayTheVerticalSpreads(aSpread, contractVS, contractsTheStrikes):

    aSpread.setRowCount(contractVS.shape[0])

    aSpread.clearContents()

    theRow = 0
    for aStrikeL in contractsTheStrikes:
        aSpread.setItem(theRow, 0, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeL)))
        aSpread.item(theRow, 0).setBackground(QtGui.QColor("lightBlue"))
        for aStrikeH in contractsTheStrikes:
            if aStrikeL < aStrikeH:
                aSpread.setItem(theRow, 1, QtWidgets.QTableWidgetItem('{:>d}'.format(aStrikeH)))
                aSpread.setItem(theRow, 2, QtWidgets.QTableWidgetItem(
                                                    '{:>7.2f}'.format(contractVS.loc[(aStrikeL, aStrikeH),'Loss$'])))
                aSpread.setItem(theRow, 3,QtWidgets.QTableWidgetItem(
                                                    '{:>7.2f}'.format(contractVS.loc[(aStrikeL, aStrikeH),'Max$'])))
                theRow += 1


def displayUnderlyingDetails(aTableWidget, expiryDate):

    aTableWidget.stockLast.setText('{:>7.2f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.last))

    aTableWidget.stockClose.setText('{:>7.2f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.close))

    aTableWidget.putOpenInterest.setText('{:>7.0f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.putOpenInterest))

    aTableWidget.callOpenInterest.setText('{:>7.0f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.callOpenInterest))

    totalOpenInterest = aTableWidget.an_option_spread.theUnderlyingReqTickerData.callOpenInterest + \
                        aTableWidget.an_option_spread.theUnderlyingReqTickerData.putOpenInterest
    aTableWidget.totalOpenInterest.setText('{:>7.0f}'.format(totalOpenInterest))

    aTableWidget.callVolume.setText('{:>7.0f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.callVolume))

    aTableWidget.putVolume.setText('{:>7.0f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.putVolume))

    theTotalVolume = aTableWidget.an_option_spread.theUnderlyingReqTickerData.putVolume + \
               aTableWidget.an_option_spread.theUnderlyingReqTickerData.callVolume
    aTableWidget.totalVolume.setText('{:>7.0f}'.format(theTotalVolume))

    aTableWidget.daysToExpiry.setText('{:>7.0f}'.format(dateUtils.daysToExpiry(expiryDate)))

    aTableWidget.impliedVol.setText('{:.2%}'.format(aTableWidget.an_option_spread.impliedVolatility))


def displayProjectedVolDetails(aTableWidget, expiryDate):

    the30DayVol = (aTableWidget.an_option_spread.projected30DayRange /
                   aTableWidget.an_option_spread.theUnderlyingReqTickerData.last)
    the45DayVol = (aTableWidget.an_option_spread.projected45DayRange /
                    aTableWidget.an_option_spread.theUnderlyingReqTickerData.last)
    the30DayUSD = aTableWidget.an_option_spread.projected30DayRange
    the45DayUSD = aTableWidget.an_option_spread.projected45DayRange

    # set Volatility %
    aTableWidget.VolPercent_30Day.setText('{:.2%}'.format(the30DayVol))
    aTableWidget.VolPercent_45Day.setText('{:.2%}'.format(the45DayVol))

    #Set Volatility USD %
    aTableWidget.volUSD_30Day.setText('{:>7.2f}'.format(the30DayUSD))
    aTableWidget.volUSD_45Day.setText('{:>7.2f}'.format(the45DayUSD))


    aTableWidget.percentRange_30Day.setText('{:.2%}'.format(the30DayVol /2))
    aTableWidget.percentRange_45Day.setText('{:.2%}'.format( the45DayVol/2))

    aTableWidget.dollarRange_30Day.setText('{:>7.2f}'.format(the30DayUSD/2))
    aTableWidget.dollarRange_45Day.setText('{:>7.2f}'.format(the45DayUSD/2))

    aTableWidget.dollarRangeUp_30Day.setText('{:>7.2f}'.format((the30DayUSD/2)
                                                               + aTableWidget.an_option_spread.theUnderlyingReqTickerData.last))
    aTableWidget.dollarRangeUp_45Day.setText('{:>7.2f}'.format((the45DayUSD/2)
                                                               + aTableWidget.an_option_spread.theUnderlyingReqTickerData.last))

    aTableWidget.dollarRangeDown_30Day.setText('{:>7.2f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.last
                                                                 - (the30DayUSD/2)))
    aTableWidget.dollarRangeDown_45Day.setText('{:>7.2f}'.format(aTableWidget.an_option_spread.theUnderlyingReqTickerData.last
                                                                 - (the45DayUSD / 2)))

def displayProjectedVolDetailsClear(aTableWidget):

    # set Volatility %
    aTableWidget.VolPercent_30Day.clear()
    aTableWidget.VolPercent_45Day.clear()

    #Set Volatility USD %
    aTableWidget.volUSD_30Day.clear()
    aTableWidget.volUSD_45Day.clear()


    aTableWidget.percentRange_30Day.clear()
    aTableWidget.percentRange_45Day.clear()

    aTableWidget.dollarRange_30Day.clear()
    aTableWidget.dollarRange_45Day.clear()

    aTableWidget.dollarRangeUp_30Day.clear()
    aTableWidget.dollarRangeUp_45Day.clear()

    aTableWidget.dollarRangeDown_30Day.clear()
    aTableWidget.dollarRangeDown_45Day.clear()

