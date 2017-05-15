import pandas as pd


def separate_rows(df, col, sep=' '):
    """
    Separate cells in a certain column if they contain a certain 
    character or string. 
    :param df: pd.DataFrame to to separate
    :param col: column name to separate rows
    :param sep: separator character(s) where you want rows to 
    be separated
    :return: a new data frame with the specified values separated
    and retained in their original rows
    
    Examples
    --------
    
    In[1]: df = pd.DataFrame({
    'name': ['first', 'second', 'third'],
    'text': ['one,two', 'three,four', 'five,six']
    })
    adv.separate_rows(df, 'text', ',')
    Out[1]: 
         name   text
    0   first    one
    1   first    two
    2  second  three
    3  second   four
    4   third   five
    5   third    six

    
    """
    df = df.copy()
    output_col = col
    temp_df = df[col].str.split(sep, expand=True)
    new_df = pd.DataFrame()
    temp_df.columns = [str(x) for x in temp_df.columns]
    for i in temp_df.columns:
        df[output_col] = temp_df.loc[:, i]
        new_df = new_df.append(df)
    new_df = new_df.sort_index()
    new_df = new_df.dropna().reset_index(drop=True)
    return new_df

