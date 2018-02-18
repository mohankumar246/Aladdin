#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

class Exchange:

    def __init__(self, keyfile='none', coinA='BTC', coinB='USD', callTimeout=10):
        pass

    def waitTillComplete(self, orderId):
        pass

    def lastPrice(self):
        pass

    def getPair(self, coinA, coinB):
        pass

    def checkBalance(self):
        pass

    def sellLimit(self, salePrice, orderSize, blockFlag=False):
        pass

    def buyLimit(self, buyPrice, orderSize, blockFlag=False):
        pass

    def withdrawCrypto(self, coinA, orderSize, address):
        pass

    def waitTillLastOrderIsComplete(self):
        pass

    def cancelOrderId(self, orderId):
        pass
