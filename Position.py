import datetime


class Position:
    open_time: datetime.datetime = datetime.datetime.min
    close_time: datetime.datetime = datetime.datetime.min
    open_value: float = 0.0
    close_value: float = 0.0
    amount: int = 1
    stop_loss: float = 0.0
    take_profit: float = 99999999.0

    def __init__(self, time: datetime.datetime, value: int, amount: int = 1, **kwargs):
        self.open_time = time
        self.open_value = value
        self.amount = amount
        self.stop_loss = kwargs.get("stop_loss", 0)
        self.take_profit = kwargs.get("take_profit", 99999)

    def close(self, time: datetime.datetime, value: int):
        self.close_time = time
        self.close_value = value
