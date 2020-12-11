import pandas
import time
import StocksReciever

while True:
	print(StocksReciever.getCurrentValue("AAPL"))
	time.sleep(1)
