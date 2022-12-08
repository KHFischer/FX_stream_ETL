from FX_Extract import connect_polygon, gen_df
from FX_Transform import gen_indicators, signals
from FX_Load import load 

if __name__ == '__main__':
    
    # Data we will request
    pair = 'EURUSD'
    timespan = 'day'
    multiplier = 1
    delta_days = 100
    
    
    # Checking status code of connection to API
    print('[Extract] Connecting to API')
    
    connection = connect_polygon('9BjGjhpj_FrVkFI0I6BIexgjgovIxpjO')
    
    if connection != 200:
        print('[Error] check API connection status')
    else:
        print('[Extract] Connection established succesfully')
        
        
        # If connection is established request relevant data
        print(f'[Extract] Retrieving OHLC data for {pair}')
        df = gen_df(pair, timespan, multiplier, delta_days)
        print('[Extract] Finished \n')
        
        
        # Calculate indicators
        print('[Transform] Transforming data')
        df = gen_indicators(df)
        print('[Transform] Finished \n')
        
        
        # Generate signals
        signals(df)
    
        # Save result to existing file for record keeping purposes
        print(f'[Load] Saving data to file "{pair}_Candlestick_Signals.csv"')
        load(df, pair)
        print(f'[Load] Finished')
