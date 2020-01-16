import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import statsmodels.api as sm
from scipy import stats

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
		self.data_frame = pd.DataFrame()
		self.daily_changes = pd.DataFrame()
		self.daily_returns = pd.DataFrame()

	def fetch_Data(self):
		self.data_frame = pd.DataFrame()
		for t in self.tickers:
			self.data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)[self.data_type]
		return [self.data_frame.head(), self.data_frame.plot(figsize = (16,6))]


	def dailyChanges(self, plottype = "line"):
		self.daily_changes = pd.DataFrame()
		for t in self.tickers:
			self.data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)["Adj Close"]
			self.daily_changes[t] = self.data_frame[t].pct_change()
		return [self.daily_changes.tail(), self.daily_changes.plot(kind = f"{plottype}",figsize = (16,6))]

	def dailyReturns(self, plottype = "line"):
		data_frame = pd.DataFrame()
		self.daily_returns = pd.DataFrame()
		for t in self.tickers:
			self.data_frame[t] = web.DataReader(t, "yahoo", start = self.start, end = self.end)["Adj Close"]
			self.daily_returns[t] = (1 + self.daily_changes[t]).cumprod()
		return [self.daily_returns.tail(), self.daily_returns.plot(kind = f"{plottype}",figsize = (16,6))]

	def compare2(self, x_stock1, y_stock2):
		self.daily_returns.dropna(inplace = True)
		x_constant = sm.add_constant(self.data_frame[x_stock1])
		model = sm.OLS(self.data_frame[y_stock2],x_constant).fit()
		results = stats.linregress(self.data_frame[x_stock1], self.data_frame[y_stock2])
		return model.summary2(), self.data_frame.plot(kind = "scatter", x = x_stock1, y = y_stock2, figsize = (16,6), alpha = 0.4), results
	def plot_graphs(self):
		fig, axes = plt.subplots(len(self.tickers), figsize = (16,10))
		for index, securt in enumerate(self.tickers):
			axes[index].plot(self.data_frame[securt])
			axes[index].set_xlabel(f"{self.tickers[index]}")
			print(f"here is the length {len(self.tickers)}")
		return fig







