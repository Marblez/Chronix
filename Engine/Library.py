import BinanceClient
import threading
import numpy as np

def begin(strategy):
    # Setup for strategy
    threading.Timer(strategy.int_horizon, run, [strategy]).start()
    
def run(strategy):
    strategy.tick()
    threading.Timer(strategy.int_horizon, run, [strategy]).start()

# Data Structures

class Strategy:

    def __init__(self, balance, symbol, horizon):
        self.balance = balance
        self.holdings = 0
        self.symbol = symbol
        self.string_horizon = horizon
        self.int_horizon = compute_horizon(horizon)
        self.actions = []
        self.price = 0
        # Trading Strategy Assumptions
        self.fee = 0.001
    
    def getValue(self):
        return self.balance() + self.holdings * self.price

    def getData(self):
        quote = BinanceClient.getQuote(self.symbol)
        if quote.valid:
            self.price = quote.getPrice() 
        else:
            raise Exception("getPrice() returned in invalid response")
        return self.price

    def update(self):
        print("Please override the update function")

    def checkActions(self):
        print("Please override checkActions function")

    def Liquidate(self): 
        if self.holdings > 0:
            self.sell(self.holdings)
        elif self.holdings < 0:
            self.buy(self.holdings * -1)

    def sell(self, amount):
        self.balance = self.balance + (amount * self.price * (1 - self.fee))
        self.holdings = self.holdings - amount
        self.actions.append(Action("SELL", amount))

    def buy(self, amount):
        if self.balance < amount * self.price * (1 + self.fee):
            print("Insufficient balance for amount " + str(amount) + " at price " + str(self.price))
        else:
            self.balance = self.balance - (amount * self.price * (1 + self.fee))
            self.holdings = self.holdings + amount
            self.actions.append(Action("BUY", amount))

    def log(self):
        # TODO: Push logs then set to none
        log = Log(self.balance, self.holdings, self.price, self.actions)
        self.actions = [] 
        log.print();

    def tick(self):
        self.getData()
        self.update()
        self.checkActions()
        self.log()

    def getCandles(self):
        return BinanceClient.getTickerData(self.symbol, self.string_horizon)

class Action:
    def __init__(self, action, amount):
        self.action = action
        self.amount = amount 

class Log:
    def __init__(self, balance, holdings, price, actions):
        self.value = balance + holdings * price
        self.balance = balance
        self.holdings = holdings
        self.price = price
        self.actions = actions

    def print(self):
        print("Value: " + str(self.value) + "\n")
        print("Balance: " + str(self.balance)  + "\n")
        print("Holdings: " + str(self.holdings) + "\n")
        print("Price: " + str(self.price) + "\n")

class Quote:
    def __init__(self, bid, ask):
        self.bid = bid
        self.ask = ask
        self.valid = bid is not None and ask is not None
        if self.valid:
            self.spread = bid - ask
        else:
            self.spread = 0

    # Where the bid and ask meet
    def getPrice(self):
        return (self.bid + self.ask) / 2.0

class Candles:
    def __init__(self, candles):
        highlist = []
        lowlist = []
        closelist = []
        for i in range(0, len(candles)):
            highlist.append(candles[i][2])
            lowlist.append(candles[i][3])
            closelist.append(candles[i][4])
        self.high = np.asarray(highlist, dtype=np.double)
        self.low = np.asarray(lowlist, dtype=np.double)
        self.close = np.asarray(closelist, dtype=np.double)
    
class Cache:
    def __init__(self, capacity):
        self.capacity = capacity 
        self.data = []
        self.size = 0

    def add(self, data):
        if size == capacity:
            self.data.pop()
            self.size = self.size - 1
        self.data.append(data)
        self.size = self.size + 1

# Other functions and shit
def compute_horizon(horizon):
    unit = horizon[-1]
    val = int(horizon[:-1])
    if unit == 'm':
        val = val * 60
    elif unit == 'h':
        val = val * 3600
    elif unit == 'd':
        val = val * 86400
    return val
