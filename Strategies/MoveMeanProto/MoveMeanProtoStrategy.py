import Strategies.Strategy as Strategy
import StockValue
import typing
import Position
import pandas
import matplotlib.axes


class MoveMeanProtoPlotter(Strategy.StrategyPlotter):

	@classmethod
	def plot(cls, ax: matplotlib.axes.Axes, strategy: Strategy, trade_data: typing.List[StockValue.StockValue]):
		plot_elems = []

		close_values_series = pandas.Series(StockValue.get_array_from_stocks(trade_data, "close_value"))
		moving_average = close_values_series.rolling(10)
		moving_average_small = close_values_series.rolling(4)

		x = StockValue.get_times_array_from_stocks(trade_data, True)

		plot_elems += ax.plot(x, moving_average.mean().values)
		plot_elems += ax.plot(x, moving_average_small.mean().values)

		return plot_elems


class StrategyMoveMeanProto(Strategy.Strategy):

	plotter = MoveMeanProtoPlotter

	def shouldOpenPosition(self, trade_data) -> bool:
		if not super(StrategyMoveMeanProto, self).shouldOpenPosition(trade_data):
			return False
		else:

			if len(trade_data) <= 1:
				return False

			close_values_series = pandas.Series(trade_data, "close_value")
			moving_average = close_values_series.rolling(10)

			last_average_value = moving_average.mean().values[-1]

			prev_average_value = moving_average.mean().values[-2]

			if pandas.isna(last_average_value) or pandas.isna(prev_average_value):
				return False

			if last_average_value > prev_average_value:
				return False

			last_stock_value = trade_data[-1]

			if last_stock_value.close_value < last_average_value - (last_stock_value.close_value / 100 * 0.1):
				return True
			else:
				return False

	def shouldClosePosition(self, trade_data, position: Position.Position) -> bool:
		if super(StrategyMoveMeanProto, self).shouldClosePosition(trade_data, position):
			return True

		close_values_series = pandas.Series(trade_data, "close_value")
		moving_average = close_values_series.rolling(10)
		moving_average_small = close_values_series.rolling(4)

		last_average_value = moving_average.mean().values[-1]
		last_small_average_value = moving_average_small.mean().values[-1]
		prev_small_average_value = moving_average_small.mean().values[-2]

		last_value = trade_data[-1]

		if last_value.close_value > last_average_value and last_small_average_value < prev_small_average_value:
			return True
