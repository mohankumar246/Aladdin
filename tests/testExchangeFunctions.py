#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import os
import sys

projectPath = os.path.dirname(os.getcwd())
print("Adding project path to sys path so that this project modules/packages can be imported:", projectPath)
sys.path.extend([projectPath])

import pprint
import time
import requests
from requests.exceptions import HTTPError

import exchanges

from exchanges.krakenExchange    import Kraken
from exchanges.gdaxExchange      import Gdax
from exchanges.bittrexExchange   import BittrexC
from exchanges.binanceExchange   import BinanceC

coinA='LTC'
coinB='BTC'
orderSize=0.1
#exchangeObj  = Kraken('../exchangeKeys/kraken.key', coinA, coinB)
#exchangeObj  = Gdax('../exchangeKeys/gdax.key', coinA, coinB)
#exchangeObj  = BittrexC('../exchangeKeys/bittrex.key', coinA, coinB)
#exchangeObj   = BinanceC('../exchangeKeys/binance.key', coinA, coinB)

price = exchangeObj.lastPrice()
exchangeObj.buyLimit(price-0.00001, orderSize=orderSize)
exchangeObj.waitTillLastOrderIsComplete()
price = exchangeObj.lastPrice()
exchangeObj.sellLimit(price+0.00001, orderSize=orderSize)
exchangeObj.waitTillLastOrderIsComplete()

exchangeObj.buyLimit(0.01, orderSize=orderSize)
exchangeObj.cancelOrderId(orderId=exchangeObj.lastOrderId)





