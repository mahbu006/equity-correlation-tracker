import numpy as np
import pandas as pd
import pandas_datareader as web
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn

from get_portfolio import *


def main():
    start = datetime(2015, 1, 1)
    symbols_list = ['AAPL', 'FB', 'TWTR', 'F', 'TSLA', 'GE', 'AMZN']

    symbols = []

    for ticker in symbols_list:
        r = web.DataReader(ticker, 'yahoo', start)
        r['Symbol'] = ticker
        symbols.append(r)

    df = pd.concat(symbols)
    df = df.reset_index()
    df = df[['Date', 'Close', 'Symbol']]

    df_pivot = df.pivot('Date', 'Symbol', 'Close').reset_index()

    corr_df = df_pivot.corr(method='pearson')

    corr_df.head().reset_index()
    #del corr_df.index.name
    # print(corr_df.head(10))

    mask = np.zeros_like(corr_df)
    mask[np.triu_indices_from(mask)] = True

    seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0,
                    vmin=-1.0, mask=mask, linewidths=2.5)
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    plt.show()


main()
