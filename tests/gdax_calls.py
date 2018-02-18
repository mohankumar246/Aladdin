#!/usr/bin/env python3

#Copyright (c) 2018 Mohankumar Nekkarakalaya

# This file is part of Aladdin.
# Licensed under the MIT license. See LICENSE.txt in the project folder.

import datetime
import gdax_calls
import requests

from datetime import timedelta
from twisted.internet import task
from twisted.internet import reactor

buyResponse = 0
buyPrice = -1
buyPending = 0
saleResponse = 0
salePrice = -1
salePending = 0
timeout = 300
sliceTime = 300
lastorderid = 0
orderSize = 1
profit = 1.5
product = 'LTC-USD'
totalProfits = 0
counter = 0
sum1 = 0

api_base = 'https://api.gdax.com/'
key = 'ur own'
b64secret = 'ur own'
passphrase = 'ur own'

auth_client = gdax_calls.AuthenticatedClient(key, b64secret, passphrase, api_url=api_base)

auth_client.get_accounts()


def checkStatus():
    global buyResponse, buyPrice, buyPending, saleResponse, salePrice, salePending, totalProfits
    # print buyResponse, buyPrice, buyPending, saleResponse, salePrice, salePending
    # check the status of site
    response = requests.get(api_base + '/products')
    # print(response.json())
    if response.status_code is not 200:
        print('Invalid GDAX Status Code: %d' % response.status_code)
        return 0

    if (buyPending is 1):
        response = auth_client.get_order(buyResponse['id'])
        print
        'BUY ORDER STATUS QUERY'
        print
        'SETTLED', response.get('settled')
        if (str(response.get('settled')) is 'True'): buyPending = 0

    if ((buyPending is 0) and (salePending is 0) and (buyPrice is not -1)):
        response = auth_client.get_product_ticker(product_id=product)
        print
        "SELL ORDER - CURR", float(response['price']) + profit, "MY SELL", buyPrice + profit
        salePrice = max(float(response['price']), buyPrice) + profit

        print
        "SELL ORDER - PRICE", salePrice
        saleResponse = auth_client.sell(price=str(salePrice), size=orderSize, product_id=product, post_only='True')
        print
        "SELL RESPONE"
        print
        saleResponse
        salePrice = -1;
        if (saleResponse.get('status') == 'pending'):
            salePending = 1
            salePrice = max(float(response['price']), buyPrice) + profit
            print
            "SALE PLACED"

    if (salePending is 1):
        response = auth_client.get_order(saleResponse['id'])
        print
        'SALE ORDER STATUS QUERY'
        print
        'SETTLED', response.get('settled')
        if (str(response.get('settled')) is 'True'):
            salePending = 0
            totalProfits += (salePrice - buyPrice) * orderSize
            print
            "TOTAL PROFIT since START", totalProfits
            buyPrice = -1

    if (salePending is 0 and buyPending is 0):
        return 1
    else:
        return 0


def setBuyOrder(r):
    global buyResponse, buyPrice, buyPending, salePending
    response = auth_client.get_product_ticker(product_id=product)
    print
    "BUY ORDER - CURR", float(response['price']) - 0.01, "MY BUY", r[0][3] - 0.01
    buyPrice = min(float(response['price']), r[0][3]) - 0.01
    print
    "BUY ORDER - PRICE", buyPrice
    buyResponse = auth_client.buy(price=str(buyPrice), size=orderSize, product_id=product, post_only='True')
    print
    "BUY RESPONE"
    print
    buyResponse
    buyPrice = -1
    if (str(buyResponse.get('status')) == 'pending'):
        buyPrice = min(float(response['price']), r[0][3]) - 0.01
        buyPending = 1
        salePending = 0
        print
        "BUY PLACED"


def safe_list_get(l, idx1, idx2, default=0):
    try:
        return l[idx1][idx2]
    except IndexError:
        return default


def safe_list_get1(l, idx1, default=0):
    try:
        return l[idx1]
    except IndexError:
        return default


def doWork():
    global sum1, counter
    if checkStatus() is 1:
        startTime = datetime.datetime.utcnow()
        # print "Time now", startTime
        startTime = startTime - timedelta(minutes=startTime.minute % 5) - timedelta(
            seconds=startTime.second) - timedelta(microseconds=startTime.microsecond)
        endTime = startTime - timedelta(seconds=sliceTime)
        r = auth_client.get_product_historic_rates(product, start=endTime.isoformat('T'), end=startTime.isoformat('T'),
                                                   granularity=sliceTime)

        # r = auth_client.get_product_historic_rates(product, granularity=3600)
        print
        "HISTORIC DATA start", startTime, "end", endTime
        print
        safe_list_get1(r, 0)
        if counter == 2:
            sum1 = 0
            counter = 0

        counter = counter + 1
        if (safe_list_get(l=r, idx1=0, idx2=3) > safe_list_get(l=r, idx1=0, idx2=4)):
            sum1 += (safe_list_get(l=r, idx1=0, idx2=3) - safe_list_get(l=r, idx1=0, idx2=4))

        if (sum1 > 2):
            setBuyOrder(r)
        # setBuyOrder(10000000)
        # response = auth_client.get_product_ticker(product_id=product)
        # print r[0][0]
        # for p in r: print p

    pass


l = task.LoopingCall(doWork)
l.start(timeout)

reactor.run()
