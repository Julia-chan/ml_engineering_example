import pandas as pd
import os
import warnings

from .common import invert_dict

# Columns can change order / add => we fix rule for renaming each column.
dict_for_leaf_humidity_columns = {
    ('Unnamed: 0_level_0', 'Дата / время'): 'datetime',
    ('Температура воздуха [°C]', 'ср.знач'): 'air_temp_mean',
    ('Температура воздуха [°C]', 'максимум'): 'air_temp_max',
    ('Температура воздуха [°C]', 'минимум'): 'air_temp_min',
    ('Точка росы [°C]', 'ср.знач'): 'dew_point_mean',
    ('Точка росы [°C]', 'минимум'): 'dew_point_min',
    ('Солнечная радиация [W/m2]', 'ср.знач'): 'solar_radiation_mean',
    ('VPD [kPa]', 'ср.знач'): 'VPD_mean',
    ('VPD [kPa]', 'минимум'): 'VPD_min',
    ('Влажность воздуха  [%]', 'ср.знач'): 'air_humidity_mean',
    ('Влажность воздуха  [%]', 'максимум'): 'air_humidity_max',
    ('Влажность воздуха  [%]', 'минимум'): 'air_humidity_min',
    ('Осадки [mm]', 'сумма'): 'precipitation',
    ('Влажность листа [минимум]', 'time'): 'leaf_humidity_min',
    ('Скорость ветра [m/s]', 'ср.знач'): 'wind_speed_mean',
    ('Скорость ветра [m/s]', 'максимум'): 'wind_speed_max',
    ('Влажность почвы [%]', 'ср.знач'): 'soil_humidity_mean',
    ('Температура почвы [°C]', 'ср.знач'): 'soil_temp_mean',
    ('Температура почвы [°C]', 'максимум'): 'soil_temp_max',
    ('Температура почвы [°C]', 'минимум'): 'soil_temp_min',
    ('Солнечная панель [mV]', 'последний'): 'solar_panel_last',
    ('АКБ [mV]', 'последний'): 'AKB_last',
    ('АКБ2 [mV]', 'последний'): 'AKB2_last',
    ('АКБ2 [mV]', 'Эталонная эвапотранспирация ET0 [mm]'): 'ETo'}

def check_columns_exist(pandas_df, list_of_columns):
    pd_columns_set = set(pandas_df.columns.to_list())
    check_columns_set = set(list_of_columns)
    
    if not pd_columns_set == check_columns_set:
        missed_columns = check_columns_set.difference(pd_columns_set)
        if len(missed_columns) > 0:
            raise RuntimeError(f'Missed columns : {missed_columns}')

def check_additional_columns(pandas_df, list_of_columns):
    additional_columns = pd_columns_set.difference(check_columns_set)
    if len(additional_columns) > 0:
        warning.warn(f'Have additional columns: {additional_columns}')
    return additional_columns

class InputLeafData:
    # Class, where we standartize processing of excel file from business and prevent common mistakes.
    
    def __init__(self, folder_path, input_file_name):
        self.folder_path = folder_path
        self.input_file_name = input_file_name
    
    def __load_file(self):
        self.data = pd.read_excel(os.path.join(self.folder_path, self.input_file_name), header=[0, 1])
        # Flatten Multiindex
        self.data.columns = self.data.columns.to_flat_index()
        check_columns_exist(self.data, list(dict_for_leaf_humidity_columns.keys()))
        self.data.rename(dict_for_leaf_humidity_columns, axis=1, inplace=True)
        
    def get_data(self):
        self.__load_file()
        return self.data
    
class OutputLeafData:
    # Class where we output standartized xlsx.
    
    def __init__(self, pandas_df, prediction_column='prediction'):
        self.pandas_df = pandas_df
        self.prediction_column = prediction_column
        self.__process_pandas_df()
        
    def __process_pandas_df(self):
        invert_dict_for_leaf_humidity_columns = invert_dict(dict_for_leaf_humidity_columns)
        invert_dict_for_leaf_humidity_columns[self.prediction_column] = ('Влажность листа [предск]', 'значение')
        check_columns_exist(self.pandas_df, list(invert_dict_for_leaf_humidity_columns.keys()) + [self.prediction_column])
        self.pandas_df = self.pandas_df.rename(invert_dict_for_leaf_humidity_columns, axis=1)
        self.pandas_df.columns = pd.MultiIndex.from_tuples(self.pandas_df.columns)
    
    def get_data(self):
        return self.pandas_df
    
    def write_to_file(self, folder_path, output_file_name):
        with pd.ExcelWriter(os.path.join(self.folder_path, self.input_file_name)) as writer:
            self.pandas_df.to_excel(writer)