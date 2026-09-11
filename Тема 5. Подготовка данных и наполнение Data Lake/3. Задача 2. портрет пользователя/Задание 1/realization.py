"""Заготовка решения. Замените TODO своим кодом перед отправкой."""

import datetime

import pyspark.sql.functions as F
from pyspark.sql.window import Window


def input_event_paths(date, depth):
    # TODO: подготовьте пути к событиям.
    raise NotImplementedError("Дополните решение по условию задания")


def tag_tops(date, depth, spark):
    # TODO: рассчитайте топ тегов публикаций по условию.
    raise NotImplementedError("Дополните решение по условию задания")
