import pandas as pd
import numpy as np


data = pd.read_csv(" MACD-ETH-daily-result.csv")
#Bitdaily1 = Bitdaily[Bitdaily['time']<'2018/4/9']
#data1=data[(data['average return']>0.1) & (data['accumulated return']>35) & (data['win ratio']>0.4)]  ##this is for MACD-btc-daily
data1=data[(data['average return']>0.2) & (data['accumulated return']>45) & (data['win ratio']>0.4)] ##this is for MACD-ETH-daily
#data1=data[(data['average return']>0.01) & (data['accumulated return']>1) & (data['win ratio']>0.3)] ##this is for MACD-btc-houry
#data1=data[(data['average return']>0.01) & (data['accumulated return']>13) & (data['win ratio']>0.3)] ##this is for MACD-ETH-hourly

data1.sort_values(by=['accumulated return'], ascending=False, inplace=True)
print(data1)
data1.to_csv(' MACD-ETH-daily-final-result.csv',index=False)