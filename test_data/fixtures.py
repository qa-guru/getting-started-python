"""Фикстуры тестовых данных пользователей.

Подключение: `pytest_plugins = ["test_data.fixtures"]` в conftest.py.
"""
import pytest

from test_data.users import UserCredentials
from test_data.utils.users import load_existing_user, unique_user


@pytest.fixture(scope="session")
def existing_user() -> UserCredentials:
    """Существующий пользователь стенда — креды из env.

    При отсутствии переменных окружения бросает MissingTestDataError:
    тест помечается ошибкой подготовки с указанием, что именно задать.
    Общий аккаунт только читается: тесты не меняют его данные,
    и teardown для него не выполняется.
    """
    return load_existing_user()


@pytest.fixture
def new_user() -> UserCredentials:
    """Уникальные креды для сценариев регистрации.

    Генерация — на каждый тест. Зарегистрированные этими кредами
    пользователи не удаляются: на стенде нет подтверждённого
    механизма удаления пользователей, поэтому данные регистраций
    накапливаются.
    """
    return unique_user()
