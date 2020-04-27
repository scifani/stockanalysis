import pandas as pd
import yfinance as yf

def get_history(ticker_name, out_csv=None):
    ticker = yf.Ticker(ticker_name)
    df = ticker.history(period='max', interval='1d')
    if (out_csv is not None):
        df.to_csv(out_csv)
    return df