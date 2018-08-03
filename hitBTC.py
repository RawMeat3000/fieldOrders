import requests


URL = "https://api.hitbtc.com/api/2"
session = requests.session()
session.auth = ("7fd5f10d29a2609f615b6a3546577b99", "020bf255763ead3e848ce5155a44cbee")

def get_symbol(coin_ticker):
    """Get symbol.
    [{
        "id": "ETHBTC",
        "baseCurrency": "ETH",
        "quoteCurrency": "BTC",
        "quantityIncrement": "0.001",
        "tickSize": "0.000001",
        "takeLiquidityRate": "0.001",
        "provideLiquidityRate": "-0.0001",
        "feeCurrency": "BTC"
    }]
    """
    return session.get("%s/public/symbol/%s" % (URL, coin_ticker)).json()

def get_ticker(coin_ticker):
    """
    [{
        "ask": "0.050043",
        "bid": "0.050042",
        "last": "0.050042",
        "open": "0.047800",
        "low": "0.047052",
        "high": "0.051679",
        "volume": "36456.720",
        "volumeQuote": "1782.625000",
        "timestamp": "2017-05-12T14:57:19.999Z",
        "symbol": "ETHBTC"
    }]
    """
    return session.get("%s/public/ticker/%s" % (URL, coin_ticker)).json()


def get_orderbook(symbol_code):
    """Get orderbook. """
    return session.get("%s/public/orderbook/%s" % (URL, coin_ticker)).json()

def get_trading_balance():
    """Get trading balance."""
    return session.get("%s/trading/balance" % URL).json()

def transfer(currency_code, amount, to_exchange):
    return session.post("%s/account/transfer" % URL, data={
            'currency': currency_code, 'amount': amount,
            'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
        }).json()

def new_order(client_order_id, coin_ticker, side, quantity, price=None):
    """Place an order."""
    data = {'symbol': coin_ticker, 'side': side, 'quantity': quantity}

    if price is not None:
        data['price'] = price

    return session.put("%s/order/%s" % (URL, client_order_id), data=data).json()

def get_order(client_order_id, wait=None):
    """Get order info."""
    data = {'wait': wait} if wait is not None else {}

    return ession.get("%s/order/%s" % (URL, client_order_id), params=data).json()

def cancel_order(client_order_id):
    """Cancel order."""
    return session.delete("%s/order/%s" % (URL, client_order_id)).json()

def get_transaction(transaction_id):
    """Get transaction info."""
    return session.get("%s/account/transactions/%s" % (URL, transaction_id)).json()