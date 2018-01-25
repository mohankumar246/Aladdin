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
        self.orderSize = 0
        self.totalProfit = 0
        pass

    def comparePrice(self):
        print("COMPARE")
        response = compareResponse()
        response.buyPrice  = self.buyExchangeObj.lastPrice(self.coinA, self.coinB) - 0.1
        response.sellPrice = self.sellExchangeObj.lastPrice(self.coinA, self.coinB) + 0.1

        response.buyFlag  = False
        if response.sellPrice  > response.buyPrice:
            response.buyFlag = True
            print("BUY PRICE", response.buyPrice, "SELL PRICE", response.sellPrice)
        return response

    def buy(self, buyPrice):
        print("BUY")
        self.buyExchangeObj.buyLimit(self.coinA, self.coinB, buyPrice, orderSize=self.orderSize, blockFlag=False)

    def sell(self, sellPrice):
        print("SELL")
        self.sellExchangeObj.sellLimit(self.coinA, self.coinB, sellPrice, orderSize=self.orderSize, blockFlag=False)

    def transfer(self):
        print("TRANSFER")
        self.buyExchangeObj.withdrawCrypto(self.coinA, self.orderSize, '1')
        pass


arbitObj                 = Arbitrage()
arbitObj.sellExchangeObj = Kraken('kraken.key')
arbitObj.buyExchangeObj  = Gdax('gdax.key')
arbitObj.coinA           = 'LTC'
arbitObj.coinB           = 'USD'
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


while True:
    tradeForever()
    time.sleep(100)
