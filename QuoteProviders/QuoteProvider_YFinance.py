from QuoteProviders.QuoteProvider import QuoteProvider
from QuoteRequest import QuoteRequest
from datetime import datetime, timedelta
import yfinance
from pandas import DataFrame

class QuoteProviderYFinance(QuoteProvider):
	
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		out_stocks: DataFrame = DataFrame()

		today = datetime.now()

		for week in range(int(30/7)):

			start = today - timedelta(days=min((week+1) * 7, 30))
			end = today - timedelta(days=(week * 7))
			
			interval = ""
			if request.period == 1:
				interval = "1s"
			if request.period == 5:
				interval = "5s"
			if request.period == 60:
				interval = "1m"

			print("Downloading stock from {start} to {end} with interval {interval}".format(
				start=str(start.date()), 
				end=str(end.date()), 
				interval=interval)
			)
				
			data = yfinance.download(
				request.ticker,
				start=str(start.date()),
				end=str(end.date()),
				interval=interval
			)

			out_stocks.append(data)

		return out_stocks
