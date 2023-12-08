import requests
import pandas as pd

# Alpha Vantage API key
api_key = '7AHUGIID4EMLOUL5'

# List of stock symbols
symbols = ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'AXP', 'V', 'MA', 'SCHW']

for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'
    r = requests.get(url)
    data = r.json()
    print(symbol, data)
    
    if 'Time Series (Daily)' in data:
        # Convert the daily data to a DataFrame
        daily_data = pd.DataFrame(data['Time Series (Daily)']).T
        column_names = {
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        }
        daily_data.rename(columns=column_names, inplace=True)
        daily_data['Symbol'] = symbol
        column_order = ['Symbol'] + [col for col in daily_data.columns if col != 'Symbol']
        daily_data = daily_data[column_order]
        
        # Convert index to datetime
        daily_data.index = pd.to_datetime(daily_data.index)
        
        # Filter data within the specified date range
        daily_data = daily_data.sort_index().loc['2021-09-16':'2023-11-10']

        # Calculate daily returns and add a new column 'daily Return'
        daily_data['Close'] = daily_data['Close'].astype(float)
        daily_data['Daily Return'] = daily_data['Close'].pct_change() * 100

        # Save the data to a CSV file labeled with company name
        file_name = f'{symbol}_stockData.csv'
        daily_data.to_csv(file_name, index=True)

        print(f'{file_name} saved successfully!')