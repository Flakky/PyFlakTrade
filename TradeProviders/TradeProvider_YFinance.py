from QuoteProvider import QuoteProvider
from QuoteRequest import QuoteRequest
from datetime import datetime
import yfinance
from pandas import DataFrame

class QuoteProviderYFinance(QuoteProvider):
	
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		out_stocks: DataFrame = DataFrame()

		today = datetime.now()

		for week in range(int(30/7)):

			start = today - datetime.timedelta(days=min((week+1) * 7, 30))
			end = today - datetime.timedelta(days=(week * 7))

			print("Downloading stock from {start} to {end}".format(start=str(start.date()), end=str(end.date())))

			data = yfinance.download(
				request.ticker,
				start=str(start.date()),
				end=str(end.date()),
				interval=request.period
			)

			out_stocks.append(data)

		return out_stocks
