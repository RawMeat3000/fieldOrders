""" This is a wrapper for Cryptopia.co.nz API """


import json
import time
import hmac
import hashlib
import base64
import requests

# using requests.compat to wrap urlparse (python cross compatibility over 9000!!!)
from requests.compat import quote_plus

class Cryptopia():
    """ A wrapper for cryptopia API """
    publicCommands = ['GetCurrencies', 'GetTradePairs', 'GetMarkets',
                        'GetMarket', 'GetMarketHistory', 'GetMarketOrders', 'GetMarketOrderGroups']
    privateCommands = ['GetBalance', 'GetDepositAddress', 'GetOpenOrders',
                        'GetTradeHistory', 'GetTransactions', 'SubmitTrade',
                        'CancelTrade', 'SubmitTip', 'SubmitWithdraw', 'SubmitTransfer']

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_currencies(self):
        """ Gets all the currencies """
        return self.api_query(command='GetCurrencies')

    def get_tradepairs(self):
        """ Gets all the trade pairs """
        return self.api_query(command='GetTradePairs')

    def get_markets(self):
        """ Gets data for all markets """
        return self.api_query(command='GetMarkets')

    def get_market(self, market):
        """ Gets market data """
        return self.api_query(command='GetMarket',
                              get_parameters={'market': market})

    def get_history(self, market):
        """ Gets the full order history for the market (all users) """
        return self.api_query(command='GetMarketHistory',
                              get_parameters={'market': market})

    def get_orders(self, market):
        """ Gets the user history for the specified market """
        return self.api_query(command='GetMarketOrders',
                              get_parameters={'market': market})
    '''
    def get_ordergroups(self, markets):
        """ Gets the order groups for the specified market """
        return self.api_query(command='GetMarketOrderGroups',
                              get_parameters={'markets': markets})
    '''
    def get_balance(self, currency):
        """ Gets the balance of the user in the specified currency """
        result, error = self.api_query(command='GetBalance',
                                       post_parameters={'Currency': currency})
        if error is None:
            result = result[0]
        return (result, error)

    def get_openorders(self, market):
        """ Gets the open order for the user in the specified market """
        return self.api_query(command='GetOpenOrders',
                              post_parameters={'Market': market})

    def get_tradehistory(self, market):
        """ Gets the trade history for a market """
        return self.api_query(command='GetTradeHistory',
                              post_parameters={'Market': market})

    def get_transactions(self, transaction_type):
        """ Gets all transactions for a user """
        return self.api_query(command='GetTransactions',
                              post_parameters={'Type': transaction_type})

    def submit_trade(self, market, trade_type, rate, amount):
        """ Submits a trade """
        return self.api_query(command='SubmitTrade',
                              post_parameters={'Market': market,
                                               'Type': trade_type,
                                               'Rate': rate,
                                               'Amount': amount})

    def cancel_trade(self, trade_type, order_id, tradepair_id):
        """ Cancels an active trade """
        return self.api_query(command='CancelTrade',
                              post_parameters={'Type': trade_type,
                                               'OrderID': order_id,
                                               'TradePairID': tradepair_id})

    def secure_headers(self, url, post_data):
        """ Creates secure header for cryptopia private api. """
        nonce = str(time.time())
        md5 = hashlib.md5()
        jsonparams = post_data.encode('utf-8')
        md5.update(jsonparams)
        rcb64 = base64.b64encode( md5.digest()).decode('utf-8' )

        signature = self.key + "POST" + quote_plus(url).lower() + nonce + rcb64
        hmacsignature = base64.b64encode(hmac.new(base64.b64decode(self.secret),
                                                  signature.encode('utf-8'),
                                                  hashlib.sha256).digest())
        header_value = "amx " + self.key + ":" + hmacsignature.decode('utf-8') + ":" + nonce
        return {'Authorization': header_value, 'Content-Type': 'application/json; charset=utf-8'}

    def api_query(self, command, get_parameters=None, post_parameters=None):
        """ Performs a generic api request """
        time.sleep(.1)
        if command in self.privateCommands:
            url = "https://www.cryptopia.co.nz/Api/" + command
            print(url)
            post_data = json.dumps(post_parameters)
            headers = self.secure_headers(url=url, post_data=post_data)

            req = requests.post(url, data=post_data, headers=headers)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            req.encoding = "utf-8-sig"
            req = req.json()
            if 'Success' in req and req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                error = req['Error'] if 'Error' in req else 'Unknown Error'
            return (result, error)
        elif command in self.publicCommands:
            market = list(get_parameters.values())
            print(market)
            if market:
                market = market[0].replace('/', '_')
            url = "https://www.cryptopia.co.nz/Api/" + command + "/" + market

            print(url)
            req = requests.get(url, params=get_parameters)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            req = req.json()
            print(req)
            if 'Success' in req and req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                error = req['Error'] if 'Error' in req else 'Unknown Error'
            return (result, error)
        else:
            return None, "Unknown feature"