# scripts/evaluate.py

import pandas as pd
from sklearn.model_selection import KFold, cross_validate
import joblib
import json
import yaml
import os

# оценка качества модели
def evaluate_model():
	# прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml','r') as fd:
        params = yaml.safe_load(fd)

    data = pd.read_csv('data/initial_data.csv')
    data = data.drop(columns=['id', 'building_id'], errors='ignore')

    # Разделение данных на X и y
    X = data.drop(columns=params['target_col'])
    y = data[params['target_col']]

	# загрузите результат прошлого шага: fitted_model.pkl
    with open('models/fitted_model.pkl', 'rb') as fd:
        model = joblib.load(fd)

	# реализуйте основную логику шага с использованием прочтённых гиперпараметров
    cv_strategy = KFold(n_splits=params['n_splits'], shuffle=True, random_state=params.get('random_state', 42))
    cv_res = cross_validate(
        model,
        X,
        y,
        cv=cv_strategy,
        n_jobs=params['n_jobs'],
        scoring=params['metrics']
        )

    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3) 

    os.makedirs('cv_results', exist_ok=True)
    
    with open('cv_results/cv_res.json', 'w') as f:
        json.dump(cv_res, f, indent=4)
    

if __name__ == '__main__':
	evaluate_model()

