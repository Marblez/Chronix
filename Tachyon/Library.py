import FirebaseClient
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
    """
    Base Strategy Class; Extend this class when building strategies
    """

    def __init__(self, balance, symbol, horizon):
        self.name = str(self.__class__.__name__) + ":" + str(symbol)
        print(self.name)
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
        return self.balance + self.holdings * self.price

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

    def setHolding(self, percentage):
        diff = percentage - ((self.price * self.holdings)/self.getValue())
        if diff > 0.15:
            self.buy((self.getValue() * diff) / self.price)
        elif diff < -0.15:
            self.sell(abs(self.getValue() * diff) / self.price)

    def sell(self, amount):
        if abs((self.holdings - amount)) * self.price > self.getValue():
            print("Not enough margin for shortsale")
        else:
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
        # TODO: Push logs then set actions to none
        log = Log(self.name, self.balance, self.holdings, self.price, self.actions)
        self.actions = [] 

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
    def __init__(self, name, balance, holdings, price, actions):
        self.name = name
        self.value = balance + holdings * price
        self.balance = balance
        self.holdings = holdings
        self.price = price
        self.actions = actions
        self.log()
    
    def log(self):
        FirebaseClient.update(self.name, self.value, self.balance, self.holdings, self.price, self.actions)

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

def kelly(win_rate, win_amount, loss_amount):
    if win_amount == 0:
        return -0.8
    if loss_amount == 0:
        return 0.8
    kelly = win_rate - ((1-win_rate) / (win_amount/loss_amount));
    if kelly > 0.8:
        return 0.8
    elif kelly < -0.8:
        return -0.8
    return kelly
