def gen_indicators(df):

    # All possible patterns
    all_indicators = [x for x in dir(abstract) if x.startswith('CDL')]

    # Calculate all patterns and add to dataframe
    for i in all_indicators:
        df[str(i.split('CDL')[1])] = getattr(abstract, i)(df)

    return df
  
  
def signals(df):    
    signallist = []

    for i in slic.columns:
        if slic[i][0] != 0:
            signallist.append(slic[i].name)

    if len(signallist) == 0:
        return f'No new signals in {pair}'
    else:
        return f'New signals in: {signallist} for pair: {pair}'
