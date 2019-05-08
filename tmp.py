import pandas as pd

df = pd.read_csv('BTC.csv', header=None)
df.rename(columns={0: 'timestamp', 1: 'symbol',2:'open',3:'high',4:'low',5:'close',6:'trades',7:'volume',8:'vwap',9:'lastSize',10:'turnover',11:'homeNotional',12:'foreignNotional'}, inplace=True)
df.to_csv('BTCwithCname.csv', index=False) # save to new csv file
