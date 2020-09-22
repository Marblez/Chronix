import Library
import talib

class DiffCrossoverStrategy(Library.Strategy):
    """
    Simple moving average crossover strategy
    """
    def __init__(self, balance, symbol, horizon):
        Library.Strategy.__init__(self, balance, symbol, horizon)
        self.prev = 0
        self.indicators = {}
        self.candles = self.getCandles() 
        self.indicators['fast2'] = talib.SMA(self.candles.close[-25:], 20)[-1]
        self.indicators['fast1'] = talib.SMA(self.candles.close[-25:], 20)[-2]
        self.indicators['slow2'] = talib.SMA(self.candles.close[-50:], 50)[-1]
        self.indicators['slow1'] = talib.SMA(self.candles.close[-50:], 50)[-2]

    def checkActions(self):
        val = self.getValue() / 3
        if self.indicators['fast1'] < self.indicators['slow1'] and self.indicators['fast2'] > self.indicators['slow2'] and self.holdings <= 0:
            if self.holdings == 0:
                self.buy(val / self.candles[-1])
            else:
                self.buy(self.holdings)
        elif self.indicators['fast1'] > self.indicators['slow1'] and self.indicators['fast2'] < self.indicators['slow2']  and self.holdings >=0:
            if self.holdings == 0:
                self.sell(val / self.candles[-1])
            else:
                self.sell(self.holdings)

    def update(self):
        self.candles = self.getCandles()
        self.indicators['fast2'] = talib.SMA(self.candles.close[-25:], 20)[-1]
        self.indicators['fast1'] = talib.SMA(self.candles.close[-25:], 20)[-2]
        self.indicators['slow2'] = talib.SMA(self.candles.close[-50:], 50)[-1]
        self.indicators['slow1'] = talib.SMA(self.candles.close[-50:], 50)[-2]

strategy = DiffCrossoverStrategy(10000, "XLM/USD", "5m")
Library.begin(strategy)

