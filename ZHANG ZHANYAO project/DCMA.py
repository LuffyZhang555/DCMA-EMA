import time
import ccxt
from time import gmtime, strftime
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
BitDaily = pd.read_csv("ETH-hourly.csv")#D capital reprents for MACD
df = pd.DataFrame(index=np.arange(27000),columns=['short term parameter','long term parameter','signal parameter','average return','accumulated return','win ratio','max','min'])

m=0
for i in range(1,21):
    for j in range(21,80):
        for k in range(2,15):
            BitDaily['EMAsmall'] = BitDaily['close'].transform(lambda x: x.ewm(span=i, adjust=False).mean())
            BitDaily['EMAbig'] = BitDaily['close'].transform(lambda x: x.ewm(span=j, adjust=False).mean())
            BitDaily['DIF'] = BitDaily['EMAsmall'] - BitDaily['EMAbig']
            BitDaily['SIG'] = BitDaily['DIF'].transform(lambda x: x.ewm(span=k, adjust=False).mean())
            BitDaily['MACD'] = BitDaily['DIF'] - BitDaily['SIG']


            def label(a):
                if a > 0:
                    b = 1;
                else:
                    b = -1;
                return b


            BitDaily['label'] = BitDaily['MACD'].apply(label)
            BitDaily["result"] = BitDaily["label"] + BitDaily["label"].shift()
            BitDaily1 = BitDaily[BitDaily['result'] == 0]
            BitDaily1["return"] = BitDaily1['close'].pct_change()
            BitDaily2 = BitDaily1[BitDaily1['label'] == -1]


            def win(a):
                if a > 0:
                    b = 1;
                else:
                    b = 0;
                return b


            BitDaily2['win'] = BitDaily2['return'].apply(win)
            sum1 = BitDaily2['win'].sum()
            number = len(BitDaily2.index)
            ratio = sum1 / number
            df.iloc[m, df.columns.get_loc('win ratio')] = ratio
            avgreturn = BitDaily2['return'].mean()

            df.iloc[m, df.columns.get_loc('average return')] = avgreturn
            most = BitDaily2['return'].max()
            df.iloc[m, df.columns.get_loc('max')] = most
            least = BitDaily2['return'].min()
            df.iloc[m, df.columns.get_loc('min')] = least
            BitDaily2['return2'] = BitDaily2['return'] + 1
            finalproduct = BitDaily2['return2'].prod() - 1
            df.iloc[m, df.columns.get_loc('accumulated return')] = finalproduct
            df.iloc[m, df.columns.get_loc('short term parameter')] = i
            df.iloc[m, df.columns.get_loc('long term parameter')] = j
            df.iloc[m, df.columns.get_loc('signal parameter')] = k
            m = m + 1
print(df.head(10))
df.to_csv(' MACD-ETH-hourly-result.csv', index=False)


