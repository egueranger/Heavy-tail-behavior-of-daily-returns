from math import *
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

#===============================================================================
# Tiingo API and data recovery (AI generated)

import requests
import pandas as pd
from datetime import datetime

class TiingoClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tiingo.com/tiingo"

    def get_close_prices(self, ticker: str, start_date: str, end_date: str):
        """
        Given a ticker, recovers adjusted daily prices.
        start_date et end_date 'YYYY-MM-DD' form.
        """
        url = f"{self.base_url}/daily/{ticker}/prices"
        params = {
            "token": self.api_key,
            "startDate": start_date,
            "endDate": end_date,
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        return df["adjClose"].tolist()

API_KEY = "eddfccbe3cca986363149ab559b5e62d91fcbfd4"
client = TiingoClient(API_KEY)
prices = client.get_close_prices("SPY", "2000-01-01", "2026-03-25")

#===============================================================================
# My own algorithm
#===============================================================================

# Compute daily log returns
n = len(prices)-1
returns = []
mean, variance = 0, 0
for i in range(n):
    returns.append(abs(log(prices[i+1]/prices[i])))
    mean += log(prices[i+1]/prices[i])
    variance += (log(prices[i+1]/prices[i]))**2
mean /= n
variance /= n
variance -= mean**2
returns.sort()

def histogram():
    """
    Plot the histogram of daily log returns.
    """
    plt.hist(returns, bins=100, color='grey', edgecolor='black', alpha=0.8)
    plt.xlabel('Daily absolute log returns')
    plt.ylabel('Count')
    plt.title('Daily absolute log returns of the S&P500')
    plt.show()



def plot_tail(mean=mean, variance=variance):
    """
    Compares the empirical tail with the Gaussian on a log-log plot.
    """
    X = []
    Yemp = []
    Yth = []
    for i in range(n):
        # Empirical
        X.append(returns[i])
        Yemp.append((n-i)/n)
        # Theoretical
        Yth.append(2*(1-norm.cdf(returns[i], loc=mean, scale=sqrt(variance))))
    plt.scatter(X, Yemp, c='black', s=1, label='S&P500')
    plt.plot(X, Yth, c='grey', label='Gaussian')
    plt.xlim(1/n)
    plt.xscale('log')
    plt.xlabel('Daily absolute log return')
    plt.yscale('log')
    plt.ylabel('Probability')
    plt.title('Empirical distribution tail VS Gaussian')
    plt.legend()
    plt.show()

def estimate_tail_index_ml(threshold=0.03)->tuple:
    """
    Estimates the tail index with the maximum-likelihood method. Returns the
    estimation with confidence interval radius (beta, r).
    """
    S = 0
    N = 0
    for i in range(n):
        if returns[i]>threshold: # We only keep variations above threshold
            S += log(returns[i]/threshold)
            N += 1
    beta = N/S # Maximum-likelihood estimator
    return (beta, beta*1.9600/sqrt(N))

def plot_qq(mean=mean, variance=variance):
    """
    Compares the empirical tail with the Gaussian on a QQ-plot.
    """
    Xemp = []
    Xth = []
    for i in range(n):
        # Empirical
        Xemp.append(returns[i])
        # Theoretical
        Xth.append(norm.ppf(1/2+i/(2*n), loc=mean, scale=sqrt(variance)))
    plt.scatter(Xth, Xemp, c='black', s=1, label='S&P500')
    plt.plot(Xth, Xth, c='grey', label='Gaussian')
    plt.xlabel('Gaussian')
    plt.ylabel('Empirical')
    plt.title('QQ-plot empirical VS Gaussian')
    plt.legend()
    plt.show()