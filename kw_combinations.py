import pandas as pd

from advertools import expand

def kw_combinations(data_dict, combos, nesting=None,
                    match_types=['Exact','Phrase']):
    assert isinstance(data_dict, dict)
    assert [x in data_dict.keys() for x in nesting]
    assert isinstance(combos, list)
    assert all([isinstance(x,list) for x in combos])
    matches = ['Exact','Phrase','Broad', 'Negative Broad',
               'Negative Exact','Negative Phrase']
    match_types = [x.title() for x in match_types]
    if not all([x in matches for x in match_types]):
        raise ValueError('Please make sure you choose match types from', matches)
    df = expand(data_dict, nesting=nesting)

    for c in combos:
       col = '_'.join(c)
       df[col] = df[c[0]].str.cat([df[x] for x in df[c[1:]]],sep=' ')

    value_vars = [col for col in df.columns if not col in data_dict.keys()]
    df = pd.melt(df, id_vars=nesting,
                 value_vars=value_vars,
                 var_name='Labels',
                 value_name='Keyword')
    df['Labels'] = df['Labels'].str.replace('_', ';')
    df['Labels'] = df['Labels'].str.title()
    df = df.drop_duplicates()

    df_copy = df.copy()
    df['Criterion Type'] = match_types[0]
    for i in range(1, len(match_types)):
        df_copy['Criterion Type'] = match_types[i]
        df = pd.concat([df, df_copy], ignore_index=True)
    df = df.sort_values(nesting + ['Keyword', 'Criterion Type'])
    df = df.reset_index(drop=True)
    df['Keyword'] = df['Keyword'].str.lower()
    df.index = range(len(df))
    return df
