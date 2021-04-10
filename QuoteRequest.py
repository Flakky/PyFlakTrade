class QuoteRequest:
	start = None
	end = None
	period = None
	ticker: str = ""
	
	def __init__(self, ticker, start, end, period):
		self.start = start
		self.end = end
		self.ticker = ticker
		self.period = period