import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class AddDatetimeColumn(BaseEstimator, TransformerMixin):
    """
    Abstract class for processing datetime column in str. Both '2020-08-31 19:00:00' and
    '2020-08-31' formats are egible.
    """

    def __init__(self, datetime_str_column='datetime'):
        self.datetime_str_column = datetime_str_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, output_column='num'):
        pass

    
class AddDay(AddDatetimeColumn):
    """Adds month number to df with datetime column in str
    
    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({'datetime': {0: '2020-08-31 19:00:00',
    >>>   1: '2020-08-31 18:00:00',
    >>>   2: '2020-08-31 17:00:00',
    >>>   3: '2020-08-31 16:00:00',
    >>>   4: '2020-08-31 15:00:00'}})
    >>> AddDay().fit_transform(x)
    
    |    | datetime   |   day_n |
    |---:|:-----------|--------:|
    |  0 | 2020-08-31 |      31 |
    |  1 | 2020-08-31 |      31 |
    |  2 | 2020-08-31 |      31 |
    |  3 | 2020-08-31 |      31 |
    |  4 | 2020-08-31 |      31 |
    """

    def transform(self, X, y=None, output_column='day_n'):
        X_copy = X.copy()
        X_copy[output_column] = pd.to_datetime(X_copy[self.datetime_str_column]).dt.day
        return X_copy

    
class AddMonth(AddDatetimeColumn):
    """Adds month number to df with datetime column in str
    
    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({'datetime': {0: '2020-08-31 19:00:00',
    >>>   1: '2020-08-31 18:00:00',
    >>>   2: '2020-08-31 17:00:00',
    >>>   3: '2020-08-31 16:00:00',
    >>>   4: '2020-08-31 15:00:00'}})
    >>> AddMonth().fit_transform(x)
    
    |    | datetime            |   month_n |
    |---:|:--------------------|----------:|
    |  0 | 2020-08-31 19:00:00 |         8 |
    |  1 | 2020-08-31 18:00:00 |         8 |
    |  2 | 2020-08-31 17:00:00 |         8 |
    |  3 | 2020-08-31 16:00:00 |         8 |
    |  4 | 2020-08-31 15:00:00 |         8 |
    """

    def transform(self, X, y=None, output_column='month_n'):
        X_copy = X.copy()
        X_copy[output_column] = pd.to_datetime(X_copy[self.datetime_str_column]).dt.month
        return X_copy

    
class AddHour(AddDatetimeColumn):
    """Adds month number to df with datetime column in str
    
      
    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({'datetime': {0: '2020-08-31 19:00:00',
    >>>   1: '2020-08-31 18:00:00',
    >>>   2: '2020-08-31 17:00:00',
    >>>   3: '2020-08-31 16:00:00',
    >>>   4: '2020-08-31 15:00:00'}})
    >>> AddHour().fit_transform(x)
    
    |    | datetime            |   hour_n |
    |---:|:--------------------|---------:|
    |  0 | 2020-08-31 19:00:00 |       19 |
    |  1 | 2020-08-31 18:00:00 |       18 |
    |  2 | 2020-08-31 17:00:00 |       17 |
    |  3 | 2020-08-31 16:00:00 |       16 |
    |  4 | 2020-08-31 15:00:00 |       15 |
    """

    def transform(self, X, y=None, output_column='hour_n'):
        X_copy = X.copy()
        X_copy[output_column] = pd.to_datetime(X_copy[self.datetime_str_column]).dt.hour
        return X_copy