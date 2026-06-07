# Загрузка данных в HDFS

## Задание
Нормализация датасетов и загрузка в HDFS в формате Parquet.

## Использование
1. Создать виртуальное окружение
2. Установить зависимости: `pip install -r requirements.txt`
3. Запустить: `python process_data.py`

## Результат
- events_normalized.parquet
- accidents_normalized.parquet

## Загрузка в HDFS
hdfs dfs -mkdir -p /user/Админ/hdfs_data
hdfs dfs -put data/events_normalized.parquet /user/Админ/hdfs_data/
hdfs dfs -put data/accidents_normalized.parquet /user/Админ/hdfs_data/