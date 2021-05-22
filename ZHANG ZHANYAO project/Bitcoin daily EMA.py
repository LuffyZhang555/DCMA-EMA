import time
import ccxt
from time import gmtime, strftime
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#EMA:


Bitdaily = pd.read_csv("ETH-daily.csv")

df = pd.DataFrame(index=np.arange(1800),columns=['short term parameter','long term parameter','average return','accumulated return','win ratio','max','min'])

k=0
for i in range(1,20):
    for j in range(21,80):
        Bitdaily['EMAsmall'] = Bitdaily['close'].transform(lambda x: x.ewm(span=i, adjust=False).mean())
        Bitdaily['EMAbig'] = Bitdaily['close'].transform(lambda x: x.ewm(span=j, adjust=False).mean())
        Bitdaily['difference'] = Bitdaily['EMAsmall'] - Bitdaily['EMAbig']


        def label(a):
            if a > 0:
                b = 1;
            else:
                b = -1;
            return b


        Bitdaily['label'] = Bitdaily['difference'].apply(label)
        Bitdaily["result"] = Bitdaily["label"] + Bitdaily["label"].shift()
        Bitdaily1 = Bitdaily[Bitdaily['result'] == 0]
        Bitdaily1["return"] = Bitdaily1['close'].pct_change()
        Bitdaily2 = Bitdaily1[Bitdaily1['label'] == -1]


        def win(a):
            if a > 0:
                b = 1;
            else:
                b = 0;
            return b


        Bitdaily2['win'] = Bitdaily2['return'].apply(win)
        sum1 = Bitdaily2['win'].sum()
        number = len(Bitdaily2.index)
        ratio = sum1 / number
        df.iloc[k, df.columns.get_loc('win ratio')] = ratio
        avgreturn = Bitdaily2['return'].mean()
        df.iloc[k, df.columns.get_loc('average return')] = avgreturn
        most = Bitdaily2['return'].max()
        df.iloc[k, df.columns.get_loc('max')] = most
        least = Bitdaily2['return'].min()
        df.iloc[k, df.columns.get_loc('min')] = least
        Bitdaily2['return2'] = Bitdaily2['return'] + 1
        finalproduct = Bitdaily2['return2'].prod()-1
        df.iloc[k, df.columns.get_loc('accumulated return')] = finalproduct
        df.iloc[k, df.columns.get_loc('short term parameter')] = i
        df.iloc[k, df.columns.get_loc('long term parameter')] = j
        k=k+1
print(df.head(10))
df.to_csv(' EMA-ETH-daily-result.csv',index=False)