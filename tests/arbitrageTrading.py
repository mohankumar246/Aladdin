#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import pprint
import time
import requests
from requests.exceptions import HTTPError

from krakenExchange import Kraken
from gdaxExchange   import Gdax

class compareResponse:
    def __init__(self):
        self.buyFlag   = False
        self.buyPrice  = 0
        self.sellPrice = 0

class Arbitrage:

    def __init__(self):
        self.buyExchangeObj = 'none'
        self.sellExchangeObj = 'none'
        self.coinA = 'LTC'
        self.coinB = 'USD'
        pass

    def comparePrice(self):
        print("COMPARE")
        percentDifference = self.buyExchangeObj.lastPrice(self.coinA, self.coinB) / self.sellExchangeObj.lastPrice(self.coinA, self.coinB)
        response = compareResponse()
        response.buyFlag  = False
        if percentDifference < 0.97:
            response.buyFlag = True

        response.buyPrice  = self.buyExchangeObj.lastPrice(self.coinA, self.coinB)
        response.sellPrice = self.sellExchangeObj.lastPrice(self.coinA, self.coinB)
        print("BUY PRICE", response.buyPrice , "SELL PRICE", response.sellPrice)
        return response

    def buy(self, buyPrice):
        print("BUY")
        self.buyExchangeObj.buyLimit(self.coinA, self.coinB, buyPrice, orderSize=0.1, blockFlag=True)

    def sell(self, sellPrice):
        print("SELL")
        self.sellExchangeObj.sellLimit(self.coinA, self.coinB, sellPrice, orderSize=0.1, blockFlag=True)

    def transfer(self):
        print("TRANSFER")
        self.buyExchangeObj.withdrawCrypto(self.coinA, 0.1, '1')
        pass


arbitObj                 = Arbitrage()
arbitObj.sellExchangeObj = Kraken('kraken.key')
arbitObj.buyExchangeObj  = Gdax('gdax.key')
arbitObj.coinA           = 'LTC'
arbitObj.coinB           = 'USD'

def tradeForever():
    response = arbitObj.comparePrice()
    #if True:#response.buyFlag is True:
    # All these calls are blocking calls
    #Transfers in gdax happens from gdax -> coinbase api -> external address. # no time to track coinbase api now
    arbitObj.buy(response.buyPrice)
    arbitObj.transfer()
    arbitObj.sell(response.sellPrice)
    time.sleep(1800)
    arbitObj.buyExchangeObj, arbitObj.sellExchangeObj = arbitObj.sellExchangeObj, arbitObj.buyExchangeObj


while True:
    tradeForever()
    time.sleep(100)
