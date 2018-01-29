#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Prints the account balance to standard output.

import pprint
import time
import requests
from requests.exceptions import HTTPError

import krakenex
from exchanges.exchangeClass import Exchange

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
                response = self.handle.query_private('QueryOrders', {'txid': id})
            except:
                #print(str(e))
                time.sleep(10)
                self.waitTillComplete(id, timeOut)

            #pprint.pprint(response)
            print("WAIT SINCE ORDER IS OPEN")
            try:
                status = response.get('result').get(id).get('status')
            except:
                time.sleep(timeOut)
                #print("OPEN")
                self.waitTillComplete(id, timeOut)

            pprint.pprint(status)
            if status == 'closed':
                print("CLOSED")
                break
            else:
                time.sleep(timeOut)
                #print("OPEN")
                self.waitTillComplete(id, timeOut)

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)
        #print("kraken last")
        try:
            response = self.handle.query_public('Trades', {'pair': 'XLTCZUSD'})
        except:
            #print(str(e))
            time.sleep(10)
            self.lastPrice(coinA, coinB)
        price = ''
        try:
            price = response.get('result').get('XLTCZUSD')[-1][0]
            #pprint.pprint(response.get('result').get('XLTCZUSD')[-1])
            #pprint.pprint(price)
        except:
            time.sleep(10)
            self.lastPrice(coinA, coinB)

        try:
            price = round(float(price), 2)
            #print("kraken price",price)
        except:
            time.sleep(10)
            self.lastPrice(coinA, coinB)
        
        #print("Must not happen kraken", price)
        return price   

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

    def sellLimit(self, coinA, coinB, salePrice, orderSize, blockFlag=False):
        salePrice = round(salePrice, 2)
        product  = self.getPair(coinA, coinB)

        req_data = {'pair': product, 'type': 'sell', 'ordertype': 'limit',
                    'price': str(salePrice), 'volume': str(orderSize)}
        try:
            response = self.handle.query_private('AddOrder', req_data)
            #pprint.pprint(response)
            if not response.get('error'):
                print("SELL PLACED")
            else:
                print("Hmm something's wrong, calling sell again")
                time.sleep(10)
                self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)
        except:
            #print(str(e))
            time.sleep(10)
            self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

        try:
            txid = response.get('result').get('txid')[0]
        except:
            print("Hmm something's wrong, calling sell again")
            time.sleep(10)
            self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

        if txid is not None:
            if blockFlag is True:
                self.waitTillComplete(txid, 100)
            self.lastOrderId = txid
        else:
            print("Hmm something's wrong, calling sell again")
            time.sleep(10)
            self.sellLimit(coinA, coinB, salePrice, orderSize, blockFlag)

    def buyLimit(self, coinA, coinB, buyPrice, orderSize, blockFlag=False):
        buyPrice = round(buyPrice, 2)
        product  = self.getPair(coinA, coinB)
        req_data = {'pair': product, 'type': 'buy', 'ordertype': 'limit',
                    'price': str(buyPrice), 'volume': str(orderSize)}
        #pprint.pprint(req_data)
        try:
            response = self.handle.query_private('AddOrder', req_data)
            #pprint.pprint(response)
            if not response.get('error'):
                print("BUY PLACED")
            else:
                print("Hmm something's wrong, calling buy again")
                time.sleep(10)
                self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)
        except:
            #print(str(e))
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

        try:
            txid = response.get('result').get('txid')[0]
        except:
            print("Hmm something's wrong, calling buy again")
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

        #print(txid)
        if txid is not None:
            if blockFlag is True:
                self.waitTillComplete(txid, 100)
            self.lastOrderId = txid
        else:
            print("Hmm something's wrong, calling buy again")
            time.sleep(10)
            self.buyLimit(coinA, coinB, buyPrice, orderSize, blockFlag)

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

        if response.get('result').get('refid') is not None:
            self.WaitForWithdraw('LTC',response.get('result').get('refid'))
        else:
            print("Hmm something's wrong, calling withdraw again")
            time.sleep(40)
            self.withdrawCrypto(coinA, orderSize, address)

    def waitTillLastOrderIsComplete(self):
        if self.lastOrderId is not None:
            self.waitTillComplete(self.lastOrderId, 100)
        else:
            print("Hmm something's wrong, calling waitTillLastOrderIsComplete again")
            self.waitTillLastOrderIsComplete()

