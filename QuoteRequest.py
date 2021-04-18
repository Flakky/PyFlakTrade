from datetime import timedelta


class QuoteRequest:
	start = None
	end = None
	period: timedelta = timedelta(minutes=1)
	ticker: str = ""
	
	def __init__(self, ticker, start, end, period):
		self.start = start
		self.end = end
		self.ticker = ticker
		self.period = period

	def __str__(self):
		return """QuoteRequest for '{ticker}':
	-Start: {start}
	-End: {end}
	-Period: {period}""".format(
			ticker=self.ticker,
			start=str(self.start),
			end=str(self.end),
			period=str(self.period)
		)
