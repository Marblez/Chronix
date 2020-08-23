import Library
import talib

class MACrossoverStrategy(Library.Strategy):
    """
    Simple moving average crossover strategy
    """
    def __init__(self, balance, symbol, horizon):
        Library.Strategy.__init__(self, balance, symbol, horizon)
        self.prev = 0
        self.indicators = {}
        self.candles = self.getCandles() 
        self.indicators['fast'] = talib.EMA(self.candles.close[-10:], 10)[-1]
        self.indicators['slow'] = talib.SMA(self.candles.close[-10:], 10)[-1] 

    def checkActions(self):
        if self.indicators['fast'] > self.indicators['slow'] and self.holdings <= 0:
            self.buy(0.5)
        elif self.indicators['fast'] < self.indicators['slow'] and self.holdings >=0:
            self.sell(0.5)

    def update(self):
        self.candles = self.getCandles()
        self.indicators['fast'] = talib.EMA(self.candles.close[-10:], 10)[-1]
        self.indicators['slow'] = talib.SMA(self.candles.close[-10:], 10)[-1]

strategy = MACrossoverStrategy(10000, "BTC/USD", "1m")
Library.begin(strategy)

