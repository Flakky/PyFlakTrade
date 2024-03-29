import pandas
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
	out_stocks = []

	today = datetime.datetime.now()

	for week in range(int(30/7)):

		start = today - datetime.timedelta(days=min((week+1) * 7, 30))
		end = today - datetime.timedelta(days=(week * 7))

		print("Downloading stock from {start} to {end}".format(start=str(start.date()), end=str(end.date())))

		data = yfinance.download(
			symbol,
			start=str(start.date()),
			end=str(end.date()),
			interval="1m"
		)
		out_stocks.extend(StockValue.convert_dataframe_to_list(data, symbol))

	return out_stocks


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
