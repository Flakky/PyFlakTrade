import pandas
from alpha_vantage.timeseries import TimeSeries


def receiveStocks(symbol, interval=5):
    ts = TimeSeries(key='1X1VXIAYUFBBM00J', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=str(interval)+"min", outputsize='compact')

    return data
