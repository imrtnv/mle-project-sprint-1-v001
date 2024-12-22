import pendulum
from airflow.decorators import dag, task
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from steps.messages import send_telegram_success_message, send_telegram_failure_message


@dag(
    schedule_interval='@once',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
    tags=["ETL"]
)
def prepare_predict_price_clean_dataset():
    
    @task()
    def create_table() -> None:
        from sqlalchemy import (
        Table, MetaData, Column, Integer,Float, UniqueConstraint, inspect, Boolean
        )
        hook = PostgresHook('destination_db') 
        engine = hook.get_sqlalchemy_engine()

        metadata = MetaData()

        # Определение таблицы
        users_churn = Table(
            'predict_price_clean',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('floor_id', Integer, nullable=False),
            Column('floor', Float, nullable=True),
            Column('is_apartment', Boolean, nullable=True),
            Column('kitchen_area', Float, nullable=True),
            Column('living_area', Float, nullable=True),
            Column('rooms', Float, nullable=True),
            Column('studio', Boolean, nullable=True),
            Column('total_area', Float, nullable=True),
            Column('price', Float, nullable=True),
            Column('building_id', Float, nullable=True),
            Column('build_year', Float, nullable=True),
            Column('building_type_int', Float, nullable=True),
            Column('latitude', Float, nullable=True),
            Column('longitude', Float, nullable=True),
            Column('ceiling_height', Float, nullable=True),
            Column('flats_count', Float, nullable=True),
            Column('floors_total', Float, nullable=True),
            Column('has_elevator', Boolean, nullable=True),
            UniqueConstraint('floor_id', name='unique_floor_id_clean_constraint')
        )


        # Проверка на существование таблицы
        if not inspect(engine).has_table(users_churn.name):
            metadata.create_all(engine)  # Создание таблицы с использованием SQLAlchemy engine

        engine.dispose()  # Закрытие соединения
    
    @task()
    def extract(**kwargs):
        hook = PostgresHook('destination_db')  # Используем conn_id для источника
        conn = hook.get_conn()
        sql = """
        select *
        from predict_price
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        def remove_duplicates(data):
            feature_cols = data.columns.drop(['id','price','building_id']).tolist()
            is_duplicated_features = data.duplicated(subset=feature_cols, keep=False)
            data = data[~is_duplicated_features].reset_index(drop=True)
            return data 
     
        def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
            num_cols = df.select_dtypes(include=['float','int']).columns
            threshold = 1.5
            potential_outliers = pd.DataFrame(False, index=df.index, columns=num_cols)
    
            for col in num_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                margin = threshold * IQR
                lower = Q1 - margin
                upper = Q3 + margin
                potential_outliers[col] = ~df[col].between(lower, upper)
    
            outliers = potential_outliers.any(axis=1)
            df_cleaned = df[~outliers]
            return df_cleaned

        # Теперь вызываем наши функции последовательно
        df = remove_duplicates(df)
        df = remove_outliers(df)
        return df

        

    @task()
    def load(data: pd.DataFrame):
        hook = PostgresHook('destination_db')  # Используем conn_id для назначения
        hook.insert_rows(
            table="predict_price_clean",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['floor_id'],
            rows=data.values.tolist()
        )
    
    # Действия с DAG
    create_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)

prepare_predict_price_clean_dataset()