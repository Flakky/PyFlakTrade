import TradeSystem
from Trader import Trader
from TradeProviders.TradeProvider_Test import TradeProviderTest
from QuoteProviders.QuoteProvider_Generator import QuoteProviderGenerator
from QuoteProviders.QuoteProvider_YFinance import QuoteProviderYFinance
from Strategies.MoveMeanProto.MoveMeanProtoStrategy import StrategyMoveMeanProto
from Strategies.Strategy import Backtest
from datetime import datetime, timedelta


TradeSystem.init()

tickers = ["AAPL", "AMD", "M"]

backtest = Backtest()
strategy = StrategyMoveMeanProto(
	backtest=backtest,
	update_period=timedelta(minutes=1)
)
trade_provider = TradeProviderTest(1000)

# quote_provider = QuoteProviderGenerator(
# 	datetime.now() - timedelta(days=20),
# 	datetime.now(),
# 	timedelta(minutes=1),
# 	tickers
# )

quote_provider = QuoteProviderYFinance(tickers)

trader = Trader(
	strategy,
	trade_provider,
	quote_provider,
	999999.0,
	tickers
)

TradeSystem.add_trader(trader)

trader.start()
