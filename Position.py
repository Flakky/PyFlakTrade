class Position:
    close_time = None
    close_value = None

    def __init__(self, time, value: int, amount: int = 1, **kwargs):
        self.open_time = time
        self.open_value = value
        self.amount = amount
        self.stop_loss = kwargs.stopLoss
        self.take_profit = kwargs.takeProfit

    def close(self, time, value: int):
        self.close_time = time
        self.close_value = value
