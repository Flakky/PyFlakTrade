import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Trader
import StockValue
import datetime

fig, ax = plt.subplots()
traders = []
update_traders = True

def animate(i):
	print(i)
	for trader in traders:
		
		if update_traders:
			trader.update()
	
		trade_values = trader.receiveTradeData()[max(trader.backtest.current_index-30, 0):trader.backtest.current_index]
		plot_trade_data(trade_values)
		plot_positions(trader.closedPositions)
		plot_positions([trader.openedPosition])
	
#	plt.cla()
	
def plot_trade_data(trade_values):
	x = StockValue.get_times_array_from_stocks(trade_values)
	y = StockValue.get_value_array_from_stocks(trade_values)

	ax.plot(x, y)
	
def plot_positions(positions):
	pos_x = []
	pos_y = []
	
	for position in positions:
		pos_x.append(position.open_time)
		pos_y.append(position.open_value)
		
		if position.closed:
			pos_x.append(position.close_time)
			pos_y.append(position.close_value)
		else:
			pos_x.append(position.open_time+datetime.timedelta(hour=1))
			pos_y.append(position.open_value)

	ax.plot(pos_x, pos_y)

def add_trader(trader: Trader.Trader):
	traders.append(trader)

def start_trading_plotting(should_update_traders: bool):
	update_traders = should_update_traders
	
	animation.FuncAnimation(fig, animate, interval=30)
	plt.show()
	
print("Start anim")

	
animation.FuncAnimation(fig, animate, interval=300)
plt.show()