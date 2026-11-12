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

## Локальные CLI-инструменты harness

Это shell/Python-точки входа для агента, а не helpers Page Object.
Полный контракт: [run-tests.md](../testing/run-tests.md).

| Компонент | Путь / вызов | Назначение | Пример использования |
| --- | --- | --- | --- |
| Выбор Python | `tools/_python.sh` (внутренний, source из entry point) | `PYTHON` → проектный venv → `python3`; переход в корень | `PYTHON=/path/to/python sh tools/versions.sh` |
| Проверка окружения | `tools/versions.sh` → `tools/harness.py versions` | Python 3.13/3.14 и точные установленные версии requirements | `sh tools/versions.sh` |
| Проверка исходников | `tools/compile-tests.sh` → `tools/harness.py check` | Версии, компиляция рабочих Python-каталогов, pytest collection | `sh tools/compile-tests.sh` |
| Выбор и запуск тестов | `tools/run-tests.sh` → `tools/harness.py run` | Динамический список node ID, группы/один тест, отдельные Allure/JUnit на запуск; UI требует `--allow-sut` | `sh tools/run-tests.sh group unit` |
| Чтение Git | `tools/git.sh` | Status, diff (включая staged), whitespace check без commit/push/reset | `sh tools/git.sh diff` |
| GitHub Actions CLI | `tools/gh.sh` | Список запусков/логи; явный флаг для rerun/dispatch; см. [контракт](../integrations/ci-github.md) | `GITHUB_REPOSITORY=owner/repo sh tools/gh.sh runs` |

`tools/harness.py` — внутренняя реализация CLI, не публичный Python API.
При новой области тестов обнови `GROUPS`; при смене Python в CI проверь
допустимые версии в `versions()` и инструкцию запуска. Pins читаются из
`requirements.txt`, отдельного списка версий в harness нет.
