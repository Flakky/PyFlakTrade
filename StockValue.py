import datetime


class StockValue:
	symbol = ""
	close_value = 0
	open_value = 0
	high_value = 0
	low_value = 0
	volume = 0
	time_start = 0
	time_end = 0

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
			close=self.close_value,
			open=self.open_value,
			high=self.high_value,
			low=self.low_value,
			vol=self.volume,
			close_time=self.time_end,
			open_time=self.time_start,
			color="\033[92m" if self.close_value >= self.open_value else "\031[92m"
		)
