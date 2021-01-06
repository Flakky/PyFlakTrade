import datetime
import typing
import pandas


class StockValue:
	symbol: str = ""
	close_value: int = 0
	open_value: int = 0
	high_value: int = 0
	low_value: int = 0
	volume: int = 0
	time_start: datetime.datetime = 0
	time_end: datetime.datetime = 0

	def __init__(self, symbol: str, last_value: int, time_end, **kwargs):
		self.symbol = symbol
		self.close_value = last_value
		self.time_end = time_end
		self.low_value = kwargs.get("low_value", last_value)
		self.high_value = kwargs.get("high_value", last_value)
		self.time_start = kwargs.get("time_start", time_end)
		self.volume = kwargs.get("volume", 0)
		self.open_value = kwargs.get("open_value", last_value)

	def __str__(self):
		return """StockValue for '{symbol}':
	-Open: {open} - {open_time}
	-Close: {color} {close} \033[0m - {close_time}
	-High: {high}
	-Low: {low}
	-Volume: {vol}""".format(
			symbol=self.symbol,
			close=round(self.close_value, 3),
			open=round(self.open_value, 3),
			high=round(self.high_value, 3),
			low=round(self.low_value, 3),
			vol=self.volume,
			close_time=self.time_end,
			open_time=self.time_start,
			color="\033[92m" if self.close_value > self.open_value
			else ("" if self.close_value == self.open_value else "\033[91m")
		)


def get_values_from_list(values_list: typing.List[StockValue], start: datetime.datetime, end: datetime.datetime) -> \
	typing.List[StockValue]:
	out_list = []
	for i in range(len(values_list)):
		value = values_list[i]
#		next_value = values_list[i+1] if i+1 < len(values_list) else None

		if value.time_start >= start and value.time_end <= end:
			out_list.append(value)

	return out_list


def get_array_from_stocks(values_list: typing.List[StockValue], values_type: str):
	out = []

	for value in values_list:
		if values_type == "close_value":
			out.append(value.close_value)
		elif values_type == "open_value":
			out.append(value.open_value)
		elif values_type == "high_value":
			out.append(value.high_value)
		elif values_type == "low_value":
			out.append(value.low_value)
		elif values_type == "volume":
			out.append(value.volume)
		elif values_type == "time_start":
			out.append(value.time_start)
		elif values_type == "time_end":
			out.append(value.time_start)
		else:
			# TODO: asset
			out.append(None)

	return out


def get_value_array_from_stocks(values_list: typing.List[StockValue], close: bool = True) -> typing.List[float]:
	out_list = []
	for value in values_list:
		out_list.append(value.close_value if close else value.open_value)

	return out_list


def get_times_array_from_stocks(values_list: typing.List[StockValue], close: bool = True) -> typing.List[
	datetime.datetime]:
	out_list = []
	for value in values_list:
		out_list.append(value.time_end if close else value.time_start)

	return out_list


def convert_dataframe_to_list(stock_data, symbol: str) -> typing.List[StockValue]:
	stocks_array = []

	for date, row in stock_data.iterrows():
		stock_value = StockValue(
			symbol,
			row["Close"],
			datetime.datetime.fromtimestamp(date.timestamp()),
			open_value=row["Open"],
			time_start=datetime.datetime.fromtimestamp(date.timestamp() - 60),
			volume=row["Volume"],
			low_value=row["Low"],
			high_value=row["High"]
		)
		stocks_array.append(stock_value)

	return stocks_array


def convert_list_to_dataframe(stock_data,
							  value_types: tuple = ("close_value", "open_value", "high_value", "low_value", "volume")):
	datetimes = get_times_array_from_stocks(stock_data)

	columns_map = {}

	for val in value_types:
		columns_map[val] = get_array_from_stocks(stock_data, val)

	stock_dataframe = pandas.DataFrame(columns_map, index=datetimes)

	return stock_dataframe
