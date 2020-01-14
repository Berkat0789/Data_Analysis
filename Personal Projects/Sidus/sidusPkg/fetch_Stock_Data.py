import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web

class Firm():
	"""
	This class takes in 4 items: tickers(Securties to evaluate),
	start(start date of data), end(date to stop), data type(Open, close,volumem Adj Close)
	"""
	def __init__(self, tickers, start = "2002-1-1", end = "2019-12-30", data_type = "Adj Close"):
		self.tickers = tickers
		self.start = start
		self.end = end
		self.data_type = data_type
		self.daily_changes = pd.DataFrame()
		self.daily_returns = pd.DataFrame()
	def fetch_Data(self):
		data_frame = pd.DataFrame()
		for t in self.tickers:
			data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)[self.data_type]
		return [data_frame.head(), data_frame.plot(figsize = (16,6))]
	def dailyChanges(self):
		data_frame = pd.DataFrame()
		self.daily_changes = pd.DataFrame()
		for t in self.tickers:
			data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)["Adj Close"]
			self.daily_changes[t] = data_frame[t].pct_change()
		return [self.daily_changes.tail(), self.daily_changes.plot(figsize = (16,6))]
	def dailyRetuns(self):
		data_frame = pd.DataFrame()
		self.daily_returns = pd.DataFrame()
		for t in self.tickers:
			data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)["Adj Close"]
			self.daily_returns[t] = (1 + self.daily_changes[t]).cumprod()
		return [self.daily_returns.tail(), self.daily_returns.plot(figsize = (16,6))]



