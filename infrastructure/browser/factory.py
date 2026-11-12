"""Создание и первичная настройка WebDriver по Settings."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from settings import Settings

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


def _build_options(s: Settings):
    if s.browser == "chrome":
        options = ChromeOptions()
        if s.headless:
            options.add_argument("--headless=new")
        for arg in (
            f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ):
            options.add_argument(arg)
    else:
        options = FirefoxOptions()
        if s.headless:
            options.add_argument("-headless")
        options.add_argument(f"-width={WINDOW_WIDTH}")
        options.add_argument(f"-height={WINDOW_HEIGHT}")
    if s.browser_version:
        options.browser_version = s.browser_version
    return options


def create_driver(s: Settings) -> WebDriver:
    """Создать Remote/Chrome/Firefox драйвер и применить базовую настройку.

    Ошибка обязательной настройки прерывает подготовку: созданный драйвер
    закрывается, а исходная ошибка передаётся вызывающему коду. Если
    закрытие тоже падает, вторичная ошибка добавляется к исходной
    через add_note и не подменяет её.
    """
    options = _build_options(s)

    if s.remote_url:
        drv = webdriver.Remote(command_executor=s.remote_url, options=options)
    elif s.browser == "chrome":
        drv = webdriver.Chrome(options=options)
    else:
        drv = webdriver.Firefox(options=options)

    try:
        drv.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    except Exception as setup_error:
        try:
            drv.quit()
        except Exception as quit_error:
            setup_error.add_note(
                f"Не удалось закрыть драйвер после сбоя настройки: {quit_error!r}"
            )
        raise
    return drv
