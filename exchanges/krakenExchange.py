#!/usr/bin/env python

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import pprint
import time
import requests
from requests.exceptions import HTTPError

import krakenex
from exchanges.exchangeClass import Exchange

class Kraken(Exchange):
    productList = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD',
                   'XETHXXBT', 'XLTCXXBT']

    def __init__(self, keyfile, coinA='BTC', coinB='USD', callTimeout=10):
        super().__init__()
        self.handle = krakenex.API()
        self.handle.load_key(keyfile)

        self.currencyPair = self.getPair(coinA, coinB)
        self.callTimeout  = callTimeout
        if coinB == 'USD':
            self.roundingPlaces = 2
        else:
            self.roundingPlaces = 5

    def waitTillComplete(self, id):
        print("WAIT SINCE ORDER IS OPEN")
        while True:
            try:
                response = self.handle.query_private('QueryOrders', {'txid': id})
                status   = response.get('result').get(id).get('status')
                if status == 'closed':
                    print("CLOSED")
                    break
                else:
                    print("Kraken WAIT SINCE ORDER IS OPEN")
                    time.sleep(self.callTimeout)
            except:
                #print(str(e))
                time.sleep(self.callTimeout)
                print("Kraken WAIT SINCE ORDER IS OPEN")

    def lastPrice(self):
        try:
            response = self.handle.query_public('Trades', {'pair': self.currencyPair})
            price    = response.get('result').get(self.currencyPair)[-1][0]
            price    = round(float(price), self.roundingPlaces)
        except:
            time.sleep(self.callTimeout)
            price    = self.lastPrice()

        return price

    def checkBalance(self):
        print(self.handle.query_private('Balance'))
        try:
            response = self.handle.query_private('Balance')
            pprint.pprint(response)
        except HTTPError as e:
            print(str(e))
            time.sleep(self.callTimeout)
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

    def sellLimit(self, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, self.roundingPlaces)

        req_data = {'pair': self.currencyPair, 'type': 'sell', 'ordertype': 'limit',
                    'price': str(salePrice), 'volume': str(orderSize)}
        try:
            response = self.handle.query_private('AddOrder', req_data)
            #pprint.pprint(response)
            if not response.get('error'):
                print("SELL PLACED")
            else:
                print("Hmm something's wrong, calling sell again")
                time.sleep(self.callTimeout)
                response = self.sellLimit(salePrice, orderSize, blockFlag)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        txid = response.get('result').get('txid')[0]

        if txid is not None:
            if blockFlag is True:
                self.waitTillComplete(txid)
            self.lastOrderId = txid
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(self.callTimeout)
            response = self.sellLimit(salePrice, orderSize, blockFlag)

        return response

    def buyLimit(self, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, self.roundingPlaces)
        req_data = {'pair': self.currencyPair, 'type': 'buy', 'ordertype': 'limit',
                    'price': str(buyPrice), 'volume': str(orderSize)}
        #pprint.pprint(req_data)
        try:
            response = self.handle.query_private('AddOrder', req_data)
            #pprint.pprint(response)
            if not response.get('error'):
                print("BUY PLACED")
            else:
                print("Hmm something's wrong, calling buy again")
                time.sleep(self.callTimeout)
                response = self.buyLimit(buyPrice, orderSize, blockFlag)
        except:
            #print(str(e))
            time.sleep(self.callTimeout)
            response = self.buyLimit(buyPrice, orderSize, blockFlag)

        txid = response.get('result').get('txid')[0]

        #print(txid)
        if txid is not None:
            if blockFlag is True:
                self.waitTillComplete(txid)
            self.lastOrderId = txid
        else:
            print("Hmm something's wrong, calling buy again")
            time.sleep(self.callTimeout)
            response = self.buyLimit(buyPrice, orderSize, blockFlag)

        return response

    def WaitForWithdraw(self, coinA, refid):
        while True:
            try:
                response = self.handle.query_private('WithdrawStatus', {'asset': str(coinA)})
                pprint.pprint(response)
                print("Withdraw Status")
                result = response.get('result')
                for info in result:
                    if info.get('refid') == refid:
                        break
                if info.get('status') == 'Success':
                    print("Withdraw Succeeded")
                    break
            except HTTPError as e:
                print(str(e))
                time.sleep(self.callTimeout)
                self.WaitForWithdraw(coinA)
            time.sleep(self.callTimeout)

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
            time.sleep(self.callTimeout)
            self.withdrawCrypto(coinA, orderSize, address)

        if response.get('result').get('refid') is not None:
            self.WaitForWithdraw('LTC',response.get('result').get('refid'))
        else:
            print("Hmm something's wrong, calling withdraw again")
            time.sleep(self.callTimeout)
            self.withdrawCrypto(coinA, orderSize, address)

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

    def cancelOrderId(self, orderId, blockFlag=False):
        req_data = {'txid': str(orderId)}
        #pprint.pprint(req_data)
        try:
            response = self.handle.query_private('CancelOrder', req_data)
            pprint.pprint(response)
        except:
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        if response.get('result').get('count') is not None:
            if blockFlag is True:
                self.waitTillComplete(response.get(orderId))
        else:
            print("Hmm something's wrong, calling cancelOrderId again")
            time.sleep(self.callTimeout)
            response = self.cancelOrderId(orderId)

        return response

