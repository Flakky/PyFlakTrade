import time
import StocksReciever
import Position
import Strategy


class Trader:
	openedPosition = None
	closedPositions = []
	tradeInProgress = False
	backtest = {"testMode": False, "tradeData": {}, "testCurrentTime": None}

	def __init__(self, strategy: Strategy.Strategy, budget: float, position_max_value: float, allowed_stocks):
		self.strategy = strategy
		self.budget = budget
		self.posMaxValue = position_max_value
		self.allowed_stocks = allowed_stocks

	def update(self):
		if self.strategy is None:
			return

		trade_data = self.recieveTradeData()

		if self.openedPosition is not None:
			if self.strategy.shouldClosePosition(trade_data, self.openedPosition):
				self.closePosition()
		else:
			if self.strategy.shouldOpenPosition(trade_data):
				open_value = trade_data[-1].value
				position = Position.Position(
					0,
					open_value,
					1,
					stopLoss=open_value - (open_value / 100),
					takeProfit=open_value + (open_value / 100 * 2)
				)
				self.openPosition(position)

	def openPosition(self, position: Position.Position):
		self.openedPosition = position

		self.budget -= position.open_value

		print("Position open: {p}".format(p=str(position)))

	def closePosition(self, close_time, value: float):
		self.openedPosition.close(close_time, value)
		self.closedPositions.append(self.openedPosition)

		self.budget += value

		print("Position close: {p}".format(p=str(self.openedPosition)))

		self.openedPosition = None

	def recieveTradeData(self):
		trade_data = {"12.01.2020, 23.54": 125.534}
		return trade_data

	def start(self):
		self.tradeInProgress = True
		while self.tradeInProgress:
			self.update()
			time.sleep(5)

	def stop(self):
		self.tradeInProgress = False

	def enableBacktestMode(self, test_trade_data):
		self.backtest["testMode"] = True
		self.backtest["tradeData"] = test_trade_data
