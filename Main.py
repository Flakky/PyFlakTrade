import StocksReciever
import StockValue
import datetime
import Trader
import Strategy
import TraderPlotting
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

TraderPlotting.add_trader(trader)
TraderPlotting.start_trading_plotting(True)

# fig, ax = plt.subplots()
#
#
# def anim(i):
# 	print("test")
#
# 	x = [0,1,2,3,4]
# 	y = [1,2,5,7,2]
#
# #	plt.cla()
#
# 	ax.plot(x, y)
#
#
# print("Start anim")
#
#
# ani = animation.FuncAnimation(fig, anim, interval=300)
# plt.show()
