import pandas as pd
import numpy as np
from polygon import RESTClient
import requests
import json
from datetime import date
from datetime import timedelta
import talib
from talib import abstract
import os

apikey = os.environ.get('Polygon_api_key_1')


def connect_polygon(api_key):
    
    url = f'https://api.polygon.io/v3/reference/exchanges?asset_class=fx&apiKey={api_key}'    
    res = requests.request("GET", url)
    
    return res.status_code
  
  
def gen_ohlc(pair, timespan, multiplier, delta_days):
    
    
    # E.g. 'EURUSD' or 'GBPUSD' 
    # Datatype = String
    if type(pair) == str:
        pair = pair.upper()
    else:
        return f'{pair} is not a valid currency pair, valid inputs include: EURUSD, DKKNOK etc.'
        
    
    # Adjust for splits options are 'true' or 'false'  
    # Datatype = String
    adjusted = 'true'

    
    # Timespan multiplier, if timespan is 'hour' and multiplier is 5 the output will be ohlc data for 5 hour candlesticks
    # Datatype = Integer
    multiplier = multiplier

    
    # Timespan of candlestick, for example 'hour' or 'day', 
    # Datatype = String
    timespan_options = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']
    
    if timespan.lower() in timespan_options:
        timespan = str(timespan.lower())
    else:
        return f'{timespan} is not a valid timespan, valid timespans are: {timespan_options}'

    
    # Format: YYY-MM-DD or datetime obj
    # Datatype = String
    to_date = date.today() - timedelta(days=1)
    
    if type(delta_days) == int:
        from_date = date.today() - timedelta(days=delta_days)
    else:
        return f'{delta_days} is not a valid timedelta, timedelta must be an integer'

    
    # Sort values, 'asc' or 'desc', asc = oldest at the top
    # Datatype = String
    sort = 'desc'

    
    # Request data
    url = f'https://api.polygon.io/v2/aggs/ticker/C:{pair}/range/{multiplier}/{timespan}/{from_date}/{to_date}?adjusted=true&sort={sort}&limit=120&apiKey={apikey}'
    response = requests.request("GET", url)

    
    data = json.loads(response.text)
    
    
    if data['resultsCount'] == 0:
        return f'Invalid inputs: {data}'
    else: 
        return data
      
      
def gen_df(pair, timespan, multiplier, delta_days):
    
    # Generate OHLC data
    data = gen_ohlc(pair, timespan, multiplier, delta_days)
    
    
    # Take the ohlc for the len of delta_days
    datelist = []
    openlist = []
    highlist = []
    lowlist = [] 
    closelist = []

    for i in range(data['count']):
        datelist.append(date.today() - timedelta(days=i+1))
        openlist.append(data['results'][i]['o'])
        highlist.append(data['results'][i]['h'])
        lowlist.append(data['results'][i]['l'])
        closelist.append(data['results'][i]['c'])

        
    # Create dictionary of lists
    mydict = {
        'date': datelist,
        'open': openlist,
        'high': highlist,
        'low': lowlist,
        'close': closelist
    }
    
    
    # Convert to dataframe
    df = pd.DataFrame(mydict)
    
    return df
