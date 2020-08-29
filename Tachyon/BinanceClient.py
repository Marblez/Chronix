import ccxt
import Library
from binance.client import Client
import os.path
import pandas as pd
from datetime import timedelta, datetime
from dateutil import parser
import math

# ccxt docs https://buildmedia.readthedocs.org/media/pdf/ccxt/stable/ccxt.pdf

apiKey = '25HUOrJu76evPWNCJtSDydExaKtdB6DjyItVW5lTYSzEe2NgAvMsfLfuuX8Ake1m'
apiSecret = 'vBaUNet4o7N2qVA3lW84Is6RXFnAt4Q6Dk6qdfiR1VzAOi0vO4Ujq2eCq0qHjCfP'

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

## Fetching All Candles
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=apiKey, api_secret=apiSecret)

def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new

def get_all_binance(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2019', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    return data_df
