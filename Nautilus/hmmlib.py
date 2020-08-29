import pandas as pd
import matplotlib.pyplot as plt
import math
import time
from tqdm import tqdm_notebook 
from hmmlearn import hmm
import seaborn as sns
from sklearn.metrics import mean_squared_error

class HMM:
    """
    Class for training and maintaining hmm models
    """

    def __init__(self, regime_count, iterations, candles, compression_factor, window):
        self.regime_count = regime_count
        self.iterations = iterations
        self.compression_factor = compression_factor
        self.candles = self.process_candles(candles, compression_factor, window)
        self.model = None
        self.next = []
        self.refresh_count = 0
        self.refresh_threshold = 10

    def add(self, price):
        self.next.append(price)
        if len(self.next) == self.compression_factor:
            returns = (self.next[-1] - self.next[0]) / self.next[0]
            volatility = mean_squared_error(self.next, [sum(self.next) / len(self.next)] * len(self.next))
            self.obs.append([returns, volatility])
            self.next = []
            self.refresh_count += 1
            if self.refresh_count == self.refresh_threshold:
                self.train()
            return True
        return False

    def process_candles(self, candles, compression_factor, window):
        candles = candles[-compression_factor * window:]
        counter = 0
        obs = []
        for i in range(0, window):
            temp = []
            for j in range(0, compression_factor):
                temp.append(candles[counter])
                counter += 1
            returns = (temp[-1] - temp[0]) / temp[0]
            volatility = mean_squared_error(temp, [sum(temp) / len(temp)] * len(temp)) 
            obs.append([returns, volatility])
        self.obs = obs
        return candles

    def train(self):
        self.obs = self.obs[self.refresh_threshold:]
        self.model = hmm.GaussianHMM(n_components = regimes, covariance_type="full", n_iter = self.iterations)
        self.model.fit(self.obs)

    def predict(self):
        self.predictions = self.model.predict(self.obs) 
        return self.predictions[-1] 
    
    def transmat(self):
        return self.model.transmat_        

    def getRegimeReturns(self):
        regime_val = []
        regime_count = []
        for i in range(0, self.regime_count):
            regime_val.append(0)
            regime_count.append(0)

        for i in range(0, len(self.obs)):
            regime_count[self.predictions[i]] += 1
            regime_val[self.predictions[i]] += self.obs[i][0]
        
        for i in range(0, self.regime_count):
            regime_val[i] = regime_val[i] / regime_count[i]

        return regime_val



