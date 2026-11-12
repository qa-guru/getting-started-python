# Константы

[Оглавление каталога](README.md)

В `test_data/consts/` размещаются фиксированные данные для тестов, функций
и классов: входные значения, ожидаемые результаты и наборы параметризации.
Локаторы, названия Allure-шагов и технические параметры остаются
в соответствующих компонентах. Ниже указаны текущие пути существующих констант.

| Компонент | Путь импорта | Назначение | Пример использования |
| --- | --- | --- | --- |
| `WRONG_PASSWORD`, `BAD_CREDENTIALS_ERRORS` | `test_data.consts.auth` | Неверный пароль и допустимые тексты ошибки кредов (en/ru) | `assert error in BAD_CREDENTIALS_ERRORS` |
| `HISTORY_HEADER_TEXT` | `test_data.consts.main_page` | Ожидаемый заголовок истории трат | `assert main_page.history_header_text() == HISTORY_HEADER_TEXT` |
| `REGISTRATION_SUCCESS_MESSAGE`, `PASSWORDS_MISMATCH_ERROR`, `MISMATCHED_PASSWORD_SUFFIX`, `USERNAME_TAKEN_ERROR_TEMPLATE` | `test_data.consts.registration` | Ожидаемые сообщения и входные данные тестов регистрации | `assert register_page.error_text() == USERNAME_TAKEN_ERROR_TEMPLATE.format(name)` |
| `USERNAME_PREFIX`, `USERNAME_SUFFIX_LENGTH`, `PASSWORD_LENGTH` | `test_data.consts.users` | Параметры генерации уникальных пользователей | Используются в `test_data.utils.users.unique_username` |
| `EMPTY_ENV`, `ENV_*`, `CLI_*`, `EXPECTED_*`, `ERROR_PATTERN_*`, `UNSUPPORTED_BROWSER` | `test_data.consts.settings_data` | Входные env (read-only через `MappingProxyType`) и ожидаемые значения `tests/unit/test_settings.py` | `load_settings(env=ENV_BROWSER_FIREFOX) == EXPECTED_BROWSER_FIREFOX` |
| `TEST_BASE_URL`, `TEST_AUTH_URL`, `TEST_TIMEOUT_S`, `TEST_BROWSER`, `TEST_REMOTE_URL`, `LOCAL_BROWSERS`, `SETUP_ERROR_TEXT`, `QUIT_ERROR_TEXT`, `TEST_ERROR_TEXT` | `test_data.consts.browser` | Примеры настроек и тексты ошибок подмен для `tests/unit/test_browser.py` и `infrastructure.browser.testing.make_test_settings` | `create_driver(make_test_settings(remote_url=TEST_REMOTE_URL))` |
| `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_API_URL`, `HTTP_STATUS_OK`, `RUN_INFO`, `STATS_ALL_PASSED`, `STATS_MIXED`, `STATS_MIXED_TOTAL`, `STATS_MIXED_FAILED`, `SCREENSHOT_BYTES`, `PAGE_SOURCE_HTML`, `ARTIFACT_ERROR_TEXT`, `SEND_ERROR_TEXT` | `test_data.consts.reporting` | Подменные креды (не реальные), наборы статистики (`MappingProxyType`) и payload'ы артефактов для `tests/unit/test_reporting.py` | `send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, "text")` |
| `ENV_USERNAME`, `ENV_PASSWORD` | `test_data.utils.users.ENV_USERNAME`, `test_data.utils.users.ENV_PASSWORD` | Имена переменных окружения для учётных данных | `env = {ENV_USERNAME: name, ENV_PASSWORD: password}` |
| `WINDOW_WIDTH`, `WINDOW_HEIGHT` | `infrastructure.browser.factory.WINDOW_WIDTH` | Размер окна браузера | `assert drv.window_size == (WINDOW_WIDTH, WINDOW_HEIGHT)` |
