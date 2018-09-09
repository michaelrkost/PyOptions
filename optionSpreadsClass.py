# Get my Utilities
from localUtilities import ibPyUtils, logger, dateUtils

import pandas as pd
import math

import itertools

from ib_insync import *

# using last price NOT close price throughout as close seemed to mess things up. 9/8/18 - mrk

class OptionVerticalSpreads:

    # The options Pandas builds and Calculations
    # ##### # #####
    #    -- init
    #       :param a_qualified_contract: the Contract
    #       :param anIB: the api
    # ##### # #####
    #   -- attributes
    #     ib - IB
    #     contracts - requested options based on expiry and price range then qualifyContracts(*self.contracts)
    #     theStrikes - the Strikes as defined by current price, strikePriceRange and strikePriceMultiple
    #     aTicker - the contracts ticker / a snapshot ticker of the given contract.
    #     bullCallSpreads - Pandas dataframe for spread info
    #     greekValues - Pandas dataframe for greeks/option price
    #
    putRight = 'P'
    callRight = 'C'
    rights = [putRight, callRight]
    #
    #

    # a single list is shared by all instances:
    # Headers
    # Puts / Calls
    putRight = 'P'
    callRight = 'C'
    right = [putRight, callRight]

    # Some header stuff
    headerLM = ['Loss$', 'Max$', 'Delta']
    colStrikeHL = ['StrikeL', 'StrikeH']

    # invoked for each instantiated class
    def __init__(self, a_qualified_contract, anIB):
        """init

        :param a_qualified_contract: the Contract
        :param anIB: the api
        """
        self.a_Contract = a_qualified_contract
        self.ib = anIB

        # replaced --> self.ib.reqMktData(self.a_Contract, '9,23,24,27,28,29,30')
        #   def reqMktData(self, tickerId, contract, genericTickList, snapshot):
        # 8/11/18 with this:
        # IB api / reqMktData

        self.theUnderlyingReqTickerData = self.ib.reqTickers(self.a_Contract).pop()
        self.theUnderlyingReqTickerData = self.ib.reqMktData(self.a_Contract,'100, 101, 104, 105, 106')

        # get implied volatility for this underlying out past 15days
        # use this to keep the implied volatility contract info
        self.theImpliedVolContract = []
        self.daysTillExpriy = ibPyUtils.getNearestExpiryFromToday()

        self.impliedVolatility = self.getImpliedVol(self.a_Contract.symbol, self.theUnderlyingReqTickerData.last,
                                                    self.a_Contract.exchange, self.daysTillExpriy)

        #based on Impled Vol get projected 30 & 45 day range        
        self.projected30DayRange = self.projectedVolatilityNDays(self.impliedVolatility, self.theUnderlyingReqTickerData.last, 30)
        self.projected45DayRange = self.projectedVolatilityNDays(self.impliedVolatility, self.theUnderlyingReqTickerData.last, 45)

        logger.logger.info('self.theUnderlyingReqTickerData.last:  %s', self.theUnderlyingReqTickerData.last)

        self.optionContracts = []
        self.theStrikes = []
        self.contractReqTickers = []
        self.theExpiration = []

        # greekValues = ID, Delta, TimeVal, ImpVol, Gamma, Price // was previously named optionPrices
        self.greekValues = []

        self.right = []

        # Bull Call Vertical Spreads --------------------
        self.oneBullCallVerticalSpreadOptionUnit = None
        self.oneBullPutVerticalSpreadOptionUnit = None

        self.pandasBullCallVerticalSpread = None
        self.pandasBullPutVerticalSpread = None

        # Bear Call Vertical Spreads --------------------
        self.oneBearCallVerticalSpreadOptionUnit = None
        self.oneBearPutVerticalSpreadOptionUnit = None

        self.pandasBearCallVerticalSpread = None
        self.pandasBearPutVerticalSpread = None

        # Ratio Spreads  --------------------
        self.oneCallRatioSpreadOptionUnit = None
        self.callRatioSpread = None

    def qualify_option_chain(self, anExpiry, strikePriceRange=5, strikePriceMultiple=5):
        """Fully qualify the given contracts in-place.
        This will fill in the missing fields in the contract, especially the conId.

        Update attributes: aTicker, contracts, theStrikes
        :param strikePriceRange:    Define the price range plus/minus this amount
        :param strikePriceMultiple: Define the price increment for price range
        :param anExiry: the expriration
        :return:
        """
        self.theExpiration = anExpiry

        # ----get list of options
        # reqSecDefOptParams returns a list of expires and a list of strike prices.
        # In some cases it is possible there are combinations of strike and expiry that
        # would not give a valid option contract.
        # filter on SMART / Exchange
        listOptionChain = self.ib.reqSecDefOptParams(self.a_Contract.symbol, '', self.a_Contract.secType,
                                                self.a_Contract.conId)

        listSmartOptionChain = next(c for c in listOptionChain
                                      if c.exchange == 'SMART')

        # Get the Strikes as defined by current price, strikePriceRange and strikePriceMultiple
        # Updated so no longer using close price / added last price functionality
        self.theStrikes = ibPyUtils.getStrikes(listSmartOptionChain, self.theUnderlyingReqTickerData.last,
                                       strikePriceRange, strikePriceMultiple)

        # Get the SPX expiration set and find the proper expiration
        # as it is not always the third thursday/friday
        theExpirationList = sorted(exp for exp in listSmartOptionChain.expirations
                                   if exp[:6] == self.theExpiration[:6])

        self.theExpiration = theExpirationList.pop()

        # Build requested options based on expiry and price range
        # Most common approach is to use "SMART" as the exchange
        allCallOptionContracts = [(Option(self.a_Contract.symbol, self.theExpiration, strike, ibPyUtils.call_right(),
                                        exchange='SMART', multiplier='100'))
                              for strike in self.theStrikes]

        allPutOptionContracts = [(Option(self.a_Contract.symbol, self.theExpiration, strike, ibPyUtils.put_right(),
                                        exchange='SMART', multiplier='100'))
                              for strike in self.theStrikes]

        # # Qualify the options
        self.ib.qualifyContracts(*allCallOptionContracts)
        self.ib.qualifyContracts(*allPutOptionContracts)

        # filter for Contract Numbers - remove those w/out Contract Numbers
        # and set attribute optionContracts
        # at this point self.optionContracts will have all the contracts P/C
        for c in allCallOptionContracts:
            if c.conId != 0:
                self.optionContracts.append(c)

        # filter for Contract Numbers
        # and set attribute optionContracts
        for c in allPutOptionContracts:
            if c.conId != 0:
                self.optionContracts.append(c)


    def buildPandasVerticalSpreads(self):
        """
        Build all Vertical Spreads
        - Bull - Call / Put
        - Bear - Call / Put
        :return:
        """

        headerLM = ['Loss$', 'Max$']
        colStrikeHL = ['StrikeL', 'StrikeH']

        indexRangeList = list(itertools.product(self.theStrikes, self.theStrikes))
        # indexRangeList
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList, names=colStrikeHL)

        type(multiIndexRange)

        self.pandasBullCallVerticalSpread = pd.DataFrame(0.0, index=multiIndexRange, columns=headerLM)
        self.pandasBullPutVerticalSpread = self.pandasBullCallVerticalSpread.copy(deep=True)
        self.pandasBearCallVerticalSpread = self.pandasBullCallVerticalSpread.copy(deep=True)
        self.pandasBearPutVerticalSpread = self.pandasBullCallVerticalSpread.copy(deep=True)

        self.populateBullCallVerticalSpread()
        self.populateBullPutVerticalSpread()
        self.populateBearCallVerticalSpread()
        self.populateBearPutVerticalSpread()

        # self.updateBearSpreads(self)
        # self.updateBullSpreads(self)


    def populateBullPutVerticalSpread(self):
        """
        Create & Display
        Bull Put Vertical Spread:
            OptionA  - buy a put option at a lower strike price
            OptionB  - write(sell) a put options w/a higher strike price than OptionA

        Max potential Profit: The net credit.
        Max potential Loss:   Difference between the strike prices minus the net credit
        :return:
        """
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = 0
                    self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Profit = Higher Strike - Lower Strike for net credit
                    self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] \
                        = self.greekValues.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeH), 'Price'] \
                          - self.greekValues.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeL), 'Price']

                    # Max Loss = difference between strike prices minus cost of spread ie.Loss
                    # Max Loss = (aStrikeH - aStrikeL) - Max Loss
                    self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$']
        self.oneBullPutVerticalSpreadOptionUnit = self.pandasBullPutVerticalSpread.copy(deep=True)
        self.pandasBullPutVerticalSpread.update(self.oneBullPutVerticalSpreadOptionUnit.loc[:, :] * (100*1))


    def populateBullCallVerticalSpread(self):
        """
        Create & Display  -mrk 8/13/18                  _
        Bull Call Vertical Spread / Debit Call Spread _/
            OptionA/aStrikeL  - buy a long Call option
            OptionB/aStrikeH  - write(sell) a short Call options at a higher strike price than OptionA

        Max Profit: Difference between strike A and strike B minus the Net Debit paid.
        Max Loss:   Net Debit
        :return:
        """
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = 0
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Loss is the Net Debit ----
                    # Difference between (OptionB/aStrikeH Net Credit / Price) and (Cost/Price of OptionA/aStrikeL)
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] \
                        = self.greekValues.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeL), 'Price'] \
                          - self.greekValues.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeH), 'Price']

                    # Max Profit = difference between strike prices minus Net Debit ie.Loss
                    # Max Profit = (aStrikeH - aStrikeL) - Net Debit/Loss$
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$']
        self.oneBullCallVerticalSpreadOptionUnit = self.pandasBullCallVerticalSpread.copy(deep=True)
        self.pandasBullCallVerticalSpread.update(self.oneBullCallVerticalSpreadOptionUnit.loc[:, :] * (100 * 1))


    def populateBearPutVerticalSpread(self):
        """
        Create & Display - mrk 8/13/18
        Bear Call Vertical Spread / Debit Spread
            OptionA - aStrikeH - buy a 1 long Put option
            OptionB - aStrikeL - write(sell) a short Put options at a lower strike price than OptionA

        Max Profit: Difference between aStrikeH and aStrikeL minus the Net Debit paid
        Max Loss:   Net Debit
        :return:
        """
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.pandasBearPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = 0
                    self.pandasBearPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Loss is the Net Debit ----
                    # Difference between (OptionB/aStrikeH Net Credit/Price) and (Cost/Price of OptionA/aStrikeL)
                    self.pandasBearPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] \
                        = self.greekValues.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeH), 'Price'] \
                          - self.greekValues.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeL), 'Price']

                    # Max Profit = difference between strike prices minus Net Debit ie.Loss
                    # Max Profit = (aStrikeH - aStrikeL) - Net Debit/Loss$
                    self.pandasBearPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBearPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$']
        self.oneBearPutVerticalSpreadOptionUnit = self.pandasBearPutVerticalSpread.copy(deep=True)
        self.pandasBearPutVerticalSpread.update(self.oneBearPutVerticalSpreadOptionUnit.loc[:, :] * (100*1))

    def populateBearCallVerticalSpread(self):
        """
        Create & Display - mrk 8/13/18
        Bear Call Vertical Spread / Credit Spread
            OptionA - aStrikeH - buy 1 long Put option at a higher strike price than OptionB
            OptionB - aStrikeL - write(sell) short Put option at a lower strike price than OptionA

        Max Profit: The Net Credit.
        Max Loss:   Difference between the strike prices minus the net credit
        :return:
        """
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.pandasBearCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = 0
                    self.pandasBearCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Profit is the Net Credit ----
                    # Difference between (Option/aStrikeL Net Credit/Price) and (Cost/Price of OptionA/aStrikeH)
                    self.pandasBearCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] \
                        = self.greekValues.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeL), 'Price'] \
                          - self.greekValues.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeH), 'Price']

                    # Max Loss = difference between strike prices minus Net Debit ie.Loss
                    # Max Loss = (aStrikeH - aStrikeL) - Max Loss
                    self.pandasBearCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBearCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$']
        self.oneBearCallVerticalSpreadOptionUnit = self.pandasBearCallVerticalSpread.copy(deep=True)
        self.pandasBearCallVerticalSpread.update(self.oneBearCallVerticalSpreadOptionUnit.loc[:, :] * (100*1))

    def updateBullSpreads(self, contracts=1):

        # using 0 to see the option price -
        # one unit will show the single option price
        # TODO make sure this is working w/0
        if contracts == 0:
            numberOfUnits = 1
        else:
            numberOfUnits = 100

        self.pandasBullCallVerticalSpread.update(self.oneBullCallVerticalSpreadOptionUnit.loc[:, :] * (numberOfUnits * contracts))
        self.pandasBullPutVerticalSpread.update(self.oneBullPutVerticalSpreadOptionUnit.loc[:, :] * (numberOfUnits * contracts))

    def updateBearSpreads(self, contracts=1):

        # using 0 to see the option price -
        # one unit will show the single option price
        # TODO make sure this is working w/0
        if contracts == 0:
            numberOfUnits = 1
        else:
            numberOfUnits = 100

        self.pandasBearCallVerticalSpread.update(self.oneBearCallVerticalSpreadOptionUnit.loc[:, :] * (numberOfUnits * contracts))
        self.pandasBearPutVerticalSpread.update(self.oneBearPutVerticalSpreadOptionUnit.loc[:, :] * (numberOfUnits * contracts))

    def buildGreeks(self):
        """
        Create Panda DF for Greeks add Greeks to DF
        :return:
        """
        headerPrice = ['ID', 'Price', 'ImpliedVol', 'Gamma', 'Delta', 'TimeVal']
        indexRangeList = list(itertools.product(self.right, [self.theExpiration], self.theStrikes))
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList,
                                                    names=['Right', 'Expiry', 'Strike'])

        self.greekValues = pd.DataFrame(0.0, index=multiIndexRange,
                                        columns=headerPrice)

        logger.logger.info("Processing Greeks")

        for aContract in self.optionContracts:
            [theReqTicker] = self.ib.reqTickers(aContract)
            theGreeks = theReqTicker.modelGreeks
            self.contractReqTickers.append(theReqTicker)

            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'ID'] = aContract.conId

            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Delta'] = theGreeks.delta
            # close is yesterdays close - mess up calculations
            #An option's time value is equal to its premium (the cost of the option) minus its intrinsic value
            # (the difference between the strike price and the price of the underlying).
            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'TimeVal'] = theReqTicker.last - abs(self.theUnderlyingReqTickerData.last
                                                                             - aContract.strike)
            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'ImpliedVol'] = theGreeks.impliedVol
            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Gamma'] = theGreeks.gamma
            self.greekValues.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Price'] = theReqTicker.last

        logger.logger.info('=== Greeks Built =========')

    def buildCallRatioSpread(self):

        headerLM = ['BreakEven$', 'Max$']
        colStrikeHL = ['Buy ATM', 'Sell Higher OTM']

        indexRangeList = list(itertools.product(self.theStrikes, self.theStrikes))
        indexRangeList
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList, names=colStrikeHL)
        logger.logger.info("buildCallRatioSpread")


        self.callRatioSpread = pd.DataFrame(0.0, index=multiIndexRange, columns=headerLM)

        self.populateCallRatioSpread()


    def populateCallRatioSpread(self):
        """
        Front Ratio Call Spread
            A Call Front Ratio Spread is a neutral to bullish strategy that is created by
            purchasing a call debit spread with an additional short call at the short strike
            of the debit spread. The strategy is generally placed for a net credit so that
            there is no downside risk.

        Directional Assumption: Neutral to slightly bullish

        Setup:
            - Buy an ATM or OTM call option
            - Sell two further OTM call options at a higher strike

        Ideal Implied Volatility Environment : High

        Max Profit: Distance between long strike and short strike + credit received

        How to Calculate Breakeven(s): Short call strike + max profit potential
        :return:
        """

        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'BreakEven$'] = 0
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Profit: Distance  between long strike and short strike + credit received
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$'] \
                        = abs(aStrikeH - aStrikeL) \
                          + ((self.greekValues.loc[(self.right, self.theExpiration, aStrikeH), 'Price'] * 2)
                             - self.greekValues.loc[(self.right, self.theExpiration, aStrikeL), 'Price'])

                    # Breakeven(s): Short call strike + max profit potential
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'BreakEven$'] \
                        = self.greekValues.loc[(self.right, self.theExpiration, aStrikeH), 'Price'] + \
                          self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$']

        self.oneCallRatioSpreadOptionUnit = self.callRatioSpread.copy(deep=True)
        self.updateCallRatioSpread()

    def updateCallRatioSpread(self, contracts=1):

        self.callRatioSpread.update(self.callRatioSpread.loc[:, :] * (100 * contracts))

    def getImpliedVol(self, theSymbol, theLast, theExchange, theExpiry):

        nearest5StrikePrice = ibPyUtils.roundToNearest5(theLast)

        self.theImpliedVolContract = Option(theSymbol, theExpiry, nearest5StrikePrice, 'C', theExchange)

        [ticker] = self.ib.reqTickers(self.theImpliedVolContract)

        return ticker.modelGreeks.impliedVol

    def projectedVolatilityNDays(self, impliedVol, stockPrice, projectedDays):
        """
        Deannualize IV turn into a one day figure
        1-Day expected Vol = Implied Volatility  sqrt(number of trading Days in Year)
        projectedDays Expected Vol = 1-Day expected Vol * sqrt(projectedDays)

        The expected movement of a stock can be calculated with the following formula, where S subscript 0 is
        the stock's current price, IV is implied volatility, and the final term is the square root of days
        to expiration divided by 365.

        projectedVolatilityNDays = stock current price * IV * sqrt(projectedDays/daysInYear)

        :return: 
        """

        projected = stockPrice* impliedVol * math.sqrt(projectedDays / dateUtils.daysInYear())

        return projected



































