import pandas as pd
def cat_dist(df, show_rows=10, format_cols=True):
    """
    Display the top values by count for each variable in a data frame.

    As an initial step in exploring a data set it is usually good to know
    about how the variables are distributed, and the top ones.
    Metrics shown:
    * top values by count
    * percenage of each value of the total
    * cumulative percentage of values
    * number of unique values
    * the percenage of the total of the top values

    :param df: a data frame
    :param show_rows: the number of values to show, default: 10
    :param format_cols: whether or no to format the values for easy reading
    :return: no return value, only print the values for exploration

    """
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
