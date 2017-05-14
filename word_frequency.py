import pandas as pd
from collections import Counter

def word_frequency(df, text_col=None, num_col=None,
                   sep=' ', rm_words=None):
    df = df[[text_col, num_col]]
    df_copy = df.copy()
    df[text_col] = df[text_col].str.lower()
    split_df = df[text_col].str.split(sep,expand=True)
    df_split_df = pd.concat([df,split_df],axis=1)
    df_melt =  pd.melt(df_split_df, id_vars=[num_col, text_col])
    df_melt = df_melt[pd.notnull(df_melt['value'])]
    if rm_words:
        df_melt = df_melt[[word not in rm_words for word in df_melt['value']]]

    wtd_wrds = df_melt.groupby('value')
    wtd_wrds = wtd_wrds.sum()
    wtd_wrds = wtd_wrds.sort_values(num_col, ascending=False)
    wtd_wrds.index.name = 'word'

    text_vec = df[text_col].str.cat(sep=sep).split()
    text_counter = Counter(text_vec)

    abs_wrds = pd.DataFrame.from_dict(text_counter, orient='index')
    abs_wrds = abs_wrds.sort_values(0,ascending=False)
    abs_wrds.index.name = 'word'

    wtd_abs = pd.merge(wtd_wrds,abs_wrds,left_index=True, right_index=True)
    wtd_freq = 'wtd_' + str(num_col)
    abs_freq = 'abs_' + str(num_col)
    wtd_abs.columns = [wtd_freq, abs_freq]
    wtd_abs['word'] = wtd_abs.index
    wtd_abs.index = range(len(wtd_abs))

    ratio_col = 'wtd_abs_ratio'
    wtd_abs[ratio_col] = wtd_abs[wtd_freq] / wtd_abs[abs_freq]
    wtd_abs = wtd_abs[['word', abs_freq, wtd_freq, ratio_col]]
    wtd_abs = wtd_abs.sort_values(wtd_freq, ascending=False)
    wtd_abs.index = range(len(wtd_abs))
    df = df.sort_values(num_col, ascending=False)
    df.index = range(len(df))
    final = pd.concat([wtd_abs, df_copy],axis=1)
    return final
