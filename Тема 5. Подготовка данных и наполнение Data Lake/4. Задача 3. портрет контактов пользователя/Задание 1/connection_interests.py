"""Заготовка решения. Замените TODO своим кодом перед отправкой."""

import sys
import datetime

import pyspark.sql.functions as F
from pyspark.sql.window import Window


def main():
    # TODO: прочитайте шесть аргументов командной строки по условию.
    date = None
    days_count = None
    events_base_path = None
    interests_base_path = None
    verified_tags_path = None
    output_base_path = None

    # TODO: создайте Spark-контекст и прочитайте данные.
    # Сохраняйте эти имена: их использует статическая проверка.
    messages = None
    direct_messages = None
    posts = None
    interests = None
    subscriptions = None
    verified_tags = None
    contacts = None
    contact_interests = None
    subs_interests = None
    result = None
    # TODO: вызовите функции ниже и запишите result в партицию даты.
    raise NotImplementedError("Дополните чтение, обработку и запись данных")


def input_event_paths(base_path, date, depth):
    # TODO: сформируйте пути за заданное окно дат.
    raise NotImplementedError("Дополните решение по условию задания")


def get_contacts(direct_messages):
    # TODO: постройте контакты пользователей из личных сообщений.
    raise NotImplementedError("Дополните решение по условию задания")


def get_contact_interests(contacts, interests):
    # TODO: рассчитайте интересы контактов по условию.
    raise NotImplementedError("Дополните решение по условию задания")


def get_subs_interests(posts, subscriptions, verified_tags):
    # TODO: рассчитайте интересы по подпискам и верифицированным тегам.
    raise NotImplementedError("Дополните решение по условию задания")


def join_result(contact_interests, subs_interests):
    # TODO: объедините результаты в итоговый портрет.
    raise NotImplementedError("Дополните решение по условию задания")


def tag_columns(reaction):
    # TODO: подготовьте названия колонок для типа реакции.
    raise NotImplementedError("Дополните решение по условию задания")


if __name__ == "__main__":
    main()
