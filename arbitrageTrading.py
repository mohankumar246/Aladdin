from krakenExchange import Kraken
from gdaxExchange   import Gdax
from strategyClass  import Strategy
from twisted.internet import task
from twisted.internet import reactor


class Arbitrage(Strategy):

    def __init__(self):
        pass

    def comparePrice(self, coinA, coinB):
        pass

    def buy(self, coinA, coinB, price, exchange):
        pass

    def sell(self, coinA, coinB, price, exchange):
        pass

    def transfer(self, coin, exchangeA, exchangeB):
        pass


l = task.LoopingCall(doWork)
l.start(timeout)

reactor.run()