# -*- coding: utf-8 -*-
"""class6+lh3298.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1up4zol1tQiMK_GtcuSWY7mRd0Lw5WxYe

# getReturn
"""

import yfinance as yf
import pandas as pd

# download Yahoo Finance data
def YahooDataExtract(ticker="GS"):

    # Step 1: download the data
    data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

    # Step 2:  `Close` column
    close_prices = data["Close"].values

    return close_prices

# calculate lagged return
def get_lagged_returns(prices):

    returns = (prices[1:] / prices[:-1]) - 1
    return returns


if __name__ == "__main__":

    adclose_prices = YahooDataExtract("GS")


    returns = get_lagged_returns(adclose_prices)


    print("\nLagged Returns:")
    print(returns[:10])  # just first 10

"""# qVaR"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def VaR(r,confidence,principle=1):

  #mean and std
  mean_r=np.mean(r)
  std_r=np.std(r)

  #quantile
  alpha=1-confidence
  percentile=norm.ppf(alpha,mean_r,std_r)  #norm distribution calculate 1-αpercentile

  #VaR
  VaR=principal*abs(percentile)

def percent_var(r,confidence):
    alpha=1-confidence
    out=np.percentile(r,alpha*100)
    plt.hist(r,bins=50,alpha=0.75)
    plt.show()
    return abs(out) #return the absolute value of the calculated percentile

#Example tools:percentile
returns=np.random.normal(0,1,10000)
print(np.percentile(returns,97.72))

#Unit test
r=np.random.normal(0.05,0.03,1000000)
probability2SD=norm.cdf(2) #Probability under normal curve within 2 standard deviations

my_confidence=probability2SD
my_percent_var=percent_var(r,my_confidence)
print(np.round(my_percent_var,2)==0.01)

"""# qES"""

import numpy as np
def ES(losses,confidence=None,VaR=None,use_PnL=False):
  if VaR is None:
    VaR=np.percentile(losses,100*confidence)
  es_value=np.mean(losses[losses>VaR])  #这个缩进和if对齐
  return es_value

#Unit test
u=np.random.uniform(0,100,100000)

#Test the ES function with an confidence of 0.8
es_confidence=ES(losses=u,confidence=0.8)
print('ES with confidence:',np.round(es_confidence,0)==90)

#Test the ES function with a VaR of 80
es_var=ES(losses=u,VaR=80)
print('ES with VaR:',np.round(es_var,0)==90)