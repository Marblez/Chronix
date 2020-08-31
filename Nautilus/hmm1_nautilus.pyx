import hmmlearn
import talib
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.metrics import mean_squared_error
import Library
import FirebaseClient
import hmmlib

class hmm1_nautilus():
    """
    Using a hidden markov model to trade ETHUSD
    """
    def __init__(self, balance, symbol, horizon):
        self.balance = balance
        self.position = 0
        self.symbol = symbol
        self.horizon = horizon
        ########## VARIABLES ##############
        self.regime_count = 4
        self.compression = 240
        self.step_range = range(30, 151, 10) 
        self.windows = range(50, 251, 10)
        ####################################
        self.counter = self.windows[-1] * self.compression + 1
        self.candles = self.getCandles()
        self.run()

    def run(self):
        for step in self.step_range:
            for window in self.windows:
                self.hmm = hmmlib.HMM(self.regime_count, step, self.candles[:self.windows[-1]*self.compression], self.compression, window)
                self.simulate("ETHUSD" + str(step) + ":" + str(window))

    def getCandles(self):
        data = Library.get_all_binance(self.symbol, self.horizon, save = True)
        close = np.array(data.iloc[:,3].astype(float), np.float)[-279564:] # Jan 1 2018 - Present
        return close

    def simulate(self, name):
        # Hard Reset
        self.position = 0
        self.balance = 10000
        values = []
        positions = []
        prices = []
        for i in range(self.windows[-1] * self.compression + 1, len(self.candles)):
            if self.hmm.add(self.candles[i]):
                positions.append(self.position)
                values.append(self.position * self.candles[i] + self.balance)
                prices.append(self.candles[i])
                self.forecast(self.candles[i])
        FirebaseClient.log(name, "Position", positions)
        FirebaseClient.log(name, "Value", values)
        FirebaseClient.log(name, "Price", prices)

    def forecast(self, price):
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

        percentage = Library.kelly(win_rate, win_amount, loss_amount)
        
        #Low-Pass Filter
        if abs(expected_value) > 0.003:
            # Buy or sell here
            diff = percentage - (self.position * price) / (self.position * price + self.balance)
            if diff > 0 and self.balance > diff * (self.position * price + self.balance):
                old_balance = self.balance
                self.balance -= diff * (self.position * price + self.balance)
                self.position += (diff * (self.position * price + old_balance)) / price
            elif diff < 0 and self.position + (diff*(self.position*price + self.balance))/price > -1:
                old_balance = self.balance
                self.balance += -diff * (self.position * price + self.balance)
                self.position += (diff * (self.position * price + old_balance)) / price

strategy = hmm1_nautilus(10000, "ETHUSDT", "5m")

