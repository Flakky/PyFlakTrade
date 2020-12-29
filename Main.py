import StocksReciever
import StockValue
import datetime
import TradeSystem
import Trader
import Strategies.MoveMeanProto.MoveMeanProtoStrategy as MoveMeanProtoStrategy
import Strategies.Strategy as Strategy
import TraderPlotting
import matplotlib.pyplot # import it so PyDroid start programm in graphical mode

#while True:
#	print(StocksReciever.getCurrentValue("AAPL"))
#	time.sleep(1)

TradeSystem.init()

data = StocksReciever.receiveStocks("AAL")

TradeSystem.addTrader(MoveMeanProtoStrategy.StrategyMoveMeanProto)

TradeSystem.traders[0].enableBacktestMode(data)
TradeSystem.traders[0].start(False)

#TraderPlotting.add_trader(trader)
#TraderPlotting.start_trading_plotting(True)

