#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Prints the account balance to standard output.

import krakenex
import pprint
from requests.exceptions import HTTPError
from exchangeClass import Exchange


class Kraken(Exchange):
    productList = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD',
                   'XETHXXBT', 'XLTCXXBT']

    def __init__(self, keyfile):
        self.handle = krakenex.API()
        self.handle.load_key(keyfile)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)

        while True:
            try:
                response = self.handle.query_public('Trades', {'pair': 'XLTCZUSD'})
                pprint.pprint(response)
                break
            except HTTPError as e:
                print(str(e))

    def checkBalance(self):
        print(self.handle.query_private('Balance'))

    def getPair(self, coinA, coinB):

        if coinB == 'USD':
            pairName = str('X' + coinA + 'ZUSD')
        else:
            pairName = str('X' + coinA + 'XXBT')

        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")
