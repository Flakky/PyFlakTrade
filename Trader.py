import time
import StocksReciever
import Position
import Strategies.Strategy as Strategy
import datetime
import StockValue
import typing
from Observer import Observer
from QuoteRequest import QuoteRequest
from TradeProviders.TradeProvider import TradeProvider
from threading import Thread
from QuoteProviders.QuoteProvider import QuoteProvider

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

	def update_ticker(self, ticker: str):
		if not self.tradeInProgress or self.strategy is None:
			self.stop()
			return
			
		quote_request = self.strategy.get_quotes_request()
		quote_request.ticker = ticker

		trade_data = self.quote_provider.read_quotes(quote_request)

		if len(trade_data.index) == 0:
			print("No more trade data")
			self.stop()
			return

		last_stock_value = trade_data.iloc[-1]
		trade_time = last_stock_value.name
		print(last_stock_value)

		if self.openedPosition is not None:
			if self.strategy.shouldClosePosition(trade_data, self.openedPosition):
				self.closePosition(trade_time, last_stock_value["Close"])
		else:
			if self.strategy.shouldOpenPosition(trade_data):
				open_value = last_stock_value["Close"]
				position = Position.Position(
					trade_time,
					open_value,
					self.trade_provider.read_budget() // open_value,
					stop_loss=open_value - ((open_value / 100.0) * 0.5)
				)
				self.openPosition(position)

	def openPosition(self, position: Position.Position):
		self.openedPosition = position
		
		self.trade_provider.open_position(position)

		self.on_position_opened.exec(self, position)

	def closePosition(self, close_time: datetime.datetime, value: float):
		self.trade_provider.close_position(self.openedPosition)
		
		self.openedPosition.close(close_time, value)
		self.closedPositions.append(self.openedPosition)

		self.on_position_closed.exec(self, self.openedPosition)

		self.openedPosition = None
		
	def update(self):
		for ticker in self.allowed_stocks:
					self.update_ticker(ticker)

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

		print("Trading stopped")

