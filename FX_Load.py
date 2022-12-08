def load(df, pair):
    
    df_existing = pd.read_csv(f'{pair}_Candlestick_Signals.csv', index_col=0)
    df_new = pd.concat([df, df_existing[:]]).reset_index(drop=True)
    df_new.to_csv(f'{pair}_Candlestick_Signals.csv')
    
    return f'File saved as: {pair}_Candlestick_Signals.csv'
