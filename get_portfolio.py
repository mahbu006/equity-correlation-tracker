from flask import Flask, render_template
import numpy as np
import pandas as pd
import pandas_datareader as web
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn
import yfinance as yf

app = Flask(__name__)


@app.route('/')
def get_portfolio():

    tickers = ['AAPL', 'GE', 'LULU', 'TSLA', 'AAL', 'PFE', 'VRTX', 'WFC']
    # tickers.append(ticker)

    positions = [42, 143, 131, 30, 11, 65, 97, 12]
    # positions.append(positions)

    # Initialize the portfolio data frame and set start/end dates
    portfolio = pd.DataFrame()
    start = '2015-01-01'
    end = datetime.today()

    # Put price of each individual asset times its position into the data frame
    for i in range(len(tickers)):
        ticker = tickers[i]
        stock = yf.download(tickers=ticker, start=start, end=end)
        portfolio[ticker] = stock["Close"].copy()*positions[i]

    # Drop ticker from portfolio
    current_portfolio = portfolio.drop(ticker, 1)

    # Calculate the entire value of portfolio
    portfolio["Portfolio"] = current_portfolio.sum(axis=1)

    # Pearson correlation coefficient
    corr_df = portfolio.corr(method='pearson')

    corr_df.head().reset_index()
    #del corr_df.index.name
    print(corr_df)

    mask = np.zeros_like(corr_df)
    mask[np.triu_indices_from(mask)] = True

    seaborn.set_style('dark')
    seaborn.heatmap(corr_df, annot=True, cmap='RdYlBu', vmax=1.0,
                    vmin=-1.0, mask=mask, linewidths=2.5)
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    plt.title('Equity Portfolio Correlation Tracker',
              fontweight='bold', color='royalblue', fontsize='18')
    plt.savefig('static/images/plot.png')

    return render_template('plot.html', url='/static/images/plot.png')


if __name__ == '__main__':
    app.run()
