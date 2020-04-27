import pandas as pd
import matplotlib.pyplot as plt

def get_technical_indicators(dataset):
    # Create 7 and 21 days Moving Average
    dataset['ma7'] = dataset['price'].rolling(window=7).mean()
    dataset['ma21'] = dataset['price'].rolling(window=21).mean()
    
    # Create EMA 20/50/100/200
    dataset['20ema'] = dataset['price'].ewm(span=20, adjust=False).mean()
    dataset['50ema'] = dataset['price'].ewm(span=50, adjust=False).mean()
    dataset['100ema'] = dataset['price'].ewm(span=100, adjust=False).mean()
    dataset['200ema'] = dataset['price'].ewm(span=200, adjust=False).mean()
    
    # Create MACD_12_26_9
    dataset['26ema'] = dataset['price'].ewm(span=26, adjust=False).mean()
    dataset['12ema'] = dataset['price'].ewm(span=12, adjust=False).mean()
    dataset['MACD_12_26'] = (dataset['12ema']-dataset['26ema']).rolling(window=9).mean()
    
    # Create MACD_3_10_16
    dataset['3ema'] = dataset['price'].ewm(span=3, adjust=False).mean()
    dataset['10ema'] = dataset['price'].ewm(span=10, adjust=False).mean()
    dataset['MACD_3_10'] = (dataset['3ema']-dataset['10ema']).rolling(window=9).mean()

    # Create Bollinger Bands
    dataset['20sd'] = dataset['price'].rolling(window=20).std()
    dataset['upper_band'] = dataset['ma21'] + (dataset['20sd']*2)
    dataset['lower_band'] = dataset['ma21'] - (dataset['20sd']*2)
    
    # Create Momentum (14 days shift)
    dataset['momentum'] = dataset['price']-dataset['price'].shift(14)
    
    dataset.fillna(0, inplace=True)
    
    return dataset


def plot_technical_indicators(dataset, last_days):
    plt.figure(figsize=(16, 10), dpi=100)
    shape_0 = dataset.shape[0]
    xmacd_ = shape_0-last_days
    
    dataset = dataset.iloc[-last_days:, :]
    x_ = range(3, dataset.shape[0])
    x_ =list(dataset.index)
    
    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dataset['ma7'],label='MA 7', color='y',linestyle='--')
    plt.plot(dataset['price'],label='Closing Price', color='b')
    plt.plot(dataset['20ema'],label='EMA 20', color='g',linestyle='--')
    plt.plot(dataset['50ema'],label='EMA 50', color='r',linestyle='--')
    plt.plot(dataset['100ema'],label='EMA 50', color='m',linestyle='--')
    plt.plot(dataset['upper_band'],label='Upper Band', color='c')
    plt.plot(dataset['lower_band'],label='Lower Band', color='c')
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.35)
    plt.title(f'Technical indicators for last {last_days} days.')
    plt.ylabel('USD')
    plt.legend()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    plt.title('MACD')
    plt.plot(dataset['MACD_12_26'],label='MACD_12_26', linestyle='-.', color='r')
    plt.plot(dataset['MACD_3_10'],label='MACD_3_10', linestyle='-.', color='k')
    plt.hlines(15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.hlines(-15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.plot(dataset['momentum'],label='Momentum', color='b',linestyle='-')

    plt.legend()
    plt.show()
