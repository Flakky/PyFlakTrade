import time
import StocksReciever
import Position
import Strategies.Strategy as Strategy
import datetime
import StockValue
import typing
from Observer import Observer
from TradeProviders.TradeProvider import TradeProvider
from threading import Thread
from QuoteProvider import QuoteProvider

class Trader:
	strategy: Strategy.Strategy = None
	posMaxValue: float = 0.0
	allowed_stocks: typing.List[str] = []
	openedPosition: Position.Position = None
	closedPositions: typing.List[Position.Position] = []
	tradeInProgress: bool = False
	on_position_opened: Observer = Observer()
	on_position_closed: Observer = Observer()
	trade_provider: TradeProvider = None
	quote_provider: QuoteProvider = None

	def __init__(self, 
				strategy: Strategy.Strategy, 
				trade_provider: TradeProvider, 
				quote_provider: QuoteProvider,
				position_max_value: float,
				allowed_stocks: typing.List[str]):
		self.strategy = strategy
		self.trade_provider = trade_provider
		self.quote_provider = quote_provider

		self.posMaxValue = position_max_value
		self.allowed_stocks = allowed_stocks

	def update(self):
		if not self.tradeInProgress or self.strategy is None:
			self.stop()
			return
			
		quote_request = self.strategy.get_quotes_requst()

		trade_data = self.quote_provider.read_quotes(quote_request)

		if len(trade_data.index) == 0:
			self.stop()
			return

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
					self.trade_provider.read_budget() // open_value,
					stop_loss=open_value - ((open_value / 100.0) * 0.5)
				)
				self.openPosition(position)

	def openPosition(self, position: Position.Position):
		self.openedPosition = position
		
		self.trade_provider.open_position(position.ticker, position.amount)

		self.on_position_opened.exec(self, position)

	def closePosition(self, close_time: datetime.datetime, value: float):
		self.trade_provider.close_position(
			self.openedPosition.ticker,
			self.openedPosition.amount
		)
		
		self.openedPosition.close(close_time, value)
		self.closedPositions.append(self.openedPosition)

		self.on_position_closed.exec(self, self.openedPosition)

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

	def start_async(self):
		th = Thread(target=self.start)
		th.start()

	async def start_async_internal(self):
		self.start(False)

	def stop(self):
		self.tradeInProgress = False

		print("Trading stopped: {budget}".format(budget=self.budget))

	def enableBacktestMode(self, test_trade_data: typing.List[StockValue.StockValue]):
		self.backtest = BackTestMode(test_trade_data)

		self.closedPositions.clear()
