import datetime


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
	-Close: {color}{close}\033[0m - {close_time}
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
			else ("" if self.close_value == self.open_value else "\031[92m")
		)
