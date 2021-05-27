def month_hardcode_split(pandas_df, month_column='month_n'):
    max_month = pandas_df[month_column].max()
    pandas_df_copy = pandas_df.copy()
    train = pandas_df_copy[pandas_df_copy[month_column] < max_month]
    test = pandas_df_copy[pandas_df_copy[month_column] == max_month]
    return train, test