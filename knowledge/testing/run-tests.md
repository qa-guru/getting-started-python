# Запуск и проверка тестов

Все команды ниже выполняются из корня проекта. Shell-скрипты запускаются
через `sh`; executable bit не нужен. Они сами переходят в корень проекта.
Интерпретатор выбирается так: `PYTHON` (путь к executable, без аргументов),
затем `.venv/bin/python`, затем `python3` из PATH.

## Предварительная проверка

```sh
sh tools/git.sh status
sh tools/versions.sh
sh tools/compile-tests.sh
sh tools/run-tests.sh list
```

`versions.sh` проверяет Python 3.13/3.14 и точные версии всех зависимостей
из `requirements.txt`, используя metadata установленного окружения.
Python 3.13 соответствует локальному проекту/Actions, 3.14 — описанному
Jenkins-агенту. Проверка одной версии не подтверждает другую.
Она не проверяет браузер, драйвер, сетевой доступ или наличие тестового аккаунта.
Скрипты ничего не устанавливают и не запускают сервисы.

`compile-tests.sh` проверяет версии, компилирует корневые Python-файлы,
`pages/`, `infrastructure/`, `test_data/`, `tests/`, `tools/`, затем выполняет
`pytest --collect-only`. `list` получает актуальные node ID через pytest,
а не из сохранённого списка. Сбор загружает conftest, dotenv и pytest-плагины,
но не исполняет тесты и не создаёт браузер через наши фикстуры.
Компиляция и сбор тестов не являются успешным тестовым прогоном.

## Выбор области

```sh
sh tools/run-tests.sh group unit
sh tools/run-tests.sh one 'tests/unit/test_browser.py::TestDriverFactory::test_remote_mode_uses_remote_driver'
sh tools/run-tests.sh --allow-sut group auth --browser firefox
sh tools/run-tests.sh --allow-sut one 'tests/auth/test_login.py::TestLogin::test_success_login'
sh tools/run-tests.sh --allow-sut group registration
sh tools/run-tests.sh --allow-sut group ui --browser chrome --bversion 131
sh tools/run-tests.sh --allow-sut all
```

Группы: `unit`, `auth`, `registration`, `logout`, `ui` (три UI-области).
`all` выбирает весь `tests/`, включая unit. `one` принимает настоящий node ID
в существующем файле `tests/.../test_*.py`; параметризованный ID заключай в кавычки.
При добавлении новой области обнови `GROUPS` в `tools/harness.py`; новые тесты
в существующих областях обнаруживаются pytest автоматически.

Unit-тесты используют подмены драйвера и транспорта; доступ к стенду им не нужен.
Для любого выполнения вне `tests/unit/` нужен `--allow-sut`.
Этот флаг фиксирует уже имеющееся разрешение на выбранный стенд и сценарии,
включая постоянные записи регистрации; он не заменяет разрешения клиента
или sandbox. Учитывай разрешение из текущего запроса, повторно его не запрашивай.
Запрос на внедрение harness сам по себе не требует UI-прогона или CI-запуска.

Браузер и стенд настраиваются существующими `Settings`: `--browser`,
`--bversion`, `HEADLESS`, `BASE_URL`, `AUTH_URL`, `TIMEOUT_S`,
`SELENIUM_REMOTE`, `SELENIUM_REMOTE_URL`, `.env`. Значения секретов не печатай.
Перед UI-прогоном проверь наличие нужного аккаунта, локального браузера/драйвера
либо доступного Grid. Selenium Manager при первом старте может обратиться к сети.

Скрипты не передают произвольные pytest-флаги. Для более узкого фильтра или
специальных pytest-опций используй прямой `python -m pytest` в выбранном окружении,
с теми же требованиями к области и доступу.

## Результаты и коды завершения

Каждый запуск через `run-tests.sh` создаёт новый каталог:
`artifacts/harness/run-*/`, внутри `allure-results/` и `junit.xml`.
Точный путь печатается перед pytest. Посмотреть конкретный отчёт:

```sh
allure serve artifacts/harness/run-ИМЯ/allure-results
```

CI и прямые команды из README продолжают писать в `allure-results/`.
Локальные результаты harness не подхватываются автоматически Telegram-скриптом
или CI: передавай точный каталог инструментам анализа.
Скриншоты/HTML по-прежнему пишет существующий хук в `artifacts/`.

В результате укажи команду, интерпретатор/версии, область, exit code,
число passed/failed/errors/skipped и путь к материалам текущего запуска.
Сохраняй различие между failed теста и ошибками подготовки/teardown.
Сбор без выполнения, пропуски или старые результаты не подтверждают PASS.

Коды pytest сохраняются (включая 5 при отсутствии тестов); argparse возвращает
2 при неверном scope/аргументах; 69 означает неподходящий Python/зависимости,
77 — UI-запуск без подтверждения доступа. Shell `git.sh`/`gh.sh` используют
64 для неверных аргументов. Скрипты не очищают результаты предыдущих запусков.

## CI

Для GitHub Actions см. [ci-github.md](../integrations/ci-github.md).
Jenkins описан в `README.md` и `Jenkinsfile`; его credentials не заменяются env
из локального shell. Сохраняй порядок существующего CI: выполнение тестов →
отчётность/Telegram даже при падении → итоговый статус.
