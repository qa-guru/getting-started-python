import allure
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import conftest
import infrastructure.browser.factory as browser_module
from infrastructure.browser.factory import create_driver
from infrastructure.browser.testing import make_test_settings
from test_data.consts.browser import (
    LOCAL_BROWSERS,
    QUIT_ERROR_TEXT,
    SETUP_ERROR_TEXT,
    TEST_ERROR_TEXT,
    TEST_REMOTE_URL,
)


class _FakeDriver:
    def __init__(self, set_size_error=None, quit_error=None):
        self.quit_called = False
        self.window_size = None
        self._set_size_error = set_size_error
        self._quit_error = quit_error

    def set_window_size(self, w, h):
        if self._set_size_error is not None:
            raise self._set_size_error
        self.window_size = (w, h)

    def quit(self):
        self.quit_called = True
        if self._quit_error is not None:
            raise self._quit_error


@allure.epic("Инфраструктура")
@allure.feature("Браузер и WebDriver")
class TestDriverFactory:

    @allure.story("Remote-режим")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("В remote-режиме создаётся Remote WebDriver")
    def test_remote_mode_uses_remote_driver(self, monkeypatch):
        with allure.step("Подменить создание драйверов"):
            calls = {}

            def fake_remote(command_executor, options):
                calls["executor"] = command_executor
                calls["options"] = options
                return _FakeDriver()

            monkeypatch.setattr(browser_module.webdriver, "Remote", fake_remote)
            monkeypatch.setattr(
                browser_module.webdriver, "Chrome",
                lambda **_: pytest.fail("local Chrome не должен создаваться в remote-режиме"),
            )

        with allure.step("Создать драйвер с remote URL"):
            drv = create_driver(make_test_settings(remote_url=TEST_REMOTE_URL))

        with allure.step("Проверить параметры Remote и настройку окна"):
            assert calls["executor"] == TEST_REMOTE_URL
            assert isinstance(calls["options"], ChromeOptions)
            assert drv.window_size == (browser_module.WINDOW_WIDTH, browser_module.WINDOW_HEIGHT)

    @allure.story("Локальный режим")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Локальный режим выбирает драйвер по имени браузера")
    def test_local_mode_picks_browser(self, monkeypatch):
        with allure.step("Подменить локальные драйверы Chrome и Firefox"):
            calls = []

            monkeypatch.setattr(
                browser_module.webdriver, "Chrome",
                lambda options=None: calls.append(("chrome", options)) or _FakeDriver(),
            )
            monkeypatch.setattr(
                browser_module.webdriver, "Firefox",
                lambda options=None: calls.append(("firefox", options)) or _FakeDriver(),
            )

        with allure.step("Создать драйверы для каждого локального браузера"):
            for name in LOCAL_BROWSERS:
                create_driver(make_test_settings(browser=name))

        with allure.step("Проверить выбор драйверов и типы опций"):
            assert [name for name, _ in calls] == list(LOCAL_BROWSERS)
            assert isinstance(calls[0][1], ChromeOptions)
            assert isinstance(calls[1][1], FirefoxOptions)


@allure.epic("Инфраструктура")
@allure.feature("Браузер и WebDriver")
class TestDriverFixture:

    @allure.story("Освобождение ресурсов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Драйвер закрывается при teardown фикстуры")
    def test_driver_fixture_quits_on_teardown(self, monkeypatch):
        with allure.step("Подменить создание драйвера"):
            fake = _FakeDriver()
            monkeypatch.setattr(conftest, "create_driver", lambda s: fake)

        with allure.step("Выполнить фикстуру driver и завершить её"):
            gen = conftest.driver.__wrapped__(make_test_settings())
            drv = next(gen)
            gen.close()

        with allure.step("Проверить получение и закрытие драйвера"):
            assert drv is fake
            assert fake.quit_called

    @allure.story("Освобождение ресурсов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Драйвер закрывается при падении теста")
    def test_driver_fixture_quits_if_test_raises(self, monkeypatch):
        with allure.step("Подменить создание драйвера"):
            fake = _FakeDriver()
            monkeypatch.setattr(conftest, "create_driver", lambda s: fake)

        with allure.step("Передать ошибку теста в фикстуру"):
            gen = conftest.driver.__wrapped__(make_test_settings())
            next(gen)
            with pytest.raises(RuntimeError, match=TEST_ERROR_TEXT):
                gen.throw(RuntimeError(TEST_ERROR_TEXT))

        with allure.step("Проверить, что драйвер закрыт"):
            assert fake.quit_called


@allure.epic("Инфраструктура")
@allure.feature("Браузер и WebDriver")
class TestDriverSetupErrors:

    @allure.story("Сбой обязательной настройки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ошибка настройки передаётся вызывающему коду, драйвер закрывается")
    def test_setup_error_propagates_and_driver_is_closed(self, monkeypatch):
        with allure.step("Подготовить драйвер, падающий на настройке окна"):
            setup_error = RuntimeError(SETUP_ERROR_TEXT)
            fake = _FakeDriver(set_size_error=setup_error)
            monkeypatch.setattr(
                browser_module.webdriver, "Chrome", lambda options=None: fake
            )

        with allure.step("Проверить, что ошибка настройки передана без подмены"):
            with pytest.raises(RuntimeError) as excinfo:
                create_driver(make_test_settings())
            assert excinfo.value is setup_error

        with allure.step("Проверить, что неподготовленный драйвер закрыт"):
            assert fake.quit_called

    @allure.story("Сбой обязательной настройки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ошибка закрытия драйвера не подменяет исходную причину")
    def test_quit_error_does_not_mask_setup_error(self, monkeypatch):
        with allure.step("Подготовить драйвер, падающий на настройке и закрытии"):
            setup_error = RuntimeError(SETUP_ERROR_TEXT)
            fake = _FakeDriver(
                set_size_error=setup_error,
                quit_error=RuntimeError(QUIT_ERROR_TEXT),
            )
            monkeypatch.setattr(
                browser_module.webdriver, "Chrome", lambda options=None: fake
            )

        with allure.step("Проверить, что вызывающий код получает исходную ошибку"):
            with pytest.raises(RuntimeError) as excinfo:
                create_driver(make_test_settings())
            assert excinfo.value is setup_error
            assert fake.quit_called

        with allure.step("Проверить диагностику вторичной ошибки закрытия"):
            notes = getattr(excinfo.value, "__notes__", [])
            assert any(QUIT_ERROR_TEXT in note for note in notes)
