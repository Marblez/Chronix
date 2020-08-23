import ccxt
import Library
# ccxt docs https://buildmedia.readthedocs.org/media/pdf/ccxt/stable/ccxt.pdf

apiKey = '25HUOrJu76evPWNCJtSDydExaKtdB6DjyItVW5lTYSzEe2NgAvMsfLfuuX8Ake1m'
apiSecret = 'vBaUNet4o7N2qVA3lW84Is6RXFnAt4Q6Dk6qdfiR1VzAOi0vO4Ujq2eCq0qHjCfP'

# Sets exchange api key and secret for ccxt
# Exchange id can be changed to use other exchanges, for example: to use binance.com instead of binance.us, change the id to 'binance'
exchange_id = 'binanceus'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': apiKey,
    'secret': apiSecret,
    'enableRateLimit': True,
    'options': { 'adjustForTimeDifference': True }
})

markets = exchange.load_markets()
def getQuote(symbol):
    orderbook = exchange.fetch_order_book (symbol)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    return Library.Quote(bid, ask)

def getTickerData(ticker, horizon):
    return Library.Candles(exchange.fetch_ohlcv(ticker, horizon))

def getAvailableCurrencies():
    return exchange.fetch_currencies()

def getBalance():
    return exchange.fetch_balance()

def makePurchase(amt, price):
    symbol = 'BTC/USD'
    type = 'market'  # 'limit' or 'market'
    side = 'buy'  # 'buy' or 'sell'
    amount = amt
    price = None  # or None
    params = {
        'test': True,  # test if it's valid, but don't actually place it
    }
    return exchange.create_order(symbol, type, side, amount, price, params)


def makeSale(amt, price):
    symbol = 'BTC/USD'
    type = 'market'  # ' limit' or 'market'
    side = 'sell'  # 'buy' or 'sell'
    amount = amt
    price = price  # or None
    params = {
        'test': False,  # test if it's valid, but don't actually place it
    }
    return exchange.create_order(symbol, type, side, amount, price, params)


def makeTestOrder():
    symbol = 'BTC/USDT'
    type = 'limit'  # or 'market'
    side = 'sell'  # or 'buy'
    amount = .001
    price = 10000.00  # or None
    params = {
    'test': True,  # test if it's valid, but don't actually place it
    }
    return exchange.create_order(symbol, type, side, amount, price, params)

def getMarkets():
    return print(exchange.id, markets)

