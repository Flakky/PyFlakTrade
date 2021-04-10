import Position
import StockValue
import typing
import matplotlib.axes
import datetime


class StrategyPlotter:
	pass


class Strategy:
	plotter: StrategyPlotter.__class__ = StrategyPlotter
	min_open_time: datetime.time = datetime.time(hour=8, minute=0)
	max_open_time: datetime.time = datetime.time(hour=23, minute=58)
	max_close_time: datetime.time = datetime.time(hour=23, minute=59)
	position_time_limit: int = 60  # in minutes

	def __init__(self, **kwargs):
		self.min_open_time = kwargs.get("min_open_time", self.min_open_time)
		self.max_open_time = kwargs.get("max_open_time", self.max_open_time)
		self.max_close_time = kwargs.get("max_close_time", self.max_close_time)
		self.position_time_limit = kwargs.get("position_time_limit", self.position_time_limit)

	#TODO: return suggested position
	def shouldOpenPosition(self, trade_data) -> bool:
		last_value = trade_data[-1]

		if last_value.time_end.time() > self.max_open_time or last_value.time_end.time() < self.min_open_time:
			return False

		return True
		
	#TODO: return sell position
	def shouldClosePosition(self, trade_data, position: Position.Position) -> bool:
		if position is not None:
			last_value = trade_data[-1]

			if last_value.time_end.time() >= self.max_close_time:
				return True

			position_minutes_delta = (last_value.time_end - position.open_time).total_seconds() / 60

			if position_minutes_delta >= self.position_time_limit:
				return True

			if last_value.close_value <= position.stop_loss or last_value.close_value >= position.take_profit:
				return True
			else:
				return False
		else:
			return False


class StrategyPlotter:

	@classmethod
	def plot(cls, ax: matplotlib.axes.Axes, strategy: Strategy, trade_data):
		return []
	
