# Инфраструктурные helpers

[Оглавление каталога](README.md)

Новые общие компоненты размещаются по назначению:

| Директория | Назначение |
| --- | --- |
| `infrastructure/browser/` | Создание и настройка браузера и WebDriver |
| `infrastructure/waits/` | Общие механизмы явных ожиданий |
| `infrastructure/reporting/` | Отчётность и вложения |

| Компонент | Путь импорта | Назначение | Пример использования |
| --- | --- | --- | --- |
| `load_settings` | `settings.load_settings` | Сбор и валидация `Settings` по приоритету CLI > env > дефолты: алиас `chromium`→`chrome`, нормализация URL, ошибки при неподдерживаемом браузере, remote без URL и невалидном `TIMEOUT_S` | `settings_obj = load_settings(browser_option="firefox")` |
| `create_driver` | `infrastructure.browser.factory.create_driver` | Создать Remote/Chrome/Firefox драйвер и настроить окно по Settings. Сбой обязательной настройки прерывает подготовку: драйвер закрывается, исходная ошибка передаётся вызывающему коду; ошибка `quit()` добавляется к ней через `add_note` | `drv = create_driver(settings)` |
| `make_test_settings` | `infrastructure.browser.testing.make_test_settings` | Settings со значениями по умолчанию для unit-тестов; примеры значений — `test_data.consts.browser` | `s = make_test_settings(browser="firefox")` |
| `ElementWaits` | `infrastructure.waits.ElementWaits` | Явные ожидания для Page Object: `visible`, `clickable`, `present`, `url_contains`, `until` | `self.wait.visible(locator)` |
| `save_failure_artifacts` | `infrastructure.reporting.artifacts.save_failure_artifacts` | Скриншот и page source упавшего теста в каталог и Allure. Сбои каталога и артефактов диагностируются `warnings.warn` и не подменяют исходное падение теста | `save_failure_artifacts(drv, ARTIFACTS_DIR, name)` |
| `collect_stats` | `infrastructure.reporting.stats.collect_stats` | Счётчики passed/failed/broken/skipped по allure-results; нечитаемые файлы пропускаются | `stats = collect_stats(Path("allure-results"))` |
| `format_message` | `infrastructure.reporting.telegram.format_message` | Markdown-сообщение о прогоне по статистике и сведениям запуска | `text = format_message(stats, repo, branch, commit, trigger)` |
| `send_message` | `infrastructure.reporting.telegram.send_message` | Отправка через Telegram Bot API; при ошибке транспорта бросает `TelegramSendError` с замаскированным токеном | `send_message(token, chat_id, text)` |
| `TelegramSendError` | `infrastructure.reporting.telegram.TelegramSendError` | Ошибка отправки уведомления; текст не содержит секретов | `pytest.raises(TelegramSendError)` |

Корневой `notify_telegram.py` остаётся CLI-точкой входа для CI и делегирует
`infrastructure.reporting`: без секретов или при сбое отправки возвращает 0.
Хук `pytest_runtest_makereport` в `conftest.py` остаётся точкой подключения
артефактов к pytest.
