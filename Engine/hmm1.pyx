import Library
import talib
import BinanceClient
import hmmlib
import numpy as np

class hmm1(Library.Strategy):
    """
    Using a hidden markov model to trade ETHUSD
    """
    def __init__(self, balance, symbol, horizon):
        Library.Strategy.__init__(self, balance, symbol, horizon)
        self.candles = self.getCandles()
        self.regime_count = 4
        self.iterations = 75
        self.hmm = hmmlib.HMM(self.regime_count, self.iterations, self.candles, 240, 180)
        self.regimes = {}

    def getCandles(self):
        return list(np.asarray(BinanceClient.get_all_binance("ETHUSDT", "5m", save = True)['close'], dtype= np.float))

    def checkActions(self):
        pass

    def update(self):
        # Get new 5m bar
        if self.hmm.add(self.getData()):
            self.forecast()

    def forecast(self):
        next = self.hmm.predict()
        transmat = self.hmm.transmat()
        regime_returns = self.hmm.getRegimeReturns()

        # Calculating Win Rate, Win/Loss amount ratio, and expected value
        win_rate = 0
        win_amount = 0
        loss_amount = 0
        expected_value = 0

        transarr = transmat[next]
        for i in range(0, self.regime_count):
            expected_value += (regime_returns[i] * transarr[i])
            if regime_returns[i] > 0:
                win_rate += transarr[i]
                win_amount += regime_returns[i]
            else:
                loss_amount -= regime_returns[i]

        position = Library.kelly(win_rate, win_amount, loss_amount)

        #Low-Pass Filter
        if abs(expected_value) > 0.003:
            self.setHolding(position)

strategy = hmm1(10000, "ETH/USD", "5m")
Library.begin(strategy)

