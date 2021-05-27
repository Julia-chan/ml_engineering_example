from sklearn.base import BaseEstimator, TransformerMixin


def drop_columns(df, columns_to_drop):
    return df.drop(columns_to_drop, axis=1)

def drop_row_less_than_including(df, column_name, min_value):
    return df[df[column_name] > min_value]

def drop_row_strictly_less_than(df, column_name, min_value):
    return df[df[column_name] >= min_value]

def drop_row_greater_than_including(df, column_name, max_value):
    return df[df[column_name] < max_value]

def drop_row_strictly_greater_than(df, column_name, max_value):
    return df[df[column_name] <= max_value]

class DropOuliers(BaseEstimator, TransformerMixin):
    """Drop outliers using quantile for column.
    
    Parameters
    ----------
    column: str
        Column of Dataframe to count quantile and remove outliers.
    precentage_of_outliers: float
        Prc. of outliers to remove simmetricaly.
    """
    
    def __init__(self, column, percentage_of_outliers=0.05):
        self.column = column
        self.percentage_of_outliers = percentage_of_outliers
    
    def fit(self, X):
        self.lower = X[self.column].quantile(self.percentage_of_outliers / 2)
        self.maximum = X[self.column].quantile(1 - self.percentage_of_outliers / 2)
        return self
    
    def transform(self, X, y=None):
        self.X_copy = X.copy()
        self.X_copy = drop_row_strictly_less_than(self.X_copy, self.column, self.lower)
        self.X_copy = drop_row_strictly_greater_than(self.X_copy, self.column, self.maximum)
        return self.X_copy
        