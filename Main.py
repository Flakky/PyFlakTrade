import StocksReciever
import StockValue
import datetime
import Trader
import Strategies.MoveMeanProto.MoveMeanProtoStrategy as MoveMeanProtoStrategy
import Strategies.Strategy as Strategy
import TraderPlotting
import matplotlib.pyplot # import it so PyDroid start programm in graphical mode

#while True:
#	print(StocksReciever.getCurrentValue("AAPL"))
#	time.sleep(1)


data = StocksReciever.receiveStocks("M")

period_data = StocksReciever.StockValue.get_values_from_list(
	data,
	datetime.datetime(2020, 12, 1),
	datetime.datetime(2020, 12, 5)
)

dataframe = StockValue.convert_list_to_dataframe(period_data)
print(dataframe)

strategy = MoveMeanProtoStrategy.StrategyMoveMeanProto()

trader = Trader.Trader(strategy, 1000.0, 150.0, ["AAPL"])

trader.enableBacktestMode(period_data)

trader.start(True)

TraderPlotting.add_trader(trader)
TraderPlotting.start_trading_plotting(True)

