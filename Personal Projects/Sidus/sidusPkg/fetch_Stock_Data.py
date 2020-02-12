import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
		self.data_frame.plot(kind = "scatter", x = x_stock1, y = y_stock2, figsize = (16,6), alpha = 0.4, label = "Data", title = f" regression between {x_stock1} and {y_stock2}")
		plt.plot(self.data_frame[x_stock1], model.predict(), label = "regression line", c = "r")
		plt.legend()
		return model.summary2(), results
	def plot_graphs(self):
		fig, axes = plt.subplots(len(self.tickers), figsize = (16,10))
		for index, securt in enumerate(self.tickers):
			axes[index].plot(self.data_frame[securt])
			axes[index].set_xlabel(f"{self.tickers[index]}")
			print(f"here is the length {len(self.tickers)}")
		return fig
	def portfolio_return(self, weights = [0.5,0.5]):
		"""
		function takes in weights as an array. Default is assuming there is 2 securties at a even weighted portfolio of 50%, 50%. You must enter the weights as an array based on the number of tickers in the portfolio
		for example: 2 stocks [0.5,0.5], with 4 stocks securties = [0.25,0.25,0.25,0.25]
		"""
		portFolio_Weight = np.array(weights)
		annual = np.mean(self.daily_changes) * 250
		print(f"{annual}")
		portfolio_Return_pct = np.dot(annual, portFolio_Weight)
		return f"The return for the portfolio containing {self.tickers} is {round(portfolio_Return_pct * 100, 3)} % for the period of {self.start} to {self.end}"
	def check_Portfolio_Volitility(self, weights):
		"""
		Using the Volitility function enter the weights of the portfolio as an array: eg: 2 securties at 50/50 weight =  [0.5, 0.5], 4 = [0.25,0.25,0.25,0.25]
		"""
		port_vol = np.dot(np.array(weights).T, np.dot(self.daily_changes.cov() * 250, np.array(weights))) ** 0.5
		return f"The Volitility of the portfolio containing {self.tickers} is {round(port_vol, 4) * 100 } % for the period of {self.start} to {self.end}"


