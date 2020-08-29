import Library

class TemplateStrategy(Library.Strategy):
    """
    Description of this template strategy
    """
    def __init__(self, balance, symbol, horizon):
        Library.Strategy.__init__(self, balance, symbol, horizon)
        self.prev = 0

    def checkActions(self):
        if self.price > self.prev:
            self.buy(0.01)
        self.prev = self.price

strategy = TemplateStrategy(10000, "BTC/USD", "3s")
Library.begin(strategy)
