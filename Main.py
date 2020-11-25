import pandas
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='1X1VXIAYUFBBM00J', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AAPL',interval='5min', outputsize='full')

print(data)

open = data["1. open"]
high = data["2. high"]
low = data["3. low"]
close = data["4. close"]

fig, ax = plt.subplots()
ax.plot(data.index, open, label='open')
ax.plot(data.index, high, label='high')
ax.plot(data.index, low, label='low')
ax.plot(data.index, close, label='close')
plt.legend()
plt.show()