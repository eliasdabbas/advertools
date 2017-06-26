import pandas as pd
def cat_dist(df, show_rows=10, format_cols=True):
    for i in df:
        print('Distribution of ', i,sep='')
        print('--------------------')
        df_dist = pd.DataFrame({
            'count': df[i].value_counts(),
            'perc' : df[i].value_counts(normalize=True)
        })
        df_dist['cum_perc'] = df_dist['perc'].cumsum()
        if format_cols:
            df_dist['count'] = ['{:,}'.format(x) for x in df_dist['count']]
            df_dist['perc'] = ['{:.2%}'.format(x) for x in df_dist['perc']]
            df_dist['cum_perc'] = ['{:.2%}'.format(x) for x in df_dist['cum_perc']]
        print(df_dist.iloc[:show_rows,:])
        print(' Categories of ', i, ': ', '{:,}'.format(len(df_dist)),sep='')
        if show_rows >= len(df_dist):
            print(' Showing 100% of categories')
        else:
            print(' Showing ', '{:.2%}'.format(show_rows / len(df_dist)),
                  ' of categories', sep='')
        print()
        print('====================')
        print()
    return None
