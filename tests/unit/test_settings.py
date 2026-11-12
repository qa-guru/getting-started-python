import allure
import pytest

from settings import load_settings
from test_data.consts.settings_data import (
    CLI_BROWSER_CHROME,
    CLI_BROWSER_CHROMIUM,
    CLI_BVERSION_121,
    EMPTY_ENV,
    ENV_BROWSER_CHROMIUM,
    ENV_BROWSER_FIREFOX,
    ENV_BROWSER_UNSUPPORTED,
    ENV_BVERSION_120,
    ENV_HEADLESS_FALSE,
    ENV_HEADLESS_TRUE,
    ENV_REMOTE_URL_TRAILING_SLASH,
    ENV_REMOTE_WITHOUT_URL,
    ENV_TIMEOUT_NON_NUMERIC,
    ENV_TIMEOUT_ZERO,
    ENV_URLS_TRAILING_SLASH,
    ERROR_PATTERN_REMOTE_URL,
    ERROR_PATTERN_TIMEOUT,
    EXPECTED_AUTH_URL_NO_SLASH,
    EXPECTED_BASE_URL_NO_SLASH,
    EXPECTED_BROWSER_CHROME,
    EXPECTED_BROWSER_FIREFOX,
    EXPECTED_BVERSION_120,
    EXPECTED_DEFAULT_SETTINGS,
    EXPECTED_REMOTE_URL_NO_SLASH,
    UNSUPPORTED_BROWSER,
)


@allure.epic("Инфраструктура")
@allure.feature("Настройки запуска")
class TestLoadSettings:

    @allure.story("Значения по умолчанию")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Настройки по умолчанию соответствуют стенду Niffler")
    def test_defaults(self):
        with allure.step("Загрузить настройки без переопределений"):
            loaded = load_settings(env=EMPTY_ENV)

        with allure.step("Проверить значения по умолчанию"):
            assert loaded == EXPECTED_DEFAULT_SETTINGS

    @allure.story("Приоритет источников")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Браузер выбирается по приоритету CLI > env > умолчание")
    def test_browser_priority_cli_over_env_over_default(self):
        with allure.step("Проверить приоритет CLI-опции над env"):
            assert load_settings(
                browser_option=CLI_BROWSER_CHROME, env=ENV_BROWSER_FIREFOX,
            ).browser == EXPECTED_BROWSER_CHROME

        with allure.step("Проверить приоритет env над значением по умолчанию"):
            assert load_settings(env=ENV_BROWSER_FIREFOX).browser == EXPECTED_BROWSER_FIREFOX
            assert load_settings(env=EMPTY_ENV).browser == EXPECTED_BROWSER_CHROME

    @allure.story("Приоритет источников")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Версия браузера выбирается по приоритету CLI > env")
    def test_bversion_priority_cli_over_env(self):
        with allure.step("Проверить приоритет CLI-опции версии над env"):
            assert load_settings(
                bversion_option=CLI_BVERSION_121, env=ENV_BVERSION_120,
            ).browser_version == CLI_BVERSION_121

        with allure.step("Проверить чтение версии из env"):
            assert load_settings(env=ENV_BVERSION_120).browser_version == EXPECTED_BVERSION_120

    @allure.story("Выбор браузера")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Алиас chromium приводится к chrome из CLI и env")
    def test_chromium_alias_from_cli_and_env(self):
        with allure.step("Проверить алиас chromium из CLI-опции"):
            assert load_settings(
                browser_option=CLI_BROWSER_CHROMIUM, env=EMPTY_ENV,
            ).browser == EXPECTED_BROWSER_CHROME

        with allure.step("Проверить алиас chromium из env"):
            assert load_settings(env=ENV_BROWSER_CHROMIUM).browser == EXPECTED_BROWSER_CHROME

    @allure.story("Выбор браузера")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Режим headless читается из env")
    def test_headless_flag(self):
        with allure.step("Проверить отключение headless через env"):
            assert load_settings(env=ENV_HEADLESS_FALSE).headless is False

        with allure.step("Проверить включение headless через env"):
            assert load_settings(env=ENV_HEADLESS_TRUE).headless is True

    @allure.story("Нормализация адресов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Завершающие слэши убираются из URL стендов")
    def test_urls_are_normalized(self):
        with allure.step("Загрузить настройки с завершающими слэшами в URL"):
            loaded = load_settings(env=ENV_URLS_TRAILING_SLASH)

        with allure.step("Проверить нормализацию URL"):
            assert loaded.base_url == EXPECTED_BASE_URL_NO_SLASH
            assert loaded.auth_url == EXPECTED_AUTH_URL_NO_SLASH

    @allure.story("Нормализация адресов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Завершающий слэш убирается из URL удалённого WebDriver")
    def test_remote_url_is_normalized(self):
        with allure.step("Загрузить remote URL с завершающим слэшем"):
            loaded = load_settings(env=ENV_REMOTE_URL_TRAILING_SLASH)

        with allure.step("Проверить нормализацию remote URL"):
            assert loaded.remote_url == EXPECTED_REMOTE_URL_NO_SLASH

    @allure.story("Валидация настроек")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Remote-режим без URL завершается ошибкой")
    def test_remote_requested_without_url_fails(self):
        with allure.step("Проверить ошибку remote-режима без URL"):
            with pytest.raises(ValueError, match=ERROR_PATTERN_REMOTE_URL):
                load_settings(env=ENV_REMOTE_WITHOUT_URL)

    @allure.story("Валидация настроек")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Неподдерживаемый браузер завершается ошибкой")
    def test_unsupported_browser_fails(self):
        with allure.step("Проверить ошибку неподдерживаемого браузера"):
            with pytest.raises(ValueError, match=UNSUPPORTED_BROWSER):
                load_settings(env=ENV_BROWSER_UNSUPPORTED)

    @allure.story("Валидация настроек")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Невалидный таймаут завершается ошибкой")
    def test_invalid_timeout_fails(self):
        with allure.step("Проверить ошибку нулевого таймаута"):
            with pytest.raises(ValueError, match=ERROR_PATTERN_TIMEOUT):
                load_settings(env=ENV_TIMEOUT_ZERO)

        with allure.step("Проверить ошибку нечислового таймаута"):
            with pytest.raises(ValueError, match=ERROR_PATTERN_TIMEOUT):
                load_settings(env=ENV_TIMEOUT_NON_NUMERIC)
