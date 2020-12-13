import time
import StocksReciever
import Position
import Strategy
import datetime
import StockValue
import typing


class Trader:
	strategy: Strategy.Strategy = None
	budget: float = 0.0
	posMaxValue: float = 0.0
	allowed_stocks: list[str] = []
	openedPosition: Position.Position = None
	closedPositions: list[Position.Position] = []
	tradeInProgress: bool = False
	backtest: BackTestMode = None

	def __init__(self, strategy: Strategy.Strategy, budget: float, position_max_value: float, allowed_stocks: list[str]):
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

	def closePosition(self, close_time: datetime.datetime, value: float):
		self.openedPosition.close(close_time, value)
		self.closedPositions.append(self.openedPosition)

		self.budget += value

		print("Position close: {p}".format(p=str(self.openedPosition)))

		self.openedPosition = None

	def recieveTradeData(self):
		trade_data = []
		return trade_data

	def start(self):
		self.tradeInProgress = True
		while self.tradeInProgress:
			self.update()
			time.sleep(5)

	def stop(self):
		self.tradeInProgress = False

	def enableBacktestMode(self, test_trade_data: typing.List[StockValue.StockValue]):
		self.backtest = BackTestMode(test_trade_data)


class BackTestMode:
	trade_data: typing.List[StockValue.StockValue]) = []
	current_time: datetime.datetime = None
	
	def __init__(self, trade_data: typing.List[StockValue.StockValue])):
		self.trade_data = trade_data
		self.current_time = trade_data[0].time_start