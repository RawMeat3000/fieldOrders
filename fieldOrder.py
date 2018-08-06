import itertools

"""
TODO:
-Use half of every sell to rebuy
-Refresh every... 5? minutes, more isn't needed.
"""


import datetime
import gettext
import sys
import time
from decimal import Decimal, DefaultContext, ROUND_HALF_DOWN
import numpy

import hitBTC

"""
TODO:
-Use half of every sell to rebuy
-Refresh every... 5? minutes, more isn't needed.
"""


TRADING_PAIR = 'ETH'

class Number:
    def __init__(self):
        stuff = self


class FieldOrder():
    """
    The ultimate trading tool. Fat finger catcher, always profit taking, always rebuying with confidence of an eventual return to base. Thanks Luc!
    Parameters:
        orderType: string : 'buy' or 'sell'
        buyStart: Decimal : Highest price to begin buying at
        buyEnd: Decimal : Lowest price to buy at
        capitalToSpent : Decimal : Amount of BTC or ETH allocated to the transaction
        sellStart:
        sellEnd:
        sellBreakEven:
        weight: Optional
        rounding:
        confidencePercent: int : Optional, basically equals the % under base to have finished selling to break even
        minimumSellPercent: int : Optional, Start selling at this % profit
    """
    def __init__( self, coin, orderType, buyStart, buyEnd, capitalToSpend, sellStart, sellEnd, sellBreakEven, coinsToSell,
                        weight=1):#, confidencePercent=100, lowestSellPercent=3, rebuy=False ):

        tickerData = hitBTC.get_ticker(coin + TRADING_PAIR)
        print(tickerData)

        symbolData = hitBTC.get_symbol(coin + TRADING_PAIR)
        print(symbolData)

        DefaultContext.prec = 8
        DefaultContext.rounding = ROUND_HALF_DOWN

        self.quantityIncrement = Decimal(symbolData['quantityIncrement'] )
        self.tickSize = Decimal(symbolData['tickSize'])

        self.orderType = orderType
        self.coin = coin
        self.capitalToSpend = capitalToSpend
        self.coinsToSell = coinsToSell
        self.weight = weight

        # This would be an sell only order.
        if sellStart:
            self.sellStart = sellStart
            self.sellEnd = sellEnd
            self.orderRange = sellEnd - sellStart
            # magic
            self.fieldSell()

        if buyStart:
            # Calculate order placement based on stuff I made up and forgot
            self.breakEvenSellStart = buyStart + (buyStart * lowestSellPercent)
            self.breakEvenStep = (sellBreakEven - self.breakEvenSellStart) / numberOfOrders
            self.breakEvenSellEnd = sellBreakEven + self.breakEvenStep
            # places the break even orders
            self.placeFieldOrder()

            self.profitSellStart = sellBreakEven + sellBreakEven * ( lowestSellPercent * 2 )
            self.profitStep = ( sellEnd - self.profitSellStart ) / numberOfOrders
            self.profitSellEnd = sellEnd + self.profitStep

            self.buyStart = "heh?"

            # places the profit orders
            self.placeFieldOrder()

        #self.monitorOrders()

    def fprint(self, message, printMe):
        print(f"{message} {printMe:.8f}")

    def weightedStep(self, start, end):
        """
        Returns dictionary of {price: amount}
        """
        if self.orderType == 'buy':
            maxOrders = self.capitalToSpend / self.tickSize # should be  self.capitalToSpend * buyPrice
        if self.orderType == 'sell':
            # This is the most number of orders possible
            maxOrders = self.orderRange / self.tickSize

            self.fprint("Sell range:", self.orderRange)

            numSteps = self.coinsToSell / self.quantityIncrement
            # just to be safe
            if numSteps > maxOrders:
                print("NUM STEPS WAS MORE THAN MAX ORDERS", numSteps, maxOrders)
                numSteps = maxOrders

            self.fprint("Step size:", numSteps)

            stepSize = self.coinsToSell / numSteps

            numRange = numpy.arange(start, end, stepSize)
            print(numRange)

    def fieldSell(self):
        #print("Weight:", self.weight)
        for x in self.weightedStep(self.sellStart, self.sellEnd):
            if self.weight:
                print ("Placing sell order at", x) # todo: round decimal place
                # API CALL
                debugTime = .01
                refreshTime = .5
                # coinigy only allows 2 orders per second
                time.sleep(debugTime)

    def monitorOrders(self, fieldOrder):
        """
        Main loop, monitors trades
        """
        #ui = Application()
        COINS = self.refreshCoins()
        while True:
            currentPrice = self.priceCheck(self.coinTicker)
            previousPrice = 0

            #
            # Check if anything has sold

            for coin in COINS:
                for sellOrder in existingSellOrders(coin):
                    if sellOrder.price > previousLow(1):#minute
                        sellPrice = sellOrder.units#math
                        print("dingus")

            # if current price less than 8% of previousPrice
            # wipe current field orders
            # set new ones
            previousPrice = currentPrice

            time.sleep(60)


coin = 'BSTN'
buyStart = 0
buyEnd = '.0000011'
capitalToSpend = '.05' # ETH
sellStart = '.00000170'
sellEnd = '.00000210'
sellBreakEven = '.0012'
coinsToSell = 30000
weight = 1
confidencePercent = 80
lowestSellPercent = 2
rebuy = False

order = FieldOrder(coin, 'sell',
                    Decimal(buyStart), Decimal(buyEnd), Decimal(capitalToSpend),
                    Decimal(sellStart), Decimal(sellEnd), Decimal(sellBreakEven),
                    Decimal(coinsToSell),
                    Decimal(weight))
