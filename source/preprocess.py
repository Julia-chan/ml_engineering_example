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

def quart_range(data, koef):
    """Функция расчета межквантильного расстояния и крайних
    точек по заданным точкам и коэффициенту
    """
    #расчет квантилей 25% и 75% 
    lower_quartile = data.quantile(0.25)
    upper_quartile = data.quantile(0.75)
    #Расчет межквантильного интервала
    iqr = upper_quartile-lower_quartile
    #Расчет "усов"
    upper_quartile = data[data<=upper_quartile+koef*iqr].max()
    lower_quartile = data[data>=lower_quartile-koef*iqr].min()
    return lower_quartile, upper_quartile

class DropOuliers(BaseEstimator, TransformerMixin):
    """Drop outliers using quantile for column.
    
    Parameters
    ----------
    column: str
        Column of Dataframe to count quantile and remove outliers.
    """
    
    def __init__(self, column, koeff=3):
        self.column = column
        self.koeff = koeff
    
    def fit(self, X):
        lower_q = X[self.column].quantile(0.25)
        upper_q = X[self.column].quantile(0.75)
        iqr = upper_q - lower_q
        self.maximum = upper_q + (self.koeff * iqr)
        self.lower = lower_q - (self.koeff * iqr)
        return self
    
    def transform(self, X, y=None):
        self.X_copy = X.copy()
        self.X_copy = drop_row_strictly_less_than(self.X_copy, self.column, self.lower)
        self.X_copy = drop_row_strictly_greater_than(self.X_copy, self.column, self.maximum)
        return self.X_copy

class BinarizeColumn:
    """Warning: Inlace Binarizer."""
    def __init__(self, column):
        self.column = column
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_copy = X.copy()
        X_copy[self.column] = X_copy[self.column].astype(int).apply(lambda x: 1 if x > 0 else 0)
        return X_copy

class Selector:
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_copy = X.copy()
        return X_copy[self.columns]