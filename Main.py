import TradeSystem
from Trader import Trader
from TradeProviders.TradeProvider_Test import TradeProviderTest
from QuoteProviders.QuoteProvider_Generator import QuoteProviderGenerator
from Strategies.MoveMeanProto.MoveMeanProtoStrategy import StrategyMoveMeanProto
from Strategies.Strategy import Backtest
from datetime import  datetime, timedelta

TradeSystem.init()

tickers = ["AAPL", "AMD", "M"]

backtest = Backtest()
strategy = StrategyMoveMeanProto(
	backtest=backtest
)
trade_provider = TradeProviderTest(1000)
quote_provider = QuoteProviderGenerator(
	datetime.now() - timedelta(days=20),
	datetime.now(),
	timedelta(seconds=5),
	tickers
)

trader = Trader(
	strategy,
	trade_provider,
	quote_provider,
	999999.0,
	tickers
)

TradeSystem.add_trader(trader)

trader.start()