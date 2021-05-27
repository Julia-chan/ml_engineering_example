import argparse
import yaml
import os

from sklearn.pipeline import Pipeline

from source.input_output import InputLeafData
from source.features import AddMonth, AddDay, AddHour, DropColumns
from source.preprocess import DropOuliers

def features(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    i_o_folder = os.path.join(config['base']['repo_path'], config['load_data']['folder'])
    
    station_data = InputLeafData(
        i_o_folder, 
        config['load_data']['file']).get_data()
    
    # Features Generator
    features_enineering = [
        ('add_month', AddMonth()),
        ('add_day', AddDay()),
        ('add_hour', AddHour()),
        # Add here as many feature generating classes as you want
        ('drop_columns', DropColumns(config['fen']['features_to_drop']))
    ]
    
    # Preprocessing. Different from features generator => class may have fit method.
    features_preprocessing = []
    for i in config['preprocessing']['preprocess_outliers']:
        features_preprocessing.append((i, DropOuliers(i)))
    
    features_pipeline = Pipeline(features_enineering + features_preprocessing)
    
    station_data = features_pipeline.fit_transform(station_data)
    station_data.to_csv(os.path.join(i_o_folder, config['output']['features']), index=False)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    features(config_path=args.config)