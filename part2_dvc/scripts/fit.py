# scripts/fit.py

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
import yaml
import os
import joblib

# обучение модели
def fit_model():
    # Прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)

    # загрузите результат предыдущего шага: inital_data.csv
    data = pd.read_csv('data/initial_data.csv')

    # Удаление ненужных столбцов
    data = data.drop(columns=['id', 'building_id'], errors='ignore')

    # Уберём цель из data до определения признаков
    y = data['price']
    X = data.drop(columns='price')

    # Теперь определяем списки признаков без price
    bool_features = X.select_dtypes(include='bool')
    num_features = X.select_dtypes(include='float64')
    

    # Создаем колонко-трансформер
    preprocessor = ColumnTransformer(
        [
            ('binary', OneHotEncoder(drop=params['one_hot_drop']), bool_features.columns.tolist()),
            ('num', StandardScaler(), num_features.columns.tolist())
        ],
        remainder='drop',
        verbose_feature_names_out=False
    )

    # Инициализация модели с параметрами
    model = LinearRegression()

    # Объединяем препроцессор и модель в pipeline
    pipeline = Pipeline(
        [
            ('preprocessor', preprocessor),
            ('model', model)
        ]
    )

    # Обучаем модель (предполагается, что в data уже есть столбец 'target')
    pipeline.fit(X, y)

    # Создаем директорию для модели, если ее нет
    os.makedirs('models', exist_ok=True)

    # Сохраняем обученную модель
    joblib.dump(pipeline, 'models/fitted_model.pkl')


if __name__ == '__main__':
    fit_model()