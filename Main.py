import pandas
import time
import StocksReciever
import StockValue
import datetime
import Trader
import Strategy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#while True:
#	print(StocksReciever.getCurrentValue("AAPL"))
#	time.sleep(1)

data = StocksReciever.receiveStocks("AAPL")

period_data = StocksReciever.StockValue.get_values_from_list(
	data,
	datetime.datetime(2020, 12, 1),
	datetime.datetime(2020, 12, 5)
)

trader = Trader.Trader(Strategy.Strategy(), 1000.0, 150.0, ["AAPL"])

trader.enableBacktestMode(period_data)

trader.start(True)

def anim(i):
	trade_values = StockValue.get_values_from_list(
		trader.backtest.trade_data,
		trader.backtest.current_time-datetime.timedelta(hours=1),
		trader.backtest.current_time
	)

	x = StockValue.get_times_array_from_stocks(trade_values)
	y = StockValue.get_value_array_from_stocks(trade_values)
	plt.cla()

	plt.plot(x, y)

	trader.update()


ani = animation.FuncAnimation(plt.gcf(), anim, interval=30)
plt.show()
