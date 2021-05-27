import pandas as pd
from sklearn.pipeline import Pipeline
import yaml
import os
import catboost as ctb
import joblib

from source.preprocess import BinarizeColumn, Selector
from source.validation import month_hardcode_split
from source.pipeline import features, train_model

def train(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    i_o_folder = os.path.join(config['base']['repo_path'], config['load_data']['folder'])
    
    target_column = config['train']['target_column']
    output_column = config['train']['output_column']
    select_columns = config['train']['select'] + [target_column]
    
    station_data = pd.read_csv(os.path.join(i_o_folder, config['output']['features']))
    train, test = month_hardcode_split(station_data)
    
    pre_model_pipeline = Pipeline([
        ('binarize_target', BinarizeColumn(target_column)),
        ('select_columns', Selector(select_columns))
    ])
    
    train = pre_model_pipeline.fit_transform(train)
    test = pre_model_pipeline.fit_transform(test)
    
    params = config['train']['catboost']
    
    clf = ctb.CatBoostClassifier(
        iterations=params['iterations'], 
        cat_features=params['categorical']
    )
    
    clf.fit(train.drop(target_column, axis=1), train[target_column])
    
    ## Metrics, Time based validation
    
    joblib.dump(clf, os.path.join(config['base']['repo_path'], config['output']['model']))

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    features(config_path=args.config)