"""
Experiment to see if I can always buy and always sell perfect tops and perfect bottoms
Take 100% advantage of volatility. Trade any volitile chart with an overwhelming number of orders.
"""

import os
import sys
import time
import json
import logger
import datetime
import schedule
import itertools
import importlib


import mpmath as mp
sys.path.append(os.path.dirname(__file__) + "\\kucoin\\")
import kucoin.client as kucoin
importlib.reload(kucoin)

"""
TODO:
Refresh once a minute
get all markets


START DOWNLOADING ALL PRICE ACTION
KEEP LOCAL COPY of 1hr data
"""

class ChartHistory(object):
    def __init__(self):
        pass

class dobj(object):
    """
    Lets you use dict keys as object attributes
    kinda cool, but mostly just confusing in practice
    """
    def __init__(self, d):
        self.__dict__ = d

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

class FieldOrder():
    """
    The ultimate trading tool (once it's finished). Fat finger catcher, always profit taking, always rebuying with confidence of an eventual return to base. Thanks Luc!
    """
    def __init__(self):
        # BOT

        # never change these...
        self.base_currency = "USDT"
        self.exclude = []
        PUB = "5e4a22d29a8f450008d86f51"
        SEC = "6e2a49f0-5d86-45cf-a638-7e29fb561090"
        TRADING = "tthis_willbethebestBot15!"
        # /never change these...

        self.api = kucoin.Client(PUB, SEC, TRADING)

        self.log_file = open(os.path.dirname(__file__) + "\\{}.log".format(self.base_currency), 'a+')
        self.data_file = os.path.dirname(__file__) + "\\{}_data.json".format(self.base_currency)

        # BIG object that has all the data we really need
        self.data = self.open_json(self.data_file)
        #quantityIncrement = mp.mpf( symbolData['quantityIncrement'] )
        #tickSize = mp.mpf( symbolData['tickSize'] )

         # bot should ideally have a "capital" value of 50% the account value
        self.capital = 350
        self.orders_per_chart = 30
        # get wanted pairs and wanted data
        """
        {'symbol': 'TIME-ETH', 'quoteMaxSize': '99999999', 'enableTrading': True,
        'priceIncrement': '0.0000001', 'feeCurrency': 'ETH', 'baseMaxSize': '10000000000',
        'baseCurrency': 'TIME', 'quoteCurrency': 'ETH', 'market': 'ALTS',
        'quoteIncrement': '0.0000001', 'baseMinSize': '0.01', 'quoteMinSize': '0.0001',
        'name': 'TIME-ETH', 'baseIncrement': '0.000001', 'isMarginEnabled': False}
        """
        self.usdt_pairs = self.get_pairs()
        self.num_pairs = len(self.usdt_pairs)


        return

        # start the business
        self.manage_orders()

    def refresh(self, what):
        """
        accounts
        charts
        orders
        balances
        """
        # this only needs to be called if there's a new/removed market.
        # returns account ID numbers which can always be used
        if what == "accounts":
            self.accounts = [account for account in self.api.get_accounts()]
            self.account_ids = [account["id"] for account in self.accounts]
            for account_ids in self.account_ids:
                self.log(account_ids)
            for account in self.accounts:
                self.log(account)
                #self.log(self.api.get_account(account["id"]))
        elif what == "charts":
            for pair in self.usdt_pairs:
                self.start_time = 1510278278 # ~1 year ago
                self.curent_time = 1510278278
                self.api.get_kline_data(pair["symbol"], kline_type='1hour', start=None, end=None):
        elif what == "orders":
            print("something else")


    def log(self, *message):
        print(message)
        for msg in message:
            self.log_file.write(str(msg) + '\n')

    def open_json(self, json_file):
        if not os.path.isfile(json_file):
            with open(json_file, 'w+') as df:
                return json.load(df)
        else:
            with open(json_file, 'r') as df:
                return json.load(df)

    def save_json(self, json_file, data):
        json.dump(data, json_file)

    def get_balance(self):
        balance = {}


    def set_min_buy(self):
        """
        Some rules:
            We use ~50% of capital at any given time
            We set ~30 orders per chart
            Currently have about 79 USDT trading pairs
        """

    def get_price_history(self):
        trade_history = self.api.get_trade_histories()
        for trade in trade_history:
            self.log(trade)

    def get_usdt_pairs(self):
        """
        Gets all the SHITCOIN/USDT trading pairs and any additional information the bot might need
        """
        usdt_pairs = {}
        raw_symbols = self.api.get_symbols()
        '''
        {'symbol': 'GRIN-USDT', 'quoteMaxSize': '99999999', 'enableTrading': True, 'priceIncrement': '0.000001',
        'feeCurrency': 'USDT', 'baseMaxSize': '10000000000', 'baseCurrency': 'GRIN', 'quoteCurrency': 'USDT', 'market': 'USDS', 'quoteIncrement': '0.000001',
        'baseMinSize': '0.01', 'quoteMinSize': '0.01', 'name': 'GRIN-USDT', 'baseIncrement': '0.00000001', 'isMarginEnabled': False}
        '''

        for data in raw_symbols:
            if self.base_currency in data["symbol"]:
                pair = data["symbol"]
                quote, base = pair.split('-')
                if base == self.base_currency:
                    self.log(pair, quote)
                    # add/modify data here
                    usdt_pairs[quote] = data

        return usdt_pairs

    def get_pairs(self):
        usdt_pairs = self.get_usdt_pairs()
        self.log("Got data for {} pairs".format(len(usdt_pairs)))
        return usdt_pairs

    def manage_orders(self):
        """
        Goes through all open orders on pair, figured out if they're in range, wipe and recreate if adjustment is needed
        def get_orders(self, symbol=None, status=None, side=None, order_type=None, start=None, end=None, page=None, limit=None):
        """
        for coin, pair_info in self.usdt_pairs.items():
            orders = self.api.get_orders(pair_info["symbol"], status="active")
            self.log(coin, orders["totalNum"])
            if orders["totalNum"]:
                self.log(len(orders["items"]))
                for order in orders["items"]:
                    self.log(order)

                    self.log(mp.mpf())

                # ticker = current price action, bid/ask, etc
                ticker = self.api.get_ticker(pair_info["symbol"])
                self.log(ticker)
                return

if __name__ == "__main__":
    order = FieldOrder()

    # the rest on a timer
    schedule.every(1).days.do(order.get_pairs)
    schedule.every(1).minutes.do(order.manage_orders)
