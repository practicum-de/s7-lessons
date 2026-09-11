"""Заготовка решения. Замените TODO своим кодом перед отправкой."""

import datetime

import pyspark.sql.functions as F
from pyspark.sql.window import Window


def input_event_paths(date, depth):
    # TODO: перенесите свою функцию подготовки путей.
    raise NotImplementedError("Дополните решение по условию задания")


def tag_tops(date, depth, spark):
    # TODO: перенесите своё решение для публикаций.
    raise NotImplementedError("Дополните решение по условию задания")


def reaction_tag_tops(date, depth, spark):
    # TODO: перенесите своё решение для реакций.
    raise NotImplementedError("Дополните решение по условию задания")


def calculate_user_interests(date, depth, spark):
    # TODO: объедините результаты в портрет пользователя.
    raise NotImplementedError("Дополните решение по условию задания")
