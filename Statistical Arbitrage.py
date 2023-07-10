#!/usr/bin/env python
# coding: utf-8

# In[206]:


import numpy as np

import matplotlib.pyplot as plt

import yfinance as yf

from scipy import stats

#INDUSTRY_TICKERS = ["XOM", "SHEL", "CVX"] # exxon mobil, shell, chevron, and bp --> removed BP because of lower correlation
# INDUSTRY_TICKERS = ["PEP", "KO"]
INDUSTRY_TICKERS = ["RTX", "LMT"]
COLORS = ["blue", "red", "green", "orange"]
MARKERS = ["o", "v", "s", "x"]

# constants
OPEN_SCALAR = 1.7
CLOSE_SCALAR = 1
LOSS_STOP = 2


# takes time series for each security and returns a list of long entries, long exits, short entries,
# and short exits for that security
# position list is a list of lists with order: long_entries, long_exits, short_entries, short_exits
# repeated for each security
def find_positions(series_list, avg, open_scalar, close_scalar, loss_stop):
    position_lists = []
    net_gains = []
    for series in series_list:
        long = 0
        short = 0
        long_entries = []
        long_exits = []
        short_entries = []
        short_exits = []
        net_gain = 0
        
        res_sum = 0
        for i in range(len(series)):
            residual = abs(series[i] - avg[i]) # absolute value of residuals
            res_sum += residual
        mean_res = res_sum / len(series)

        open_thresh = mean_res * open_scalar
        close_thresh = mean_res * close_scalar
        
        for i in range(len(series)):
            
            short_entries.append(None)
            short_exits.append(None)
            long_entries.append(None)
            long_exits.append(None)
            if (series[i] - avg[i]) > open_thresh:
                if short==0 and long==0:
                    short = series[i]
                    short_entries[i] = series[i]
            if short != 0 and series[i] - avg[i] < close_thresh:
                short_exits[i] = series[i]
                net_gain += (short - series[i])
                short = 0
            if (avg[i] - series[i] > open_thresh) and short == 0 and long == 0:
                long = series[i]
                long_entries[i] = series[i]
            if long != 0 and avg[i] - series[i] < close_thresh:
                net_gain += (series[i] - long)
                long = 0
                long_exits[i] = series[i]
            if long != 0 and long - series[i] > loss_stop:
                net_gain += series[i] - long
                long_exits[i] = series[i]
                long = 0
                
            if short != 0 and series[i] - short > loss_stop:
                net_gain += short - series[i]
                short_exits[i] = series[i]
                short = 0
                
                
        net_gains.append(net_gain)
                
        position_lists.append(long_entries)
        position_lists.append(long_exits)
        position_lists.append(short_entries)
        position_lists.append(short_exits)
        
        #plot all series
        x = range(len(series))
        plt.plot(x, series, 'o-r')
        plt.plot(x, avg, 'D-k')
        plt.plot(x, long_entries, "^g", ms=15, label="long entry")
        plt.plot(x, long_exits, "^b", ms=15, label="long exit")
        plt.plot(x, short_entries, "vc", ms=15, label="short entry")
        plt.plot(x, short_exits, "vm", ms=15, label="short exit")
        plt.legend()
        plt.show()
        
    
    return position_lists, net_gains
                
                    

                


def stat_arb(tickers, colors, markers, PERIOD, INTERVAL):
    industry_avg = []
    time_series = []
    for i in range(len(tickers)):
        data = yf.Ticker(tickers[i])
        historical_data = data.history(period=PERIOD, interval=INTERVAL)
        closes = list(historical_data['Close'])
        
        norm = np.linalg.norm(closes)
        closes_normalized = closes/norm
        
        if len(industry_avg) == 0:
            industry_avg = closes_normalized
        else:
            industry_avg = industry_avg + closes_normalized
        
        time_series.append(closes_normalized)
        
    industry_avg = industry_avg / (len(tickers))
    
    # begin at 100 for visual consistency
    scalar = 100/industry_avg[0]
    
    x_axis = range(len(industry_avg))
    
    industry_avg_scaled = industry_avg*scalar
    
    time_series_scaled = []
    for i in range(len(time_series)):
        series_scaled = time_series[i]*scalar
        time_series_scaled.append(series_scaled)
        
        plt.plot(x_axis, series_scaled, marker=markers[i], color=colors[i])
        
    plt.plot(x_axis, industry_avg_scaled, marker="D", color="black")
        
    plt.show()
    
    _, gains = find_positions(time_series_scaled, industry_avg_scaled, OPEN_SCALAR, CLOSE_SCALAR, LOSS_STOP)
    print("gains", gains)
    print("total", np.sum(gains))
    print("individual benchmarks:")
    for series in time_series_scaled:
        print(series[len(series)-1] - series[0])
    print("benchmark", len(time_series_scaled)* (industry_avg_scaled[len(industry_avg_scaled)-1] - industry_avg_scaled[0]) )
    
    # calculate correlations:
#     for i in range(len(time_series)):
#         for j in range(len(time_series)):
#             print("Corr btwn", tickers[i], "and", tickers[j] + ":", stats.pearsonr(time_series[i], time_series[j]))
    


# In[207]:



# TEST FUNCTION CALL
stat_arb(INDUSTRY_TICKERS, COLORS, MARKERS, '6mo', '1d')


# In[ ]:




