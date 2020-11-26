class Position:
    close_time = None
    close_value = None

    def __init__(self, time, value, amount=1, **kwargs):
        self.open_time = time
        self.open_value = value
        self.amount = amount
        self.stop_loss = kwargs.stopLoss
        self.take_profit = kwargs.takeProfit

    def close(self, time, value):
        self.close_time = time
        self.close_value = value


class Trader:

    openedPosition = None
    closedPositions = []

    def shouldOpenPosition(self, trade_data):
        return True

    def shouldClosePosition(self, trade_data):
        if self.openedPosition is not None:
            last_value = trade_data[-1]
            if last_value > self.openedPosition.stop_loss or last_value < self.openedPosition.take_profit:
                return True
            else:
                return False
        else:
            return False

    def openPosition(self, position):
        self.openedPosition = position

    def closePosition(self, time, value):
        self.openedPosition.close(time, value)
        self.closedPositions.append(self.openedPosition)
        self.openedPosition = None
