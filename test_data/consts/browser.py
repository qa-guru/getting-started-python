"""Фиксированные данные для unit-тестов браузера и тестовых Settings.

Значения — примеры настроек и данных для подмен, а не адреса реального
стенда. Технические параметры инфраструктуры (размер окна, имена env)
остаются в своих компонентах.
"""

# Пример значений настроек для make_test_settings и проверок выбора драйвера.
TEST_BASE_URL = "https://app.example"
TEST_AUTH_URL = "https://auth.example"
TEST_TIMEOUT_S = 10
TEST_BROWSER = "chrome"
TEST_REMOTE_URL = "http://grid:4444/wd/hub"

# Браузеры, создаваемые локально при отсутствии remote_url.
LOCAL_BROWSERS = ("chrome", "firefox")

# Тексты ошибок, выбрасываемых подменёнными драйверами в проверках сбоев.
SETUP_ERROR_TEXT = "set_window_size failed"
QUIT_ERROR_TEXT = "driver quit failed"

# Текст ошибки, которую условный тест передаёт в фикстуру driver.
TEST_ERROR_TEXT = "test failed"
