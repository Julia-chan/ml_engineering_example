from tabulate import tabulate

def invert_dict(dict_to_invert):
    """Invert Python dictionary.
    
     Examples
    --------
    >>> invert_dict({'key': 'value'})
    
    {'value': 'key'}
    """
    return {v: k for k, v in dict_to_invert.items()}

def print_df_as_markdown(df):
    """Use this for writing docstrings.
    
     Examples
    --------
    import pandas as pd
    x = pd.DataFrame({'column': ['value']})
    print_df_as_markdown(x)
    
    |    | column   |
    |---:|:---------|
    |  0 | value    |"""
    print(tabulate(df, tablefmt="pipe", headers="keys"))