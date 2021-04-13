from pandas import DataFrame

from QuoteRequest import QuoteRequest

class QuoteProvider:

#		Return DataFrame format:
#		Date | Close, Open, Volume, Low, High
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		return
		