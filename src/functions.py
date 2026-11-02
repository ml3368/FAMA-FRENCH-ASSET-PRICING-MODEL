import pandas as pd
import pandas_datareader.data as web

def clean_columns(df):
    """Columns have mulitple rows of names. We will flatten 'multi-index' columns and clean column names."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    return df

def get_ff5_monthly(start_date="2020-01-01"):
    """Fetch and format Fama-French 5 Factor monthly data."""
    ff_dict = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', start=start_date)
    ff_df = ff_dict[0] 
    ff_df.index = ff_df.index.to_timestamp(how='end').normalize()
    return ff_df / 100.0 

#You need to set up the FF data in line with desired data
def merge_with_ff5(stock_rets_df, tickers, start_date="2016-01-01"):
    """Merge notebook stock data with background FF5 data and calculate excess returns."""
    ff5 = get_ff5_monthly(start_date)
    
    # Inner join aligns the dates perfectly
    merged_df = stock_rets_df.join(ff5, how='inner')
    
    # Calculate excess return for each ticker provided
    for ticker in tickers:
        merged_df[f'{ticker}_Excess'] = merged_df[ticker] - merged_df['RF']
        
    return merged_df