# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 13:00:07 2021

@author: Nicola
"""
import alphavantage_data_import as alpha
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import mplfinance as mf # https://medium.com/codex/creating-advanced-financial-charts-with-python-in-one-line-of-code-79f87ed482e8


# API KEY: X6T0DKG5FNAWW9R9
api_key = open(r'api_key.txt').read()


def historic_plot(price, volume):
    fig, ax = plt.subplots(2)
    ax[0].plot(price, linewidth=1.0)
    ax[1].plot(volume, linewidth=1.0)
    xfmt = mpl.dates.DateFormatter('%Y-%m')
    ax[1].xaxis.set_major_locator(mpl.dates.MonthLocator(interval=4))
    ax[1].xaxis.set_major_formatter(xfmt)
    xfmt = mpl.dates.DateFormatter('%m')
    ax[1].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=2))
    ax[1].xaxis.set_minor_formatter(xfmt)
    ax[1].get_xaxis().set_tick_params(which='major', pad=25)
    fig.autofmt_xdate()
    plt.show()

def candlestick(df, volume_boolean, mav_tuple):
    '''Candlestick Plot with optional Moving Averages and Volume Chart'''
    mf.plot(df, mav=mav_tuple, type='candle', volume=volume_boolean)


if __name__ == "__main__":
    #tsla_intra = alpha.get_intraday_data(api_key, 'TSLA', '1min')
    #msft_hist = alpha.get_historical_data(api_key, 'MSFT', '2000-01-01')
    #ibm_updates = alpha.get_live_updates(api_key, 'IBM')
    btc_hist = alpha.get_daily_exchange_rates(api_key, 'BTC', 'EUR')
    #eurusd_hist = alpha.get_daily_exchange_rates(api_key, 'USD', 'EUR')
    #yields_10y = alpha.get_treasury_yields(api_key, 'Daily', '10Y')
    
    historic_plot(btc_hist['close (USD)'], btc_hist['volume'])
    
    btc_candlestick = btc_hist[btc_hist.columns.drop(list(btc_hist.filter(regex='(EUR)')))]
    btc_candlestick = btc_candlestick.sort_index() # mplfinance requires ascending data order
    #btc_candlestick.loc[:,btc_candlestick.columns != 'volume'].rename(columns = lambda x: x[:-6].capitalize(), inplace=True)
    btc_candlestick.columns = btc_candlestick.columns.str.replace('..(USD).', '')
    btc_candlestick.rename(columns = lambda x: x.capitalize(), inplace=True)
    candlestick(btc_candlestick[-50:], True, (5, 15))

    
    #historic_plot(alpha.get_historical_data(api_key, 'HLI')['adj close'], alpha.get_historical_data(api_key, 'HLI')['volume'])