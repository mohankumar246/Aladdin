#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import pprint
import time
import requests
from requests.exceptions import HTTPError

import gdax
from exchanges.exchangeClass import Exchange

class Gdax(Exchange):
    productList = ['BTC-USD', 'BCH-USD', 'ETH-USD', 'LTC-USD',
                   'ETH-BTC', 'LTC-BTC']

    def __init__(self, keyfile, coinA='BTC', coinB='USD', callTimeout=10):
        super().__init__()

        with open(keyfile, 'r') as f:
            api_base     = f.readline().strip()
            key          = f.readline().strip()
            b64secret    = f.readline().strip()
            passphrase   = f.readline().strip()
            self.handle  = gdax.AuthenticatedClient(key, b64secret, passphrase,
                                                             api_url=api_base)

        self.lastOrderId  = None
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
                status   = response.get('settled')

                if str(status) is 'True':
                    print("SETTLED")
                    break
                else:
                    print("WAIT SINCE ORDER IS OPEN")
                    time.sleep(self.callTimeout)
            except:
                #print(str(e))
                print("WAIT SINCE ORDER IS OPEN")
                time.sleep(self.callTimeout)

    def lastPrice(self):
        try:
            response = self.handle.get_product_ticker(product_id=self.currencyPair)
            price = round(float(response['price']), self.roundingPlaces)
            #print("gdax last")
            #pprint.pprint(response)
            #pprint.pprint(float(response['price']))
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            price = self.lastPrice()

        return price

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
            response = self.handle.sell(price=str(salePrice), size=orderSize, product_id=self.currencyPair, post_only='True')
            #pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        if (response.get('id') is not None) or (response.get('status') != 'rejected'):
            if blockFlag is True:
                self.waitTillComplete(response['id'])
            self.lastOrderId = response['id']
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        return response

    def buyLimit(self, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, self.roundingPlaces)
        try:
            response = self.handle.buy(price=str(buyPrice), size=orderSize, product_id=self.currencyPair, post_only='True')
            #pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.buyLimit(buyPrice, orderSize, blockFlag)

        if (response.get('id') is not None) or (response.get('status') != 'rejected'):
            if blockFlag is True:
                self.waitTillComplete(response['id'])
            self.lastOrderId = response['id']
        else:
            print("Hmm something's wrong, calling buy again")
            time.sleep(self.callTimeout)
            response = self.buyLimit(buyPrice, orderSize, blockFlag)

        return response

    def withdrawCrypto(self, coinA, orderSize, address):
        try:
            response = self.handle.crypto_withdraw(amount=str(orderSize),
                                                   currency=str(coinA),
                                                   crypto_address='LWjNG8BpjyvKfoHaeRTUP88fSZERqzTqta')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(self.callTimeout)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('id') is not None:
            self.waitTillComplete(str(response['id']))
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
        id = 0
        try:
            response = self.handle.cancel_order(str(orderId))
            id = response[0]
            pprint.pprint(response)
        except:
            time.sleep(self.callTimeout)
            id = self.cancelOrderId(orderId)

        if id == orderId:
            if blockFlag is True:
                self.waitTillComplete(orderId)
        else:
            print("Hmm something's wrong, calling cancelOrderId again")
            time.sleep(self.callTimeout)
            id = self.cancelOrderId(orderId)

        return id


