#!/usr/bin/env python3

import pprint
import time
import requests
from requests.exceptions import HTTPError

import gdax
from exchanges.exchangeClass import Exchange

class Gdax(Exchange):
    productList = ['BTC-USD', 'BCH-USD', 'ETH-USD', 'LTC-USD',
                   'ETH-BTC', 'LTC-BTC']

    def __init__(self, keyfile):
        with open(keyfile, 'r') as f:
            api_base     = f.readline().strip()
            key          = f.readline().strip()
            b64secret    = f.readline().strip()
            passphrase   = f.readline().strip()
            self.handle  = gdax.AuthenticatedClient(key, b64secret, passphrase,
                                                             api_url=api_base)

        super().__init__('none')
        self.lastOrderId = None

    def waitTillComplete(self, orderId, timeOut):
        while True:
            try:
                response = self.handle.get_order(orderId)
            except:
                #print(str(e))
                time.sleep(10)
                response = self.waitTillComplete(orderId, timeOut)

            #pprint.pprint(response)
            print("WAIT SINCE ORDER IS OPEN")
            try:
                status = response.get('settled')
            except:
                time.sleep(timeOut)
                self.waitTillComplete(orderId, timeOut)

            if str(status) is 'True':
                print("SETTLED")
                break
            else:
                time.sleep(timeOut)
                self.waitTillComplete(orderId, timeOut)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.get_product_ticker(product_id=product)
            price = round(float(response['price']), 2)
            #print("gdax last")
            #pprint.pprint(response)
            #pprint.pprint(float(response['price']))
        except:
            #print(str(e))
            time.sleep(10)
            price = self.lastPrice(coinA, coinB)

        return price

    def getPair(self, coinA, coinB):
        pairName = str(coinA + '-' + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def checkBalance(self):
        print()

    def sellLimit(self, coinA, coinB, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, 2)
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.sell(price=str(salePrice), size=orderSize, product_id=product, post_only='True')
            #pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(10)
            response = self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

        if (response.get('id') is not None) or (response.get('status') != 'rejected'):
            if blockFlag is True:
                self.waitTillComplete(response['id'], 100)
            self.lastOrderId = response['id']
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(10)
            response = self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

        return response

    def buyLimit(self, coinA, coinB, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, 2)
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.buy(price=str(buyPrice), size=orderSize, product_id=product, post_only='True')
            #pprint.pprint(response)
        except:
            #print(str(e))
            time.sleep(10)
            response = self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

        if (response.get('id') is not None) or (response.get('status') != 'rejected'):
            if blockFlag is True:
                self.waitTillComplete(response['id'], 100)
            self.lastOrderId = response['id']
        else:
            print("Hmm something's wrong, calling buy again")
            time.sleep(10)
            response = self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

        return response

    def withdrawCrypto(self, coinA, orderSize, address):
        try:
            response = self.handle.crypto_withdraw(amount=str(orderSize),
                                                   currency=str(coinA),
                                                   crypto_address='LWjNG8BpjyvKfoHaeRTUP88fSZERqzTqta')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('id') is not None:
            self.waitTillComplete(str(response['id']), 100)
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.withdrawCrypto(coinA, orderSize, address)

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId, 100)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

