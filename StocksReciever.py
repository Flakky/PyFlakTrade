import pandas
from alpha_vantage.timeseries import TimeSeries
import yfinance
import datetime
import StockValue
import typing

stocks_cache = {}


def getCurrentValue(symbol: str) -> StockValue:
	stock = yfinance.Ticker(symbol)

	has_symbol_array = symbol in stocks_cache
	
	if has_symbol_array:
		last_value = stocks_cache[symbol][-1]
	else:
		last_value = None
		print("no symbol in cache")

	value = (stock.info["bid"] + stock.info["ask"]) / 2

	stock_value = StockValue.StockValue(
		symbol,
		value,
		datetime.datetime.now(),
		open_value=last_value.close_value if has_symbol_array else value,
		time_start=last_value.time_end if has_symbol_array else datetime.datetime.now()
	)

	insert_to_cache(stock_value)

	return stock_value


def receiveStocks(symbol: str) -> typing.List[StockValue.StockValue]:
	data = yfinance.download(
		symbol,
		start="2020-12-01",
		end="2020-12-07",
		interval="1m"
	)
	
	stocks_array = []
	
	for date, row in data.iterrows():

		stock_value = StockValue.StockValue(
			symbol,
			row["Close"],
			datetime.datetime.fromtimestamp(date.timestamp()),
			open_value=row["Open"],
			time_start=datetime.datetime.fromtimestamp(date.timestamp()-60),
			volume=row["Volume"],
			low_value=row["Low"],
			high_value=row["High"]
		)
		stocks_array.append(stock_value)

	return stocks_array


def insert_to_cache(stock_value: StockValue.StockValue) -> bool:
	if stock_value is None:
		return False

	symbol = stock_value.symbol

	if symbol == "":
		return False

	if symbol in stocks_cache:
		last_value = stocks_cache[symbol][-1]

		if len(stocks_cache) <= 0:
			return False

		if stock_value.close_value != last_value.close_value:
			stocks_cache[symbol].append(stock_value)
			return True
		else:
			return False
	else:
		stocks_cache[symbol] = [stock_value]
		return True

