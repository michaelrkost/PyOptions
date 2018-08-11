# Get my Utilities
from localUtilities import ibPyUtils, logger

import pandas as pd

import itertools

from ib_insync import *

class OptionVerticalSpreads:

    # all the options Pandas builds and Calculations
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
    #     optionPrices - Pandas dataframe for greeks/option price
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
        self.theUnderlyingReqTickerData = self.ib.reqTickers(self.a_Contract).pop()
        logger.logger.info('self.theUnderlyingReqTickerData.last:  %s', self.theUnderlyingReqTickerData.last)
        self.optionContracts = []
        self.theStrikes = []
        self.contractReqTickers = []
        self.theExpiration = []
        self.optionPrices = [] #todo change name to greekValues
        self.right = []
        self.oneBullCallVerticalSpreadOptionUnit = None
        self.oneBullPutVerticalSpreadOptionUnit = None
        self.oneCallRatioSpreadOptionUnit = None
        self.pandasBullCallVerticalSpread = None
        self.pandasBullPutVerticalSpread = None
        self.callRatioSpread = None

    def qualify_option_chain(self, anExpiry, strikePriceRange=5, strikePriceMultiple=5):
        """Fully qualify the given contracts in-place. close not last
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
        listOptionChain = self.ib.reqSecDefOptParams(self.a_Contract.symbol, '', self.a_Contract.secType,
                                                self.a_Contract.conId)

        listSmartOptionChain = next(c for c in listOptionChain
                                      if c.exchange == 'SMART')

        # Get the Strikes as defined by current price, strikePriceRange and strikePriceMultiple
        # Updated so not using close price / added last price functionality
        self.theStrikes = ibPyUtils.getStrikes(listSmartOptionChain, self.theUnderlyingReqTickerData.last,
                                       strikePriceRange, strikePriceMultiple)

        #todo need to put in more logic to get existing expiries as they do not extend out logically
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

        # filter for Contract Numbers
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

        print(self.optionContracts)


    def buildPandasBullVerticalSpreads(self):

        headerLM = ['Loss$', 'Max$']
        colStrikeHL = ['StrikeL', 'StrikeH']

        indexRangeList = list(itertools.product(self.theStrikes, self.theStrikes))
        # indexRangeList
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList, names=colStrikeHL)
        # print("\nmultiIndexRange\n", multiIndexRange)
        type(multiIndexRange)

        self.pandasBullCallVerticalSpread = pd.DataFrame(0.0, index=multiIndexRange, columns=headerLM)
        self.pandasBullPutVerticalSpread = self.pandasBullCallVerticalSpread.copy(deep=True)

        # todo remove all unnecessary print outs
        # todo determine how to use logging
        # print('bullCallSpreads\n', self.bullCallSpreads)
        self.populateBullCallVerticalSpread()
        self.populateBullPutVerticalSpread()
        # print('POP bullCallSpreads\n', self.bullCallSpreads)

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
                        = self.optionPrices.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeH), 'Price'] \
                          - self.optionPrices.loc[(ibPyUtils.put_right(), self.theExpiration, aStrikeL), 'Price']

                    # Max Loss = difference between strike prices minus cost of spread ie.Loss
                    # Max Loss = (aStrikeH - aStrikeL) - Max Loss
                    self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBullPutVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$']
        self.oneBullPutVerticalSpreadOptionUnit = self.pandasBullPutVerticalSpread.copy(deep=True)
        self.pandasBullPutVerticalSpread.update(self.oneBullCallVerticalSpreadOptionUnit.loc[:, :] * (100 * 1))


    def populateBullCallVerticalSpread(self):
        """
        Create & Display
        Long Call Vertical Spread:
            OptionA - buy a call option
            OptionB  - write(sell) a call options w/a higher strike price than OptionA

        Max potential Profit: Difference between strike A and strike B minus the net debit paid.
        Max potential Loss:   Net Debit
        :return:
        """
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] = 0
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Loss is the (cost of aStrikeH) plus (aStrikeL profit)
                    # Max Loss = -(aStrikeH.Price) + aStrikeL.price
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$'] \
                        = self.optionPrices.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeL), 'Price'] \
                          - self.optionPrices.loc[(ibPyUtils.call_right(), self.theExpiration, aStrikeH), 'Price']

                    # Max Profit = difference between strike prices minus cost of spread ie.Loss
                    # Max Profit = (aStrikeH - aStrikeL) - Max Loss
                    self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = \
                        (aStrikeH - aStrikeL) - self.pandasBullCallVerticalSpread.loc[(aStrikeL, aStrikeH), 'Loss$']
        self.oneBullCallVerticalSpreadOptionUnit = self.pandasBullCallVerticalSpread.copy(deep=True)
        self.pandasBullCallVerticalSpread.update(self.oneBullCallVerticalSpreadOptionUnit.loc[:, :] * (100 * 1))

    def updateBullSpreads(self, contracts=1):

        self.pandasBullCallVerticalSpread.update(self.oneBullCallVerticalSpreadOptionUnit.loc[:, :] * (100 * contracts))
        self.pandasBullPutVerticalSpread.update(self.oneBullPutVerticalSpreadOptionUnit.loc[:, :] * (100 * contracts))

    def buildGreeks(self):
        """
        Create Panda DF for Greeks add Greeks to DF
        :return:
        """
        headerPrice = ['ID', 'Price', 'ImpliedVol', 'Gamma', 'Delta', 'TimeVal']
        indexRangeList = list(itertools.product(self.right, [self.theExpiration], self.theStrikes))
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList,
                                                    names=['Right', 'Expiry', 'Strike'])
        #print('\nmultiIndexRange:\n ', multiIndexRange)
        self.optionPrices = pd.DataFrame(0.0, index=multiIndexRange,
                                         columns=headerPrice)
        print('\noptionPrices\n', self.optionPrices)
        print("\nProcessing Greeks", end="")

        for aContract in self.optionContracts:
            [theReqTicker] = self.ib.reqTickers(aContract)
            theGreeks = theReqTicker.modelGreeks
            self.contractReqTickers.append(theReqTicker)

            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'ID'] = aContract.conId

            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Delta'] = theGreeks.delta
            # close is yesterdays close - mess up calculations
            #An option's time value is equal to its premium (the cost of the option) minus its intrinsic value
            # (the difference between the strike price and the price of the underlying).
            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'TimeVal'] = theReqTicker.last - abs(self.theUnderlyingReqTickerData.last
                                                                             - aContract.strike)
            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'ImpliedVol'] = theGreeks.impliedVol
            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Gamma'] = theGreeks.gamma
            self.optionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Price'] = theReqTicker.last

        print("self.optionPrinces\n", self.optionPrices)
        logger.logger.info('=== Greeks Built =========')

    def buildCallRatioSpread(self):

        headerLM = ['BreakEven$', 'Max$']
        colStrikeHL = ['Buy ATM', 'Sell Higher OTM']

        indexRangeList = list(itertools.product(self.theStrikes, self.theStrikes))
        indexRangeList
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList, names=colStrikeHL)
        logger.logger.info("buildCallRatioSpread")


        self.callRatioSpread = pd.DataFrame(0.0, index=multiIndexRange, columns=headerLM)

        # todo remove all unnecessary print outs
        # todo determine how to use logging
        # print('bullCallSpreads\n', self.bullCallSpreads)
        self.populateCallRatioSpread()
        # print('POP bullCallSpreads\n', self.bullCallSpreads)

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

        # todo does this work for Puts???
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'BreakEven$'] = 0
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$'] = 0
                else:
                    # Max Profit: Distance  between long strike and short strike + credit received
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$'] \
                        = abs(aStrikeH - aStrikeL) \
                          + ((self.optionPrices.loc[(self.right, self.theExpiration, aStrikeH), 'Price'] *2 )
                             - self.optionPrices.loc[(self.right, self.theExpiration, aStrikeL), 'Price'])

                    # Breakeven(s): Short call strike + max profit potential
                    self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'BreakEven$'] \
                        = self.optionPrices.loc[(self.right, self.theExpiration, aStrikeH), 'Price'] + \
                          self.callRatioSpread.loc[(aStrikeL, aStrikeH), 'Max$']

        self.oneCallRatioSpreadOptionUnit = self.callRatioSpread.copy(deep=True)
        self.updateCallRatioSpread()

    def updateCallRatioSpread(self, contracts=1):

        self.callRatioSpread.update(self.callRatioSpread.loc[:, :] * (100 * contracts))

































