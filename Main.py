import TradeSystem
from Trader import Trader
from TradeProviders.TradeProvider_Test import TradeProviderTest
from QuoteProviders.QuoteProvider_YFinance import QuoteProviderYFinance
from Strategies.MoveMeanProto.MoveMeanProtoStrategy import StrategyMoveMeanProto
from Strategies.Strategy import Backtest
# import matplotlib.pyplot  # import it so PyDroid start programm in graphical mode

TradeSystem.init()

backtest = Backtest()
strategy = StrategyMoveMeanProto(
	backtest=backtest
)
trade_provider = TradeProviderTest()
quote_provider = QuoteProviderYFinance()

trader = Trader(
	strategy,
	trade_provider,
	quote_provider,
	999999.0,
	["AAPL"]
)

TradeSystem.add_trader(trader)

trader.start()