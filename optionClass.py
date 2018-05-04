# Get my Utilities
from localUtilities import dateUtils, ibPyUtils, configIB

import numpy as np
import pandas as pd
import datetime
import random
import itertools
import math

from ib_insync import *

class OptionSpreads:

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
    #     closeOptionPrices - Pandas dataframe for greeks/option price
    #
    # putRight = 'P'
    # callRight = 'C'
    # rights = [putRight, callRight]
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
    def __init__(self,a_qualified_contract, anIB):
        """init

        :param a_qualified_contract: the Contract
        :param anIB: the api
        """
        self.a_Contract = a_qualified_contract
        self.ib = anIB
        self.theUnderlyingReqTickerData = self.ib.reqTickers(self.a_Contract).pop()
        print('self.theUnderlyingReqTickerData.close:  ', self.theUnderlyingReqTickerData.close)
        self.optionContracts = []
        self.theStrikes =[]
        self.contractReqTickers = []
        self.theExpiration = []
        self.closeOptionPrices = []
        self.right = []

    def qualify_option_chain(self, aRight, anExpiry, strikePriceRange=5, strikePriceMultiple=5):
        """Fully qualify the given contracts in-place. close not last
        This will fill in the missing fields in the contract, especially the conId.

        Update attributes: aTicker, contracts, theStrikes
        :param strikePriceRange:    Define the price range plus/minus this amount
        :param strikePriceMultiple: Define the price increment for price range
        :param anExiry: the expriration
        :return:
        """
        self.theExpiration = anExpiry
        self.right = aRight
        # ----get list of options
        # reqSecDefOptParams returns a list of expires and a list of strike prices.
        # In some cases it is possible there are combinations of strike and expiry that
        # would not give a valid option contract.
        listOptionChain = self.ib.reqSecDefOptParams(self.a_Contract.symbol, '', self.a_Contract.secType,
                                                self.a_Contract.conId)
        # print('>>> listOptionChain: \n', listOptionChain)

        listSmartOptionChain = next(c for c in listOptionChain
                                      if c.exchange == 'SMART')

        print("\n>>> listSmartOptionChain: \n", listSmartOptionChain)

        #[self.aTicker] = self.ib.reqTickers(self.a_Contract)

        # Get the Strikes as defined by current price, strikePriceRange and strikePriceMultiple
        # using close price
        #TODO update so not using close price / add last price functionality
        self.theStrikes = ibPyUtils.getStrikes(listSmartOptionChain, self.theUnderlyingReqTickerData.close,
                                       strikePriceRange, strikePriceMultiple)

        #todo need to put in more logic to get existing expiries as they do not extend out logically
        # Get the SPX expiration set and find the proper experiation
        # as it is not always the third thursday/friday
        theExpirationList = sorted(exp for exp in listSmartOptionChain.expirations
                                   if exp[:6] == self.theExpiration[:6])
        print("sorted Expirations: ", theExpirationList)
        self.theExpiration = theExpirationList.pop()

        # Build requested options based on expiry and price range
        # Most common approach is to use "SMART" as the exchange
        allOptionContracts = [(Option(self.a_Contract.symbol, self.theExpiration, strike, self.right,
                                        exchange='SMART', multiplier='100'))
                              for strike in self.theStrikes]

        # print('>----------------------------------------------->>>optionContracts1:\n', allOptionContracts)
        # print('<-----------------------------------------------<<<optionContracts1:\n')

        # # Qualify the options
        self.ib.qualifyContracts(*allOptionContracts)

        # filter for Contract Numbers
        # and set attribute optionContracts
        for c in allOptionContracts:
            if c.conId != 0:
                self.optionContracts.append(c)


    def buildBullPandas(self):
        headerLM = ['Loss$', 'Max$']
        colStrikeHL = ['StrikeL', 'StrikeH']

        print('in bull ')

        indexRangeList = list(itertools.product(self.theStrikes, self.theStrikes))
        # indexRangeList
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList, names=colStrikeHL)
        print("multiIndexRange\n", multiIndexRange)
        type(multiIndexRange)
        print("multiIndexRange.names\n", multiIndexRange.names)
        print("multiIndexRange.labels\n", multiIndexRange.labels)

        self.bullCallSpreads = pd.DataFrame(0.0, index=multiIndexRange, columns=headerLM)
        print('bullCallSpreads\n', self.bullCallSpreads)

    def populateBullSpread(self):
        #TODO need to update "closeSPXOptionPrices" to reflect the data from buildGreeks
        for aStrikeL in self.theStrikes:
            for aStrikeH in self.theStrikes:
                if aStrikeH <= aStrikeL:
                    self.bullCallSpreads.loc[(aStrikeL, aStrikeH), 'Loss$'] = float('nan')
                    self.bullCallSpreads.loc[(aStrikeL, aStrikeH), 'Max$'] = float('nan')
                else:
                    self.bullCallSpreads.loc[(aStrikeL, aStrikeH), 'Loss$'] = self.closeOptionPrices.loc[
                                                                             (self.callRight, 'Price'), aStrikeL] - \
                                                                         self.closeOptionPrices.loc[
                                                                             (self.callRight, 'Price'), aStrikeH]
                    self.bullCallSpreads.loc[(aStrikeL, aStrikeH), 'Max$'] = ((aStrikeH - aStrikeL)
                                                                         - self.bullCallSpreads.loc[
                                                                             (aStrikeL, aStrikeH), 'Loss$'])
    def buildGreeks(self):
        headerPrice = ['Price', 'ImpliedVol', 'Gamma', 'Delta', 'TimeVal', 'conId']
        indexRangeList = list(itertools.product(self.right, [self.theExpiration], self.theStrikes))
        multiIndexRange = pd.MultiIndex.from_tuples(indexRangeList,
                                                    names=['Right', 'Expiry', 'Strike'])
        print('multiIndexRange: ', multiIndexRange)
        self.closeOptionPrices = pd.DataFrame(0.0, index=multiIndexRange,
                                            columns=headerPrice)
        print('closeOptionPrices\n\n', self.closeOptionPrices)

        for aContract in self.optionContracts:
            [theReqTicker] = self.ib.reqTickers(aContract)
            theGreeks = theReqTicker.modelGreeks
            self.contractReqTickers.append(theReqTicker)
            print('aRight: ', aContract.right, 'Strike: ', aContract.strike,
                  'Expiry: ', aContract.lastTradeDateOrContractMonth)
            print('theReqTicker: ', theReqTicker, 'theGreeks', theGreeks, )

            self.closeOptionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Delta'] = theGreeks.delta
            # TODO need to determine if we should use close or last - close is yesterdays close - messing up calculations
            self.closeOptionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'TimeVal'] = theReqTicker.close - \
                                                    abs(self.theUnderlyingReqTickerData.close - aContract.strike)
            self.closeOptionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'ImpliedVol'] = theGreeks.impliedVol
            self.closeOptionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Gamma'] = theGreeks.gamma
            self.closeOptionPrices.loc[(aContract.right, aContract.lastTradeDateOrContractMonth, aContract.strike),
                                       'Price'] = theReqTicker.close
            print('.', end="")
        print('closeOptionPrices\n\n', self.closeOptionPrices)



































