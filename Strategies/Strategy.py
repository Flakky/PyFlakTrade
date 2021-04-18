import Position
import StockValue
import typing
from datetime import datetime, timedelta, time
from QuoteRequest import QuoteRequest
from pandas import DataFrame

	
class Backtest:
	start: datetime = datetime.now() - timedelta(days=7)
	end: datetime = datetime.now()
	current_datetime: datetime = datetime.now() - timedelta(days=7)


class Strategy:
	# move min/max times to specific strategies
	min_open_time: time = time(hour=8, minute=0)
	max_open_time: time = time(hour=23, minute=58)
	max_close_time: time = time(hour=23, minute=59)
	position_time_limit: int = 60  # in minutes
	update_period: int = 5 # in seconds
	backtest: Backtest = None

	def __init__(self, **kwargs):
		self.min_open_time = kwargs.get("min_open_time", self.min_open_time)
		self.max_open_time = kwargs.get("max_open_time", self.max_open_time)
		self.max_close_time = kwargs.get("max_close_time", self.max_close_time)
		self.position_time_limit = kwargs.get("position_time_limit", self.position_time_limit)
		self.update_period = kwargs.get("update_period", self.update_period)
		self.backtest = kwargs.get("backtest", None)

	#TODO: return suggested position
	def shouldOpenPosition(self, trade_data: DataFrame) -> bool:
		last_data = trade_data.iloc[-1]
		last_time = last_data.name

		if last_time.time() > self.max_open_time or last_time.time() < self.min_open_time:
			return False

		return True
		
	#TODO: return sell position
	def shouldClosePosition(self, trade_data: DataFrame, position: Position.Position) -> bool:
		if position is not None:
			last_value = trade_data.iloc[-1]

			if last_value.index.time() >= self.max_close_time:
				return True

			position_minutes_delta = (last_value.index.time() - position.open_time).total_seconds() / 60

			if position_minutes_delta >= self.position_time_limit:
				return True

			if last_value.close_value <= position.stop_loss or last_value.close_value >= position.take_profit:
				return True
			else:
				return False
		else:
			return False
			
	def get_quotes_request(self) -> QuoteRequest:
		
		request = QuoteRequest(
			"",
			self.backtest.current_datetime - timedelta(days=7),
			self.backtest.current_datetime,
			self.update_period
		)
				
		if self.backtest is not None:				
			self.backtest.current_datetime += timedelta(seconds=self.update_period)
				
		return request
