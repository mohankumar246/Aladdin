#!/usr/bin/env python3

#Copyright (c) 2017-2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import os
import sys

projectPath = os.path.dirname(os.getcwd())
print("Adding project path to sys path so that this project modules/packages can be imported:", projectPath)
sys.path.extend([projectPath])

import pprint
import time
import requests
from requests.exceptions import HTTPError

import exchanges

from exchanges.krakenExchange import Kraken
from exchanges.gdaxExchange   import Gdax

class compareResponse:
    def __init__(self):
        self.buyFlag   = False
        self.buyPrice  = 0
        self.sellPrice = 0

class Arbitrage:

    def __init__(self):
        self.buyExchangeObj = 'none'
        self.sellExchangeObj = 'none'
        self.orderSize = 0
        self.totalProfit = 0
        pass

    def comparePrice(self):
        print("COMPARE")
        response = compareResponse()
        response.buyPrice  = self.buyExchangeObj.lastPrice() - 0.02
        response.sellPrice = self.sellExchangeObj.lastPrice() + 0.02

        response.buyFlag  = False
        if response.sellPrice  > response.buyPrice:
            response.buyFlag = True
            print("BUY PRICE", response.buyPrice, "SELL PRICE", response.sellPrice)
        return response

    def buy(self, buyPrice):
        print("BUY")
        self.buyExchangeObj.buyLimit(buyPrice, orderSize=self.orderSize, blockFlag=False)

    def sell(self, sellPrice):
        print("SELL")
        self.sellExchangeObj.sellLimit(sellPrice, orderSize=self.orderSize, blockFlag=False)

    def transfer(self):
        print("TRANSFER")
        self.buyExchangeObj.withdrawCrypto(self.coinA, self.orderSize, '1')
        pass


arbitObj                 = Arbitrage()
arbitObj.sellExchangeObj = Kraken('../exchangeKeys/kraken.key', coinA='LTC', coinB='USD')
arbitObj.buyExchangeObj  = Gdax('../exchangeKeys/gdax.key', coinA='LTC', coinB='USD')
arbitObj.orderSize       = 2

def tradeForever():
    # Not doing transfer as waiting for a transfer to complete from gdax requires coinbase account api's
    # to be used and I dont have time to check that now. Also transfer cost fees and are slow. Maty check that later.
    response = arbitObj.comparePrice()
    if response.buyFlag is True:
        #All these calls are blocking calls
        arbitObj.buy(response.buyPrice)
        arbitObj.sell(response.sellPrice)
        arbitObj.buyExchangeObj.waitTillLastOrderIsComplete()
        arbitObj.sellExchangeObj.waitTillLastOrderIsComplete()
        arbitObj.totalProfit += ((response.sellPrice - response.buyPrice)*arbitObj.orderSize)
        print("Total Profit", arbitObj.totalProfit)
        arbitObj.buyExchangeObj, arbitObj.sellExchangeObj = arbitObj.sellExchangeObj, arbitObj.buyExchangeObj
        time.sleep(1800)


while True:
    tradeForever()
    time.sleep(100)
