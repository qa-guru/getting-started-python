"""Настройки запуска UI-тестов.

Единая точка сбора конфигурации. Приоритет источников:
CLI-опция > переменная окружения > значение по умолчанию.
"""
import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://niffler.qa.guru"
DEFAULT_AUTH_URL = "https://auth.niffler.qa.guru"
DEFAULT_TIMEOUT_S = 10
DEFAULT_BROWSER = "chrome"

SUPPORTED_BROWSERS = ("chrome", "firefox")
BROWSER_ALIASES = {"chromium": "chrome"}

_TRUE_VALUES = ("1", "true", "yes")


@dataclass(frozen=True)
class Settings:
    base_url: str
    auth_url: str
    timeout_s: float
    browser: str
    browser_version: str
    headless: bool
    remote_url: str
    remote_requested: bool


def _env_flag(env, name: str, default: bool = False) -> bool:
    raw = env.get(name)
    return default if raw is None else raw.strip().lower() in _TRUE_VALUES


def load_settings(browser_option=None, bversion_option=None, env=None) -> Settings:
    """Собрать и проверить настройки.

    browser_option / bversion_option — значения CLI-опций pytest
    (None, если флаг не передан). env — mapping переменных окружения,
    по умолчанию os.environ (подставляется dict в тестах).
    """
    env = os.environ if env is None else env

    browser_raw = (browser_option or env.get("BROWSER") or DEFAULT_BROWSER).strip().lower()
    browser = BROWSER_ALIASES.get(browser_raw, browser_raw)
    if browser not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"Unsupported browser {browser_raw!r}. "
            f"Supported: {', '.join(SUPPORTED_BROWSERS)} "
            f"(aliases: {', '.join(f'{k}={v}' for k, v in BROWSER_ALIASES.items())})."
        )

    base_url = env.get("BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")
    auth_url = env.get("AUTH_URL", DEFAULT_AUTH_URL).strip().rstrip("/")
    if not base_url:
        raise ValueError("BASE_URL is empty.")
    if not auth_url:
        raise ValueError("AUTH_URL is empty.")

    try:
        timeout_s = float(env.get("TIMEOUT_S", DEFAULT_TIMEOUT_S))
    except (TypeError, ValueError):
        raise ValueError(f"TIMEOUT_S must be a number, got {env.get('TIMEOUT_S')!r}.")
    if timeout_s <= 0:
        raise ValueError(f"TIMEOUT_S must be positive, got {timeout_s}.")

    remote_url = env.get("SELENIUM_REMOTE_URL", "").strip().rstrip("/")
    remote_requested = _env_flag(env, "SELENIUM_REMOTE")
    if remote_requested and not remote_url:
        raise ValueError(
            "Remote mode requested (SELENIUM_REMOTE=true) but SELENIUM_REMOTE_URL is not set. "
            "Provide the Selenium Grid/Selenoid URL, e.g. http://selenoid-host:4444/wd/hub."
        )

    return Settings(
        base_url=base_url,
        auth_url=auth_url,
        timeout_s=timeout_s,
        browser=browser,
        browser_version=(bversion_option or env.get("BROWSER_VERSION") or "").strip(),
        headless=_env_flag(env, "HEADLESS", default=True),
        remote_url=remote_url,
        remote_requested=remote_requested,
    )
