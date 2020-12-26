import Strategies.Strategy as Strategy
import StockValue
import typing
import Position
import pandas
import matplotlib.axes


class MoveMeanProtoPlotter(Strategy.StrategyPlotter):
	pass


class StrategyMoveMeanProto(Strategy.Strategy):
	pass
	
	plotter: Strategy.StrategyPlotter.__class__ = MoveMeanProtoPlotter

	def __init__(self):
		super(StrategyMoveMeanProto, self).__init__()

	def shouldOpenPosition(self, trade_data: typing.List[StockValue.StockValue]) -> bool:
		if not super(StrategyMoveMeanProto, self).shouldOpenPosition(trade_data):
			return False
		else:
			close_values_series = pandas.Series(StockValue.get_array_from_stocks(trade_data, "close_value"))
			moving_average = close_values_series.rolling(10)

			last_average_value = moving_average.mean().values[-1]

			if pandas.isna(last_average_value):
				return False

			last_stock_value = trade_data[-1]

			if last_stock_value.close_value < last_average_value:
				return True
			else:
				return False

	def shouldClosePosition(self, trade_data: typing.List[StockValue.StockValue], position: Position.Position) -> bool:
		if super(StrategyMoveMeanProto, self).shouldClosePosition(trade_data, position):
			return True


class MoveMeanProtoPlotter(Strategy.StrategyPlotter):
	
	@classmethod
	def plot(cls, ax: matplotlib.axes.Axes, strategy: Strategy, trade_data: typing.List[StockValue.StockValue]):
		print("test")
		close_values_series = pandas.Series(StockValue.get_array_from_stocks(trade_data, "close_value"))
		moving_average = close_values_series.rolling(10)
		
		x = StockValue.get_times_array_from_stocks(trade_data, True)
		
		print(x)
		
		ax.plot(x, moving_average)
		return