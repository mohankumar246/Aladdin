from krakenExchange import Kraken
from gdaxExchange   import Gdax
from strategyClass  import Strategy
from twisted.internet import task
from twisted.internet import reactor

class Arbitrage:

    def __init__(self):
        pass

    def comparePrice(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass

    def transfer(self):
        pass


arbitObj              = Arbitrage()
arbitObj.krakenObj    = Kraken()
arbitObj.gdaxObj      = Gdax()
arbitObj.sellExchange = 'GDAX'
arbitObj.buyExchange  = 'KRAKEN'
arbitObj.coinA        = 'LTC'
arbitObj.coinB        = 'USD'

def tradeForever():
    response = arbitObj.comparePrice()
    if response.buyFlag is True:
        # All these calls are blocking calls
        arbitObj.buy(response.buyPrice)
        arbitObj.transfer()
        arbitObj.sell(response.sellPrice)
        arbitObj.buyExchange, arbitObj.sellExchange = arbitObj.sellExchange, arbitObj.buyExchange


while True:
    tradeForever()
    time.sleep(100)