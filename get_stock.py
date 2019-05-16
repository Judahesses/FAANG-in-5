from os.path import isfile
import requests
import numpy as np
import pandas as pd

file = open('./.env')
api = file.read()


def get_stock(symbol):
    # Check if symbol exists as csv in current directory
    if isfile('./stock_data/' + symbol + '.csv'):
        # return our stored dataframe and with 'Date' as index
        stock = pd.read_csv('./stock_data/' + symbol +
                            '.csv', index_col="Date")
        # Make the index into DateTime
        stock.index = pd.to_datetime(stock.index)
        print('File already exists...')
        # Return our DataFrame in reverse (oldest year to current)
        return stock.iloc[::-1]
    # If it doesn't exit, get data and store it:
    else:
        API_KEY = api
        r = requests.get(
            f'https://www.worldtradingdata.com/api/v1/history?symbol={symbol}&sort=newest&api_token={API_KEY}')
        # Use eval to disregard the type str
        data = eval(r.text)
        stock = pd.DataFrame(data['history'])
        # Transpose the df
        stock = stock.T
        # Make the index into DateTime
        stock.index = pd.to_datetime(stock.index)
        # Make index name 'Date'
        stock.index.name = 'Date'
        # Creates a csv file with complete stock history
        stock.to_csv('./stock_data/' + symbol + '.csv')
        # Return our DataFrame in reverse (oldest year to current)
        return stock.iloc[::-1]
