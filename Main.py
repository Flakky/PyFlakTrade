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

test_data = trader.receiveTradeData()
for val in test_data:
	print(val)

trader.start(True)

fig, ax = plt.subplots()

def anim(i):
	trader.update()
	
	trade_values = trader.receiveTradeData()[max(trader.backtest.current_index-30, 0):trader.backtest.current_index]
	pos_x = []
	pos_y = []
	
	if trader.openedPosition is not None:
		pos_x.append(trader.openedPosition.open_time)
		pos_y.append(trader.openedPosition.open_value)
		
		if trader.openedPosition.closed:
			pos_x.append(trader.openedPosition.close_time)
			pos_y.append(trader.openedPosition.close_value)
	
	ax.scatter(pos_x, pos_y)
	
	x = StockValue.get_times_array_from_stocks(trade_values)
	y = StockValue.get_value_array_from_stocks(trade_values)
	plt.cla()

	return ax.plot(x, y)

ani = animation.FuncAnimation(fig, anim, interval=30)
plt.show()
