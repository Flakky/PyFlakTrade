import pandas
from alpha_vantage.timeseries import TimeSeries
import yfinance
import datetime
import StockValue

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

	if has_symbol_array:
		stocks_cache[symbol].append(stock_value)
	else:
		stocks_cache[symbol] = [stock_value]

	return stock_value


def receiveStocks(symbol: str, interval=5):
	ts = TimeSeries(key='1X1VXIAYUFBBM00J', output_format='pandas')
	data, meta_data = ts.get_intraday(symbol=symbol, interval=str(interval)+"min", outputsize='compact')

	data.rename(columns={
		'1. open': 'open',
		'2. high': 'high',
		'3. low': 'low',
		'4. close': 'close',
		'5. volume': 'volume'
	}, inplace=True)

	return data
