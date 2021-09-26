
#%%
import twstock
from twstock import realtime
import pandas as pd


twstock.__update_codes()
stock = twstock.realtime.get('2330')

stock3 = {**stock['realtime'], **stock['info']}
df = pd.DataFrame.from_dict([stock3])
print(df)