#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import pprint
import time
import requests
from requests.exceptions import HTTPError

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException

from exchanges.exchangeClass import Exchange

class BinanceC(Exchange):
    productList = ['BTCUSD', 'BCHUSD', 'ETHUSD', 'LTCUSD',
                   'ETHBTC', 'LTCBTC']

    def __init__(self, keyfile, coinA='BTC', coinB='USD', callTimeout=10):
        super().__init__()

        with open(keyfile, 'r') as f:
            key          = f.readline().strip()
            secret       = f.readline().strip()
            self.handle  = Client(key, secret)


        self.lastOrderId  = None
        self.currencyPair = self.getPair(coinA, coinB)
        self.callTimeout  = callTimeout
        # rounding should be dependent on the voinB different exchanges have different rounding for products
        if coinB == 'USD':
            self.roundingPlaces = 2
        else:
            self.roundingPlaces = 5

    def waitTillComplete(self, orderId):
        while True:
            try:
                response = self.handle.get_order(
                               symbol=self.currencyPair,
                               orderId=orderId)
                pprint.pprint(response)
                status   = response.get('status')
                pprint.pprint(status)
                if status == 'FILLED':
                    print("SETTLED")
                    break
                else:
                    time.sleep(self.callTimeout)
            except:
                time.sleep(self.callTimeout)

    def lastPrice(self):
        try:
            response = self.handle.get_symbol_ticker(symbol=self.currencyPair)
            price = round(float(response.get('price')), self.roundingPlaces)
            print("binance last")
            pprint.pprint(response)
            pprint.pprint(price)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            price = self.lastPrice()

        return price

    def getPair(self, coinA, coinB):
        pairName = str(coinA + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def sellLimit(self, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, self.roundingPlaces)

        try:
            response = self.handle.order_limit_sell(price=str(salePrice), quantity=orderSize, symbol=self.currencyPair)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        if (response.get('orderId') is not None) or (response.get('status') != 'REJECTED'):
            if blockFlag is True:
                self.waitTillComplete(response.get('orderId'))
            self.lastOrderId = response.get('orderId')
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        return response

    def buyLimit(self, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, self.roundingPlaces)

        try:
            response = self.handle.order_limit_buy(price=str(buyPrice), quantity=orderSize, symbol=self.currencyPair)
            pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.buyLimit(buyPrice, orderSize, blockFlag)

        if (response.get('orderId') is not None) or (response.get('status') != 'REJECTED'):
            if blockFlag is True:
                self.waitTillComplete(response.get('orderId'))
            self.lastOrderId = response.get('orderId')
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(self.callTimeout)
            response = self.sellLimit(buyPrice, orderSize, blockFlag)

        return response

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

    def cancelOrderId(self, orderId, blockFlag=False):
        try:
            response = self.handle.cancel_order(
                           symbol=self.currencyPair,
                           orderId=str(orderId))
            pprint.pprint(response)
        except:
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        if response.get('orderId') is not None:
            if blockFlag is True:
                self.waitTillComplete(response.get(orderId))
        else:
            print("Hmm something's wrong, calling cancelOrderId again")
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        return response
