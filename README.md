<<<<<<< HEAD
Здесь укажите имя вашего бакета: "s3-student-mle-20241125-59b9e9f709"

part1_airflow/dags//predict_price этот DAG создаётнабор данных в таблице predict_price, объединяя данные из flats и buildings и сохраняя результат в Postgres для дальнейшего анализа или использования

part1_airflow/dags/predict_price_clear.py - ETL-процесс (Extract → Transform → Load) для очистки и сохранения набора данных о недвижимости, с последующей загрузкой результата в отдельную таблицу predict_price_clean

Для запуска airflow выполните команду:
docker compose up --build 

Результаты модели - part2_dvc/cv_results/cv_res.json

dvc pipline - /home/mle-user/mle_projects/mle-project-sprint-1-v001/part2_dvc
=======
# mle-project-sprint1-v001

Это репозиторий-шаблон для проекта Яндекс Практикума спринта №1.
Описание проекта смотрите на платформе.
>>>>>>> c3464f1 (Update readme)

<<<<<<< HEAD
=======
Здесь укажите имя вашего бакета: "s3-student-mle-20241125-59b9e9f709"


part1_airflow/dags//predict_price этот DAG создаётнабор данных в таблице predict_price, объединяя данные из flats и buildings и сохраняя результат в Postgres для дальнейшего анализа или использования

part1_airflow/dags/predict_price_clear.py - ETL-процесс (Extract → Transform → Load) для очистки и сохранения набора данных о недвижимости, с последующей загрузкой результата в отдельную таблицу predict_price_clean

Для запуска airflow выполните команду:
docker compose up --build 

Результаты модели - part2_dvc/cv_results/cv_res.json

dvc pipline - /home/mle-user/mle_projects/mle-project-sprint-1-v001/part2_dvc

>>>>>>> 64d9068 (Добавлен dvc pipline - mvp)
