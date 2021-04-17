from QuoteProviders.QuoteProvider import QuoteProvider
from QuoteRequest import QuoteRequest
from datetime import datetime, timedelta
from pandas import DataFrame


class QuoteProviderGenerator(QuoteProvider):
	quotes: DataFrame = DataFrame()
	
	def __init__(self, start: datetime, end: datetime):
		self.quotes = DataFrame({"Close", "Open", "Volume", "Low", "High"})
		
		
	
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		out_stocks: DataFrame = DataFrame()

		today = datetime.now()


		return out_stocks
