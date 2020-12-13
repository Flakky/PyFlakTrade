import pandas
import time
import StocksReciever
import datetime

#while True:
#	print(StocksReciever.getCurrentValue("AAPL"))
#	time.sleep(1)

data = StocksReciever.receiveStocks("AAPL")

period_data = StocksReciever.StockValue.get_values_from_list(data, datetime.datetime(2020,12,3), datetime.datetime(2020,12,4))

for value in period_data:
	print(value)