import pandas_datareader as pdr
import configparser
import sqlite3
import os

config = configparser.ConfigParser()
config.read('C:/Users/Puneeth/PycharmProjects/tsworks/config.ini')

tickers = [config.get('Companies', option) for option in config.options('Companies')]

for ticker in tickers:
    data = yf.download(ticker, period='1d')
    print(data)

conn = sqlite3.connect('finance.db')

for company in companies:
    ticker = company[0]
    name = company[1]
    print(f'Downloading {name} ({ticker})')
    df = pdr.get_data_yahoo(ticker)
    df.to_sql(ticker, conn, if_exists='replace')

conn.close()




