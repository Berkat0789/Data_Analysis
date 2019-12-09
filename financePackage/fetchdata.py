import pandas as pd
import numpy as  np
from pandas_datareader import data as wb


def fetch_data(*kwargs):
   frame = pd.DataFrame()
   for t in kwargs:
    frame[t] = wb.Datareader(t, data_source = "yahoo", start = "2001- 1-1")["Adj Close"]
    return frame

   
