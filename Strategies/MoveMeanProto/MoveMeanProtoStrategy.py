import Strategies.Strategy as Strategy
import StockValue
import typing
import Position
from pandas import DataFrame, Series, isna


class StrategyMoveMeanProto(Strategy.Strategy):

	def shouldOpenPosition(self, trade_data: DataFrame) -> bool:
		if not super(StrategyMoveMeanProto, self).shouldOpenPosition(trade_data):
			return False
		else:

			if len(trade_data) <= 1:
				return False

			close_values_series = trade_data["Close"]
			moving_average = close_values_series.rolling(10)

			last_average_value = moving_average.mean().values[-1]

			prev_average_value = moving_average.mean().values[-2]

			if isna(last_average_value) or isna(prev_average_value):
				return False

			if last_average_value > prev_average_value:
				return False

			last_stock_value = trade_data[-1]

			if last_stock_value.close_value < last_average_value - (last_stock_value.close_value / 100 * 0.1):
				return True
			else:
				return False

	def shouldClosePosition(self, trade_data: DataFrame, position: Position.Position) -> bool:
		if super(StrategyMoveMeanProto, self).shouldClosePosition(trade_data, position):
			return True

		close_values_series = trade_data["Close"]
		moving_average = close_values_series.rolling(10)
		moving_average_small = close_values_series.rolling(4)

		last_average_value = moving_average.mean().values[-1]
		last_small_average_value = moving_average_small.mean().values[-1]
		prev_small_average_value = moving_average_small.mean().values[-2]

		last_value = trade_data[-1]

		if last_value.close_value > last_average_value and last_small_average_value < prev_small_average_value:
			return True
