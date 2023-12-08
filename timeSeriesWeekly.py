import requests
import pandas as pd

# Alpha Vantage API key
api_key = 'EPB0IFY8X8XUHI9J'

# List of stock symbols
symbols = ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'AXP', 'V', 'MA', 'SCHW']

for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    
    if 'Weekly Adjusted Time Series' in data:
        # Convert the weekly data to a DataFrame
        weekly_data = pd.DataFrame(data['Weekly Adjusted Time Series']).T
        column_names = {
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        }
        weekly_data.rename(columns=column_names, inplace=True)
        weekly_data['Symbol'] = symbol
        column_order = ['Symbol'] + [col for col in weekly_data.columns if col != 'Symbol']
        weekly_data = weekly_data[column_order]
        
        # Convert index to datetime
        weekly_data.index = pd.to_datetime(weekly_data.index)
        
        # Filter data within the specified date range
        weekly_data = weekly_data.loc['2021-09-16':'2023-11-10']

        # Calculate weekly returns and add a new column 'Weekly Return'
        weekly_data['Close'] = weekly_data['Close'].astype(float)
        weekly_data['Weekly Return'] = weekly_data['Close'].pct_change() * 100

        # Save the data to a CSV file labeled with company name
        file_name = f'{symbol}_stockData.csv'
        weekly_data.to_csv(file_name, index=True)

        print(f'{file_name} saved successfully!')