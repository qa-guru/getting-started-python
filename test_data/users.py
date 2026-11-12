"""Модель учётных данных и ошибки тестовых данных пользователей.

Генерация уникальных пользователей и загрузка кредов существующего
пользователя — test_data/utils/users.py.
"""
from dataclasses import dataclass


class MissingTestDataError(RuntimeError):
    """Не хватает обязательных тестовых данных (например, кредов)."""


@dataclass(frozen=True)
class UserCredentials:
    username: str
    password: str
