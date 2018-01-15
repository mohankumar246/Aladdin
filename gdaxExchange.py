#!/usr/bin/env python

import datetime
import gdax_calls
import requests
import pprint

from datetime import timedelta
from twisted.internet import task
from twisted.internet import reactor
from requests.exceptions import HTTPError
from exchangeClass import Exchange


class Gdax(Exchange):
    productList = ['BTC-USD', 'BCH-USD', 'ETH-USD', 'LTC-USD',
                   'ETH-BTC', 'LTC-BTC']

    def __init__(self, keyfile):
        with open(keyfile, 'r') as f:
            self.api_base   = f.readline().strip()
            self.key        = f.readline().strip()
            self.b64secret  = f.readline().strip()
            self.passphrase = f.readline().strip()
            self.handle     = gdax_calls.AuthenticatedClient(self.key, self.b64secret, self.passphrase,
                                                             api_url=self.api_base)
            self.handle.get_accounts()
        super.__init__()

    def waitTillComplete(self, orderId, timeOut):
        while True:
            try:
                response = self.handle.get_order(orderId)
            except HTTPError as e:
                print(str(e))
                time.sleep(10)
                self.waitTillComplete(orderId, timeOut)

            if str(response.get('settled')) is 'True':
                print("SETTLED")
                break
            else:
                time.sleep(timeOut)
                self.waitTillComplete(orderId, timeOut)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.get_product_ticker(product_id=product)
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.lastPrice(coinA, coinB)

    def getPair(self, coinA, coinB):
        pairName = str(coinA + '-' + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def checkBalance(self):
        print()

    def sellLimit(self, coinA, coinB, salePrice, orderSize):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.sell(price=str(salePrice), size=orderSize, product_id=product, post_only='True')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.sellLimit(coinA, coinB, salePrice, orderSize)

        if response.get('id') is not None:
            self.waitTillComplete(response['id'], 100)
        else:
            print("Hmm something's wrong, calling sell again")
            self.sellLimit(coinA, coinB, salePrice, orderSize)

    def buyLimit(self, coinA, coinB, buyPrice, orderSize):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.buy(price=str(buyPrice), size=orderSize, product_id=product, post_only='True')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize)

        if response.get('id') is not None:
            self.waitTillComplete(response['id'], 100)
        else:
            print("Hmm something's wrong, calling buy again")
            self.buyLimit(coinA, coinB, buyPrice, orderSize)

    def withdrawCrypto(self, coinA, orderSize, address):
        withdrawParams = {
            'amount': str(orderSize),  # Currency determined by account specified
            'currency': str(coinA),
            'crypto_address': str(address)
        }
        try:
            response = self.handle.withdraw(withdrawParams)
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('id') is not None:
            self.waitTillComplete(response['id'], 100)
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.withdrawCrypto(self, coinA, orderSize, address)
