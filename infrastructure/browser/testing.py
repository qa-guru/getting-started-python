"""Создание тестовых экземпляров Settings для unit-проверок."""
from settings import Settings
from test_data.consts.browser import (
    TEST_AUTH_URL,
    TEST_BASE_URL,
    TEST_BROWSER,
    TEST_TIMEOUT_S,
)


def make_test_settings(**overrides) -> Settings:
    """Settings со значениями по умолчанию, безопасными для unit-тестов.

    Любое поле можно переопределить через именованные аргументы.
    """
    base = dict(
        base_url=TEST_BASE_URL,
        auth_url=TEST_AUTH_URL,
        timeout_s=TEST_TIMEOUT_S,
        browser=TEST_BROWSER,
        browser_version="",
        headless=True,
        remote_url="",
        remote_requested=False,
    )
    base.update(overrides)
    return Settings(**base)
