import pandas
from alpha_vantage.timeseries import TimeSeries
import yfinance


def getCurrentValue(symbol):
    stock = yfinance.Ticker(symbol)
    return (stock.info["bid"] + stock.info["ask"]) / 2


def receiveStocks(symbol, interval=5):
    ts = TimeSeries(key='1X1VXIAYUFBBM00J', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=str(interval)+"min", outputsize='compact')

    return data
