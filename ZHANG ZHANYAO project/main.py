import time
import ccxt
import pandas as pd
exchange = ccxt.binance()
def get_bar_from_to(ex, symbol, period, start_time, end_time, length=2000, maxLoop=20):
    data = []
    stime = ex.parse8601(start_time)  # ISO8601 is the format of time
    etime = ex.parse8601(end_time)
    loop_i = 0
    if ex.has['fetchOHLCV']:
        while stime < etime and loop_i < maxLoop:
            loop_i += 1
            try:
                ohlcvs = ex.fetch_ohlcv(symbol, period, stime, limit=length)
                print(ex.iso8601(ex.milliseconds()), 'loop_i=', loop_i, ' ,Fetched', len(ohlcvs), 'candles')
                if len(ohlcvs) > 1:
                    first = ohlcvs[0][0]
                    last = ohlcvs[-1][0]
                    print('[', ex.iso8601(first), '--', ex.iso8601(last), ']')
                    stime = int(last + (last - first) / (len(ohlcvs) - 1))
                    data += ohlcvs
                    time.sleep(1)
                else:
                    return data
            except Exception as e:
                print(str(e))
    return data
# Let's have an example
start_time = '2020-01-01 00:00:00'
end_time = '2021-03-05 23:00:00'
symbol = 'ETH/USDT'
period = '1h' # '1d', '1m', '5m'
data0 = exchange.fetch_ohlcv(symbol, period, exchange.parse8601(start_time))
# ohlcv is open, high, low, close, volume
data = get_bar_from_to(exchange,symbol,period, start_time, end_time)
test = pd.DataFrame(data, columns=['time','open','high','low','close','volume'])
test.to_csv('ETH-hourly.csv',index=False)

