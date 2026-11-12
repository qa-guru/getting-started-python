"""Генерация уникальных пользователей и загрузка кредов из окружения.

Пароль существующего пользователя не хранится в исходном коде —
креды заранее созданного на стенде аккаунта берутся из окружения.
"""
import os
import uuid

from test_data.consts.users import (
    PASSWORD_LENGTH,
    USERNAME_PREFIX,
    USERNAME_SUFFIX_LENGTH,
)
from test_data.users import MissingTestDataError, UserCredentials

ENV_USERNAME = "EXISTING_USERNAME"
ENV_PASSWORD = "EXISTING_PASSWORD"


def unique_username() -> str:
    return f"{USERNAME_PREFIX}{uuid.uuid4().hex[:USERNAME_SUFFIX_LENGTH]}"


def unique_password() -> str:
    return uuid.uuid4().hex[:PASSWORD_LENGTH]


def unique_user() -> UserCredentials:
    """Сгенерировать уникального пользователя (на стенде не создан)."""
    return UserCredentials(username=unique_username(), password=unique_password())


def load_existing_user(env=None) -> UserCredentials:
    """Загрузить креды существующего пользователя из окружения.

    env — mapping переменных окружения, по умолчанию os.environ.
    Бросает MissingTestDataError с указанием недостающих переменных.
    """
    env = os.environ if env is None else env
    username = env.get(ENV_USERNAME, "").strip()
    password = env.get(ENV_PASSWORD, "").strip()
    missing = [
        name
        for name, value in ((ENV_USERNAME, username), (ENV_PASSWORD, password))
        if not value
    ]
    if missing:
        raise MissingTestDataError(
            f"Не заданы обязательные переменные окружения: {', '.join(missing)}. "
            "Тесты, которым нужен существующий пользователь (логин, логаут, "
            "занятое имя при регистрации), требуют заранее созданного на стенде "
            f"аккаунта. Задай {ENV_USERNAME} и {ENV_PASSWORD} в .env или в shell."
        )
    return UserCredentials(username=username, password=password)
