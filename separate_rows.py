import pandas as pd


def separate_rows(df, col, sep=' '):
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
