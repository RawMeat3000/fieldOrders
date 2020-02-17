import itertools

"""
TODO:

"""

import sys
import time
import gettext
import datetime
import schedule

import mpmath as mp

import python-kucoin-develop.client as ku

"""
TODO:
Refresh once a minute
get all markets

"""


class FieldOrder():
    """
    The ultimate trading tool (once it's finished). Fat finger catcher, always profit taking, always rebuying with confidence of an eventual return to base. Thanks Luc!
    Parameters:
        orderType: string : 'buy' or 'sell'
        buyStart: Decimal : Highest price to begin buying at
        buyEnd: Decimal : Lowest price to buy at
        capitalToSpend : Decimal : Amount of BTC or ETH allocated to the transaction
        sellStart:
        sellEnd:
        sellBreakEven:
        weight: Optional
        rounding:
        confidencePercent: int : Optional, basically equals the % under base to have finished selling to break even
        minimumSellPercent: int : Optional, Start selling at this % profit

    ALternate usage. Buy at all time low, or some aveage of ATL and current price, only, ever. Sell at whatever 100% you want. Under 10,000% definitely.
    """
    def __init__( self, coin, buyStart, buyEnd, capitalToSpend, sellStart, sellEnd, sellBreakEven, coinsToSell, weight=1):
        #, confidencePercent=100, lowestSellPercent=3, rebuy=False ):

        # BOT
        TRADING_PAIR = "USDT"
        PUB = "5e4a22d29a8f450008d86f51"
        SEC = "6e2a49f0-5d86-45cf-a638-7e29fb561090"
        TRADING = "649587"

        ku.Client(PUB, SEC, TRADING)
        cpia = cryptopia.Cryptopia(PUB, SEC)

        market = coin + '/' + TRADING_PAIR
        print(market)

        tickerData = cpia.get_market(market)
        print("Ticker data:", tickerData)

        symbolData = cpia.get_openorders(market)
        print("Symbol data:", symbolData)

        allHistory = cpia.get_history(market)
        print("Market history:", allHistory)

        pastOrders = cpia.get_orders(market)
        print("Past orders:", pastOrders)

        marketHistory = cpia.get_market(market)
        print("Market history:", marketHistory)

        quantityIncrement = mp.mpf( symbolData['quantityIncrement'] )
        tickSize = mp.mpf( symbolData['tickSize'] )

        mp.mp.dps = len( str(self.tickSize).split('.')[1] )

         # bot should never trade more than this, send an email every day we exceed it
        self.maxCapital = 5000

        self.orderType = None
        self.coin = coin
        self.capitalToSpend = capitalToSpend
        self.coinsToSell = coinsToSell
        self.weight = weight
        self.numOrders = 5 # TODO: Actually calculate this

        # This would be an sell only order.
        if sellStart:
            self.orderType = "buy"
            self.sellStart = sellStart
            self.sellEnd = sellEnd
            self.orderRange = sellEnd - sellStart
            # magic
            self.fieldSell()

        if buyStart:
            self.orderType = "sell"
            # Calculate order placement based on stuff I made up and forgot
            self.breakEvenSellStart = buyStart + (buyStart * lowestSellPercent)
            self.breakEvenStep = (sellBreakEven - self.breakEvenSellStart) / self.numOrders
            self.breakEvenSellEnd = sellBreakEven + self.breakEvenStep
            # places the break even orders
            self.placeFieldOrder()

            self.profitSellStart = sellBreakEven + sellBreakEven * ( lowestSellPercent * 2 )
            self.profitStep = ( sellEnd - self.profitSellStart ) / self.numOrders
            self.profitSellEnd = sellEnd + self.profitStep

            self.buyStart = "heh?"

            # places the profit orders
            self.placeFieldOrder()

        #self.monitorOrders()

    def weightedStep(self, start, end):
        """
        Returns dictionary of {price: amount}
        """
        if self.orderType == 'buy':
            maxOrders = self.capitalToSpend / self.tickSize # should be  self.capitalToSpend * buyPrice
        if self.orderType == 'sell':
            # This is the most number of orders possible
            maxOrders = self.orderRange / self.tickSize

            print("Sell range:", self.orderRange)

            numSteps = self.coinsToSell / self.quantityIncrement
            # just to be safe
            if numSteps > maxOrders:
                print("NUM STEPS WAS MORE THAN MAX ORDERS", numSteps, maxOrders)
                numSteps = maxOrders

            print("Step size:", numSteps)

            coinsInOrder = self.coinsToSell / numSteps

            sellPrices = mp.linspace(start, end, maxOrders)

            orderDetails = []
            for sellPrice in sellPrices:
                orderDetails.append( (coinsInOrder, sellPrice) )

            return orderDetails

    def fieldSell(self):
        orderDetails = self.weightedStep(self.sellStart, self.sellEnd)
        print("Weight:", self.weight)
        for numCoins, sellPrice in orderDetails:
            if self.weight:
                print("Selling %.8f at %.8f"%(numCoins, sellPrice)) # todo: round decimal place
                # API CALL
                debugTime = .01
                refreshTime = .5
                # coinigy only allows 2 orders per second
                time.sleep(debugTime)

    def getCurrentSellOrders():
        print "stuff"

    def main(self, fieldOrder):
        """
        Main loop, monitors trades
        """
        #ui = Application()
        COINS = self.refreshCoins() # ALL COINS
        while True:
            currentPrice = self.priceCheck(self.coinTicker)
            previousPrice = 0

            #
            # Check if anything has sold
            for coin in COINS:
                existingSellOrders =  getCurrentSellOrders(coin)
                for sellOrder in existingSellOrders:
                    if sellOrder.price > previousLow(1):#minute
                        sellPrice = sellOrder.units#math
                        print("dingus")




            # if current price less than 8% of previousPrice
            # wipe current field orders
            # set new ones
            previousPrice = currentPrice

            time.sleep(.1)


coin = 'WC'
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
                    mp.mpf(buyStart), mp.mpf(buyEnd), mp.mpf(capitalToSpend),
                    mp.mpf(sellStart), mp.mpf(sellEnd), mp.mpf(sellBreakEven),
                    mp.mpf(coinsToSell),
                    mp.mpf(weight))
