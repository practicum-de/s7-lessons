"""Заготовка решения. Замените TODO своим кодом перед отправкой."""

import sys
import datetime

import pyspark.sql.functions as F
from pyspark.sql.window import Window


def main():
    # TODO: получите аргументы командной строки в порядке из задания.
    date = None
    days_count = None
    suggested_cutoff = None
    base_input_path = None
    verified_tags_path = None
    base_output_path = None
    # TODO: создайте Spark-контекст, прочитайте данные и вычислите candidates.
    # TODO: сохраните результат в требуемую партицию.
    raise NotImplementedError("Соберите джобу из своего решения")


def find_candidates(messages, verified_tags, suggested_cutoff):
    # TODO: перенесите и параметризуйте свою обработку тегов.
    raise NotImplementedError("Дополните решение по условию задания")


if __name__ == "__main__":
    main()
