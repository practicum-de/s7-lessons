"""Заготовка решения. Замените TODO своим кодом перед отправкой."""

import sys
import datetime

import pyspark.sql.functions as F
from pyspark.sql.window import Window


def main():
    # TODO: прочитайте аргументы командной строки из задания.
    date = None
    days_count = None
    events_base_path = None
    output_base_path = None
    # TODO: подготовьте Spark, прочитайте публикации и реакции, сохраните result.
    raise NotImplementedError("Соберите джобу из своего решения")


def input_event_paths(base_path, date, depth):
    # TODO: адаптируйте своё решение из предыдущих заданий.
    raise NotImplementedError("Дополните решение по условию задания")


def calculate_user_interests(posts_part, posts_all, reactions):
    # TODO: адаптируйте своё решение из предыдущих заданий.
    raise NotImplementedError("Дополните решение по условию задания")


def tag_tops(posts):
    # TODO: адаптируйте своё решение из предыдущих заданий.
    raise NotImplementedError("Дополните решение по условию задания")


def reaction_tag_tops(posts_all, reactions):
    # TODO: адаптируйте своё решение из предыдущих заданий.
    raise NotImplementedError("Дополните решение по условию задания")


if __name__ == "__main__":
    main()
