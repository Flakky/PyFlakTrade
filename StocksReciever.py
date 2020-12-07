import pandas
from alpha_vantage.timeseries import TimeSeries
import yfinance
import datetime
import StockValue


def getCurrentValue(symbol: str) -> StockValue:
    stock = yfinance.Ticker(symbol)

    print(stock.info)
    value = (stock.info["bid"] + stock.info["ask"]) / 2
    stock_value = StockValue.StockValue(value, datetime.datetime.now())

    return stock_value


def receiveStocks(symbol: str, interval=5):
    ts = TimeSeries(key='1X1VXIAYUFBBM00J', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=str(interval)+"min", outputsize='compact')

    data.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    }, inplace=True)

    return data
