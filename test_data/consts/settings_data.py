"""Фиксированные входные и ожидаемые данные tests/unit/test_settings.py.

Env-наборы обёрнуты в MappingProxyType и неизменяемы: тесты не разделяют
изменяемое состояние. Имена переменных окружения внутри словарей —
это входные данные тестируемого парсера `settings.load_settings`,
а не перенос самих настроек.
"""
from types import MappingProxyType

from settings import Settings

# --- Входные env-наборы (read-only) ---
EMPTY_ENV = MappingProxyType({})
ENV_BROWSER_FIREFOX = MappingProxyType({"BROWSER": "firefox"})
ENV_BROWSER_CHROMIUM = MappingProxyType({"BROWSER": "chromium"})
ENV_BVERSION_120 = MappingProxyType({"BROWSER_VERSION": "120"})
ENV_HEADLESS_FALSE = MappingProxyType({"HEADLESS": "false"})
ENV_HEADLESS_TRUE = MappingProxyType({"HEADLESS": "true"})
ENV_URLS_TRAILING_SLASH = MappingProxyType({
    "BASE_URL": "https://app.example/",
    "AUTH_URL": "https://auth.example/",
})
ENV_REMOTE_URL_TRAILING_SLASH = MappingProxyType({
    "SELENIUM_REMOTE_URL": "http://grid:4444/wd/hub/",
})
ENV_REMOTE_WITHOUT_URL = MappingProxyType({"SELENIUM_REMOTE": "true"})
ENV_TIMEOUT_ZERO = MappingProxyType({"TIMEOUT_S": "0"})
ENV_TIMEOUT_NON_NUMERIC = MappingProxyType({"TIMEOUT_S": "abc"})

# --- Входные значения ---
CLI_BROWSER_CHROME = "chrome"
CLI_BROWSER_CHROMIUM = "chromium"
CLI_BVERSION_121 = "121"
UNSUPPORTED_BROWSER = "opera"
ENV_BROWSER_UNSUPPORTED = MappingProxyType({"BROWSER": UNSUPPORTED_BROWSER})

# --- Ожидаемые значения ---
EXPECTED_DEFAULT_SETTINGS = Settings(
    base_url="https://niffler.qa.guru",
    auth_url="https://auth.niffler.qa.guru",
    timeout_s=10,
    browser="chrome",
    browser_version="",
    headless=True,
    remote_url="",
    remote_requested=False,
)
EXPECTED_BROWSER_CHROME = "chrome"
EXPECTED_BROWSER_FIREFOX = "firefox"
EXPECTED_BVERSION_120 = "120"
EXPECTED_BASE_URL_NO_SLASH = "https://app.example"
EXPECTED_AUTH_URL_NO_SLASH = "https://auth.example"
EXPECTED_REMOTE_URL_NO_SLASH = "http://grid:4444/wd/hub"

# --- Фрагменты сообщений об ошибках для pytest.raises(match=...) ---
ERROR_PATTERN_REMOTE_URL = "SELENIUM_REMOTE_URL"
ERROR_PATTERN_TIMEOUT = "TIMEOUT_S"
