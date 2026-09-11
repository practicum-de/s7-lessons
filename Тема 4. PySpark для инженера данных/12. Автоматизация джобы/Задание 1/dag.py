"""Заготовка DAG. Создайте DAG и задачу запуска джобы из этого урока."""

import datetime
import os

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# TODO: настройте окружение Spark и Hadoop согласно уроку.
# TODO: задайте параметры DAG, операторы, аргументы джоб и зависимости.
# Используйте свои пути и логин. Сохраните задачи из предыдущих уроков,
# если они требуются по условию текущего задания.
dag = None
