import Position
import Strategies.Strategy as Strategy
import datetime
from typing import List, Dict
from Observer import Observer
from TradeProviders.TradeProvider import TradeProvider
from threading import Thread
from QuoteProviders.QuoteProvider import QuoteProvider


class Trader:
	strategy: Strategy.Strategy = None
	posMaxValue: float = 0.0
	allowed_stocks: List[str] = []
	openedPositions: Dict[str, Position.Position] = {}
	closedPositions: List[Position.Position] = [] #TODO DataFrame
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
			allowed_stocks: List[str]):
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

		print("""{start} - {end} - {ticker}""".format(ticker=ticker, start=quote_request.start, end=quote_request.end), end="\r")

		trade_data = self.quote_provider.read_quotes(quote_request)

		if len(trade_data.index) == 0:
#			print("No trade data for ticker")
			return

		last_stock_value = trade_data.iloc[-1]
		trade_time = last_stock_value.name
		# print(last_stock_value)

		if self.openedPositions.get(ticker) is not None:
			if self.strategy.shouldClosePosition(trade_data, self.openedPositions[ticker]):
				self.close_position(ticker, trade_time, last_stock_value["Close"])
		else:
			if self.strategy.shouldOpenPosition(trade_data):
				open_value = last_stock_value["Close"]	
				amount = self.trade_provider.read_budget() // open_value

				if amount >= 1:
					position = Position.Position(
						ticker,
						trade_time,
						open_value,
						self.trade_provider.read_budget() // open_value,
						stop_loss=open_value - ((open_value / 100.0) * 0.5)
					)
					self.open_position(position)

	def open_position(self, position: Position.Position):
		self.openedPositions[position.ticker] = position

		self.trade_provider.open_position(position)

		self.on_position_opened.exec(self, position)

	def close_position(self, ticker: str, close_time: datetime.datetime, value: float):
		position = self.openedPositions.pop(ticker)

		position.close(close_time, value)

		self.trade_provider.close_position(position)

		self.closedPositions.append(position)

		self.on_position_closed.exec(self, position)

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
