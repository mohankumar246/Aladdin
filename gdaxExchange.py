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

    def lastPrice(self, coinA, coinB='USD'):
        product  = self.getPair(coinA, coinB)

        while True:
            try:
                response = self.handle.get_product_ticker(product_id=product)
                pprint.pprint(response)
                break
            except HTTPError as e:
                print(str(e))

    def getPair(self, coinA, coinB):
        pairName = str(coinA + '-' + coinB)
        if pairName in self.productList:
            return pairName
        else:
            raise ValueError(pairName + "Not found")

    def checkBalance(self):
        print()
