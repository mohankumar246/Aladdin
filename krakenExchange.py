#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Prints the account balance to standard output.

import pprint
import time
import requests
from requests.exceptions import HTTPError

import krakenex
from exchangeClass import Exchange

class Kraken(Exchange):
    productList = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD',
                   'XETHXXBT', 'XLTCXXBT']

    def __init__(self, keyfile):
        self.handle = krakenex.API()
        self.handle.load_key(keyfile)
        super().__init__('none')

    def waitTillComplete(self, id, timeOut):
        while True:
            try:
                response = self.handle.query_private('OpenOrders')
                if response[id].status is 'closed':
                    print("CLOSED")
                    break
                else:
                    time.sleep(timeOut)
                    self.waitTillComplete(id, timeOut)
            except HTTPError as e:
                print(str(e))
                time.sleep(10)
                self.waitTillComplete(id, timeOut)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)
        try:
            response = self.handle.query_public('Trades', {'pair': 'XLTCZUSD'})
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.lastPrice(coinA, coinB)
        return float((response.get('result')).get('XLTCZUSD')[0][0])

    def checkBalance(self):
        print(self.handle.query_private('Balance'))
        try:
            response = self.handle.query_private('Balance')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.checkBalance()

    def getPair(self, coinA, coinB):
        if coinB == 'USD':
            pairName = str('X' + coinA + 'ZUSD')
        else:
            pairName = str('X' + coinA + 'XXBT')

        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def sellLimit(self, coinA, coinB, salePrice, orderSize):
        product  = self.getPair(coinA, coinB)

        req_data = {'pair': product, 'type': 'sell', 'ordertype': 'limit',
                    'price': str(salePrice), 'volume': str(orderSize)}
        try:
            response = self.handle.query_private('AddOrder', req_data)
            pprint.pprint(response)
            if response.get('txid') is not None:
                print("SELL PLACED")
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.checkBalance()

        if response.get('txid') is not None:
            self.waitTillComplete(response['txid'], 100)
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.sellLimit(coinA, coinB, salePrice, orderSize)

    def buyLimit(self, coinA, coinB, buyPrice, orderSize):
        product  = self.getPair(coinA, coinB)
        req_data = {'pair': product, 'type': 'buy', 'ordertype': 'limit',
                    'price': str(buyPrice), 'volume': str(orderSize)}
        pprint.pprint(req_data)
        try:
            response = self.handle.query_private('AddOrder', req_data)
            pprint.pprint(response)
            if response.get('txid') is not None:
                print("BUY PLACED")
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize)

        if response.get('txid') is not None:
            self.waitTillComplete(response['txid'], 100)
        else:
            print("Hmm something's wrong, calling withdraw again")
            self.buyLimit(coinA, coinB, buyPrice, orderSize)

    def WaitForWithdraw(self, coinA):
        while True:
            try:
                response = self.handle.query_private('WithdrawStatus', {'asset': str(coinA)})
                pprint.pprint(response)
                print("Withdraw Status")
                if response[0].get('status') is 'SUCCESS':
                    print("Withdraw Succeeded")
                    break
            except HTTPError as e:
                print(str(e))
                time.sleep(10)
                self.WaitForWithdraw(coinA)
            time.sleep(100)

    def withdrawCrypto(self, coinA, orderSize, address):
        address = 'gdaxltx'
        withdrawParams = {
            'asset': str(coinA),  # Currency determined by account specified
            'key': address,
            'amount': str(orderSize)
        }

        try:
            response = self.handle.query_private('Withdraw', withdrawParams)
            pprint.pprint(response)
            print("WITHDRAW PLACED")
        except HTTPError as e:
            print(str(e))
            time.sleep(10)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('refid') is not None:
            self.WaitForWithdraw()
        else:
            print("Hmm something's wrong, calling withdraw again")
            time.sleep(40)
            self.withdrawCrypto(coinA, orderSize, address)
