# Get my Utilities
from localUtilities import dateUtils, ibPyUtils, configIB

import numpy as np
import pandas as pd
import datetime
import random
import itertools

from ib_insync import *

class OptionSpreads:

    # a single list is shared by all instances:
    # Headers
    headerPrice = ['Price', 'impliedVol', 'Gamma', 'Delta', 'TimeVal']
    # Puts / Calls
    putRight = 'P'
    callRight = 'C'
    rights = [putRight, callRight]

    # Some header stuff
    headerLM = ['Loss$', 'Max$', 'Delta']
    colStrikeHL = ['StrikeL', 'StrikeH']

    # invoked for each instantiated class
    def __init__(self,a_qualified_contract, anIB):
        self.a_Contract = a_qualified_contract
        self.ib = anIB
        self.contracts = []
        self.theStrikes =[]

    def qualify_option_chain_close(self, theRight, exchange,
                                   strikePriceRange=10, strikePriceMultiple=5):
        print("<<in qualify_index_option_chain >>  ")
        # Fully qualify the given contracts in-place.
        # This will fill in the missing fields in the contract, especially the conId.
        # list of options
        listOptionChain = self.ib.reqSecDefOptParams(self.a_Contract.symbol, '', self.a_Contract.secType,
                                                self.a_Contract.conId)
        print(listOptionChain)
        # filter out for SMART ????
        listSmartOptionChain = next(c for c in listOptionChain
                                      if c.exchange == 'SMART')
        print("listSmartOptionChain: \n", listSmartOptionChain)

        [self.aTicker] = self.ib.reqTickers(self.a_Contract)
        print('++++++++++++++++++++++++++++++++')
        # Get the Strikes as defined by current price, strikePriceRange and strikePriceMultiple
        strikes = ibPyUtils.getStrikes(listSmartOptionChain, self.aTicker.close,
                                       strikePriceRange, strikePriceMultiple)
        print('aTicker.close:  ', self.aTicker.close)
        print('strikes: ', strikes)

        # Get the SPX expirations set
        # to narrow to Friday or Thursdays use isThursday/isFriday
        # if dateUtils.isFriday(exp))
        sortedExpirations = sorted(exp for exp in listSmartOptionChain.expirations)

        print("sortedExpirations: ", sortedExpirations)

        # Build requested options based on expriy and price range
        self.contracts = [Option(self.a_Contract.symbol, expiration, strike, right, exchange='SMART')
                     for right in theRight for expiration in sortedExpirations for strike in strikes]
        # Qualify the options
        self.ib.qualifyContracts(*self.contracts)
        print("Contracts: \n", self.contracts)

        self.theStrikes = strikes
        self.theStrikes = [int(i) for i in self.theStrikes]
        print("toIntStrikes:  ", self.theStrikes)







































