import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
import Trader
import Position
import StockValue
import datetime

fig, ax = plt.subplots()
traders = []
update_traders = True

def animate(i):
	plt.cla()

	for trader in traders:

		if update_traders:
			trader.update()

		# max(trader.backtest.current_index-30,0)

		trade_values = trader.receiveTradeData()
		last_value = trade_values[-1]

		draw_start_time = datetime.datetime(last_value.time_end.year, last_value.time_end.month, last_value.time_end.day)
		draw_end_time = last_value.time_end

		trade_values = StockValue.get_values_from_list(trade_values, draw_start_time, draw_end_time)

		closed_positions = Position.get_positions_from_list(trader.closedPositions, draw_start_time, draw_end_time)

		plot_trade_data(trade_values)
		plot_positions(closed_positions)
		plot_positions([trader.openedPosition])
		
		if trader.strategy.plotter is not None:
			trader.strategy.plotter.plot(ax, trader.strategy, trade_values)


def plot_trade_data(trade_values):
	x = StockValue.get_times_array_from_stocks(trade_values)
	y = StockValue.get_value_array_from_stocks(trade_values)

	ax.plot(x, y)


def plot_positions(positions):
	pos_x = []
	pos_y = []
	colors = []
	texts = []
	texts_pos = []

	for position in positions:
		if position is None:
			continue

		pos_x.append(position.open_time)
		pos_y.append(position.open_value)

		seed = int(position.open_time.timestamp())
		numpy.random.seed(seed)
		color = (numpy.random.random(), numpy.random.random(), numpy.random.random())
		colors.append(color)
		
		if position.closed:
			pos_x.append(position.close_time)
			pos_y.append(position.close_value)

			colors.append(color)

			ax.annotate(
				round(position.close_value - position.open_value, 3),
				(position.close_time, position.close_value),
			)

	ax.scatter(pos_x, pos_y, c=colors)


def add_trader(trader: Trader.Trader):
	traders.append(trader)


def start_trading_plotting(should_update_traders: bool):
	global update_traders
	update_traders = should_update_traders

	ani = animation.FuncAnimation(fig, animate, interval=30)
	plt.show()
