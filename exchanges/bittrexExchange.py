#!/usr/bin/env python3

#Copyright (c) 2017-2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import pprint
import time
import requests
from requests.exceptions import HTTPError

from bittrex.bittrex import *
from exchanges.exchangeClass import Exchange

class BittrexC(Exchange):
    productList = ['BTC-USD', 'BCH-USD', 'ETH-USD', 'LTC-USD',
                   'ETH-BTC', 'BTC-LTC']

    def __init__(self, keyfile, coinA='BTC', coinB='USD', callTimeout=10):
        super().__init__()
        with open(keyfile, 'r') as f:
            key          = f.readline().strip()
            secret       = f.readline().strip()
            apiVersion   = f.readline().strip()
            self.handle  = Bittrex(key, secret, api_version=apiVersion)

        self.lastOrderId = None
        self.currencyPair = self.getPair(coinA, coinB)
        self.callTimeout  = callTimeout
        if coinB == 'USD':
            self.roundingPlaces = 2
        else:
            self.roundingPlaces = 5

    def waitTillComplete(self, orderId):
        while True:
            try:
                response = self.handle.get_order(orderId)
                status = response.get('result').get('IsOpen')
                if str(status) is 'False':
                    print("SETTLED")
                    break
                else:
                    time.sleep(self.callTimeout)
                    print("Bittrex WAIT SINCE ORDER IS OPEN")
            except:
                print("Bittrex WAIT SINCE ORDER IS OPEN")
                time.sleep(self.callTimeout)

    def lastPrice(self):
        try:
            response = self.handle.get_ticker(market=self.currencyPair)
            #print("bittrex last")
            #pprint.pprint(response)
            price = response.get('result').get('Last')
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            self.lastPrice()

        #pprint.pprint(float(response['price']))
        return round(float(price), self.roundingPlaces)

    def getPair(self, coinA, coinB):
        pairName = str(coinA + '-' + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def checkBalance(self):
        print()

    def sellLimit(self, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, self.roundingPlaces)
        try:
            response = self.handle.sell_limit(market=self.currencyPair, quantity=orderSize, rate=salePrice)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            self.sellLimit(salePrice, orderSize, blockFlag)

        if (response.get('message') == '') and (response.get('success') != 'False'):
            if blockFlag is True:
                self.waitTillComplete(response.get('result').get('uuid'))
            self.lastOrderId = response.get('result').get('uuid')
        else:
            print("Hmm something's wrong, calling sell again")
            self.sellLimit(salePrice, orderSize, blockFlag)

    def buyLimit(self, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, self.roundingPlaces)
        try:
            response = self.handle.buy_limit(market=self.currencyPair, quantity=orderSize, rate=buyPrice)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            self.buyLimit(buyPrice, orderSize, blockFlag)

        if (response.get('message') == '') and (response.get('success') != 'False'):
            if blockFlag is True:
                self.waitTillComplete(response.get('result').get('uuid'))
            self.lastOrderId = response.get('result').get('uuid')
        else:
            print("Hmm something's wrong, calling buy again")
            self.buyLimit(buyPrice, orderSize, blockFlag)

    def withdrawCrypto(self, coinA, orderSize, address):
        try:
            response = self.handle.crypto_withdraw(currency=str(coinA),
                                                   quantity=orderSize,
                                                   address='LWjNG8BpjyvKfoHaeRTUP88fSZERqzTqta')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(self.callTimeout)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('result').get('uuid') is not None:
            self.waitTillComplete(str(response.get('result').get('uuid')))
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.withdrawCrypto(coinA, orderSize, address)

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

    def cancelOrderId(self, orderId, blockFlag=False):
        try:
            response = self.handle.cancel(
                           uuid=str(orderId))
            pprint.pprint(response)
        except:
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        if (response.get('message') == '') and (response.get('success') != 'False'):
            if blockFlag is True:
                self.waitTillComplete(response.get(orderId))
        else:
            print("Hmm something's wrong, calling cancelOrderId again")
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        return response


