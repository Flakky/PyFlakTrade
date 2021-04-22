from QuoteProviders.QuoteProvider import QuoteProvider
from QuoteRequest import QuoteRequest
from datetime import datetime, timedelta
import yfinance
from pandas import DataFrame
from typing import Dict, List

class QuoteProviderYFinance(QuoteProvider):
	quotes: Dict[str, DataFrame] = {}
	
	def __init__(self, tickers: List[str]):
		today = datetime.now()
		
		for ticker in tickers:
			
			ticker_stocks: DataFrame = None
	
			for week in range(int(30/7)):
	
				start = today - timedelta(days=min((week+1) * 7, 30))
				end = today - timedelta(days=(week * 7))
	
				print("Downloading {ticker} stock from {start} to {end} with interval {interval}".format(
					start=str(start.date()), 
					end=str(end.date()), 
					interval="1m",
					ticker=ticker
				))
					
				stocks_data = yfinance.download(
					ticker,
					start=str(start.date()),
					end=str(end.date()),
					interval="1m"
				)
				
				if ticker_stocks is None:
					ticker_stocks = stocks_data
				else:
					ticker_stocks.append(stocks_data)
					
			ticker_stocks = ticker_stocks.tz_convert(None)
					
			print(ticker_stocks.index)
			print(datetime(year=2021, month=4, day=3, hour=5))
			
			self.quotes[ticker] = stocks_data
		
	
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		data = self.quotes[request.ticker]

		mask = (data.index > request.start) & (data.index <= request.end)
		
		out_stocks = data.loc[mask]

		return out_stocks
