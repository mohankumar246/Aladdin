#!/usr/bin/env python

import pprint
import time
import requests
from requests.exceptions import HTTPError

from bittrex.bittrex import *
from exchanges.exchangeClass import Exchange

class BittrexC(Exchange):
    productList = ['BTC-USD', 'BCH-USD', 'ETH-USD', 'LTC-USD',
                   'ETH-BTC', 'BTC-LTC']

    def __init__(self, keyfile):
        with open(keyfile, 'r') as f:
            key          = f.readline().strip()
            secret       = f.readline().strip()
            apiVersion   = f.readline().strip()
            self.handle  = Bittrex(key, secret, api_version=apiVersion)

        super().__init__('none')
        self.lastOrderId = None

    def waitTillComplete(self, orderId, timeOut):
        while True:
            try:
                response = self.handle.get_order(orderId)
            except:
                time.sleep(10)
                self.waitTillComplete(orderId, timeOut)

            pprint.pprint(response)
            print("WAIT SINCE ORDER IS OPEN")
            try:
                status = response.get('result').get('IsOpen')
            except:
                time.sleep(timeOut)
                self.waitTillComplete(orderId, timeOut)

            if str(status) is 'False':
                print("SETTLED")
                break
            else:
                time.sleep(timeOut)
                self.waitTillComplete(orderId, timeOut)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.get_ticker(market=product)
            #print("bittrex last")
            #pprint.pprint(response)
            price = response.get('result').get('Last')
        except:
            #print(str(e))
            time.sleep(10)
            self.lastPrice(coinA, coinB)

        #pprint.pprint(float(response['price']))
        return round(float(price), 2)

    def getPair(self, coinA, coinB):
        pairName = str(coinA + '-' + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def checkBalance(self):
        print()

    def sellLimit(self, coinA, coinB, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, 6)
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.sell_limit(market=product, quantity=orderSize, rate=salePrice)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(10)
            self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

        if (response.get('message') == '') and (response.get('success') != 'False'):
            if blockFlag is True:
                self.waitTillComplete(response.get('result').get('uuid'), 100)
            self.lastOrderId = response.get('result').get('uuid')
        else:
            print("Hmm something's wrong, calling sell again")
            self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

    def buyLimit(self, coinA, coinB, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, 6)
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.buy_limit(market=product, quantity=orderSize, rate=buyPrice)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

        if (response.get('message') == '') and (response.get('success') != 'False'):
            if blockFlag is True:
                self.waitTillComplete(response.get('result').get('uuid'), 100)
            self.lastOrderId = response.get('result').get('uuid')
        else:
            print("Hmm something's wrong, calling buy again")
            self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

    def withdrawCrypto(self, coinA, orderSize, address):
        try:
            response = self.handle.crypto_withdraw(currency=str(coinA),
                                                   quantity=orderSize,
                                                   address='LWjNG8BpjyvKfoHaeRTUP88fSZERqzTqta')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('result').get('uuid') is not None:
            self.waitTillComplete(str(response.get('result').get('uuid')), 100)
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.withdrawCrypto(coinA, orderSize, address)

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId, 100)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

