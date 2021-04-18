from QuoteProviders.QuoteProvider import QuoteProvider
from QuoteRequest import QuoteRequest
from datetime import datetime, timedelta
from pandas import DataFrame, date_range
import numpy
from random import  uniform


class QuoteProviderGenerator(QuoteProvider):
	quotes: DataFrame = DataFrame()
	
	def __init__(self, start: datetime, end: datetime, period: timedelta):
		self.quotes = DataFrame({"Close", "Open", "Volume", "Low", "High"})
		
		dates = []
		date = start
		while date <= end:
			if date.isoweekday() <= 5 and date.time().hour >= 9 and date.time().hour < 17:
				dates.append(date)
			date += period			
		
		close_values = []
		open_values = []
		volume_values = []
		low_values = []
		high_values = []
		for i in range(0, len(dates)):
			if i == 0:
				base_value = uniform(100.0, 200.0)
				close_values.append(base_value)
				open_values.append(base_value)
				low_values.append(base_value)
				high_values.append(base_value)
				volume_values.append(100)
			else:
				prev_value = close_values[-1]
				new_value = prev_value + uniform(-0.05, 0.05)
				close_values.append(new_value)
				open_values.append(prev_value)
				low_values.append(new_value if prev_value > new_value else prev_value)
				high_values.append(new_value if prev_value < new_value else prev_value)
				volume_values.append(100)
		
		self.quotes = DataFrame({
			'Close': close_values,
			'Open': open_values,
			'Volume': volume_values,
			'Low': low_values,
			'High': high_values
		}, index=dates)
		
		print(self.quotes)
		
	
	def read_quotes(self, request: QuoteRequest) -> DataFrame:
		mask = (self.quotes.index > request.start) & (self.quotes.index <= request.end)
		
		out_stocks = self.quotes.loc[mask]

		return out_stocks
