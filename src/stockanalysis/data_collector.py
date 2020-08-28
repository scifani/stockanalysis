import logging
import pandas as pd
import yfinance as yf


class DataCollector:
    def __init__(self):
        logging.debug("DataCollector::__init__")

    def get_ticker_history(self, ticker_name):
        '''
            Returns an array containing all the available daily close prices
        '''
        ticker = yf.Ticker(ticker_name)
        
        # period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max                
        # interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo [Intraday data cannot extend last 60 days]                
        # start/end: 'YYYY-MM-DD' [default: start='1900-01-01' end='now' ; NB: use either period or start/end]        
        df = ticker.history(period='max', interval='1d', start=None, end=None)
      
        df = df['Close']

        # from pandas Series to numpy.ndarray
        array = df.values.reshape(df.shape[0],1)

        return array
