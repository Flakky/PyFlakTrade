import time
import StocksReciever
import Position
import Strategies.Strategy as Strategy
import datetime
import StockValue
import typing


class BackTestMode:
	trade_data: typing.List[StockValue.StockValue] = []
	current_index: int = 0

	def __init__(self, trade_data: typing.List[StockValue.StockValue]):
		self.trade_data = trade_data


class Trader:
	strategy: Strategy.Strategy = None
	budget: float = 0.0
	posMaxValue: float = 0.0
	allowed_stocks: typing.List[str] = []
	openedPosition: Position.Position = None
	closedPositions: typing.List[Position.Position] = []
	tradeInProgress: bool = False
	backtest: BackTestMode = None

	def __init__(self, strategy: Strategy.Strategy, budget: float, position_max_value: float, allowed_stocks: typing.List[str]):
		self.strategy = strategy
		self.strategy.set_trader(self)
		
		self.budget = budget
		self.posMaxValue = position_max_value
		self.allowed_stocks = allowed_stocks

	def update(self):
		if not self.tradeInProgress or self.strategy is None:
			return

		trade_data = self.receiveTradeData()
		last_stock_value = trade_data[-1]
		trade_time = last_stock_value.time_end

		if self.openedPosition is not None:
			if self.strategy.shouldClosePosition(trade_data, self.openedPosition):
				self.closePosition(trade_time, last_stock_value.close_value)
		else:
			if self.strategy.shouldOpenPosition(trade_data):
				open_value = last_stock_value.close_value
				position = Position.Position(
					trade_time,
					open_value,
					self.budget // open_value,
					stop_loss=open_value - ((open_value / 100.0) * 0.5)
				)
				self.openPosition(position)

		if self.backtest is not None:
			self.backtest.current_index += 1
			if self.backtest.current_index >= (len(self.backtest.trade_data)-1):
				self.closePosition(trade_time, last_stock_value.close_value)
				self.stop()

	def openPosition(self, position: Position.Position):
		self.openedPosition = position

		self.budget -= position.open_value * position.amount

		print("""Position open: 
		{pos}

		Budget: {budget}""".format(pos=str(position), budget=self.budget))

	def closePosition(self, close_time: datetime.datetime, value: float):
		self.openedPosition.close(close_time, value)
		self.closedPositions.append(self.openedPosition)

		self.budget += value * self.openedPosition.amount

		print("""Position open: 
		{pos}
		
		Budget: {budget}""".format(pos=str(self.openedPosition), budget=self.budget))

		self.openedPosition = None

	def receiveTradeData(self) -> typing.List[StockValue.StockValue]:
		if self.backtest is not None:
			return StockValue.get_values_from_list(
				self.backtest.trade_data,
				self.backtest.trade_data[0].time_start,
				self.backtest.trade_data[self.backtest.current_index].time_end
			)
		else:
			trade_data = []
			return trade_data

	def start(self, manual_update: bool = False):
		self.tradeInProgress = True

		if not manual_update:
			while self.tradeInProgress:
				self.update()
				if self.backtest is not None:
					time.sleep(0.1)

	def stop(self):
		self.tradeInProgress = False

		print("Trading stopped: {budget}".format(budget=self.budget))

	def enableBacktestMode(self, test_trade_data: typing.List[StockValue.StockValue]):
		self.backtest = BackTestMode(test_trade_data)
