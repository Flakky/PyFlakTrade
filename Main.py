import pandas

import matplotlib.pyplot as plt
import StocksReciever

data = StocksReciever.receiveStocks("AAPL", 5)

print(StocksReciever.getCurrentValue("AAPL"))

print(data)

# open = data["1. open"]
# high = data["2. high"]
# low = data["3. low"]
# close = data["4. close"]
#
# deltas = []
#
# prevVal = close[0]
# for closeVal in close:
#     deltas.append(prevVal - closeVal)
#     prevVal = closeVal
#
# deltasPercentage = []
# for i in range(0, len(close)):
#     deltasPercentage.append((deltas[i] / close[i])*100)
#
# fig = plt.figure()
#
# plt.subplot(2,1,1)
# plt.bar(data.index, high-low, width=0.0005, bottom=low)
# plt.bar(data.index, open-close, width=0.001, bottom=close)
# plt.plot(data.index, close, label='close')
# plt.legend()
#
# plt.subplot(2,1,2)
# plt.bar(data.index, deltas, 0.002)
# plt.bar(data.index, deltasPercentage, 0.001)
#
# plt.show()