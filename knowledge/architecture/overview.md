# Архитектура Niffler UI-тестов

Источники истины — текущий код, [AGENTS.md](../../AGENTS.md),
[requirements.txt](../../requirements.txt) и конфигурация CI.
Этот документ — карта для навигации, а не отдельный набор правил.

| Область | Где читать |
| --- | --- |
| Сценарии | `tests/auth/`, `tests/registration/`, `tests/logout/` |
| Unit-тесты без настоящего браузера | `tests/unit/`: settings, browser factory/fixture, reporting |
| Page Object | `pages/`: `BasePage`, `LoginPage`, `RegisterPage`, `MainPage` |
| Настройки | `settings.py`: `Settings`, `load_settings`; CLI > env > defaults |
| Браузер | `infrastructure/browser/factory.py`: Chrome, Firefox, Remote |
| Ожидания | `infrastructure/waits/element_waits.py`: `ElementWaits` |
| Фикстуры и артефакты | `conftest.py`, `test_data/fixtures.py` |
| Общие компоненты | [Каталог](../components/README.md): импорты, назначение, примеры |
| Запуск | [run-tests.md](../testing/run-tests.md) |
| Диагностика | [debugging.md](../testing/debugging.md) |

## Жизненный цикл

`conftest.py` загружает `.env` через python-dotenv. Session-фикстура `settings`
собирает конфигурацию, function-фикстура `driver` вызывает `create_driver(settings)`
и гарантирует `quit()` в `finally`. Наличие `SELENIUM_REMOTE_URL` выбирает Remote;
`SELENIUM_REMOTE=true` без URL приводит к ошибке конфигурации.
Локальный Selenium Manager может скачивать драйвер: сбор тестов этого не делает.

Page Object получает `(driver, settings)`; настройки окружения внутри страниц
не читаются. Локаторы и действия находятся в страницах, общие ожидания —
в `ElementWaits`. Проверки результата сценария находятся в тестах;
методы страниц могут ожидать готовность страницы. Не заменяй это ограничением
на фиксированное количество проверок или буквальное копирование цепочек вызовов.

Ближайшие образцы — `TestLogin` в `tests/auth/test_login.py` и `TestRegistration`
в `tests/registration/test_registration.py`. Сохраняй их русские явные
`with allure.step(...)` и разметку Allure согласно `AGENTS.md`.

## Данные и окружение

Приложение: `https://niffler.qa.guru`, авторизация: `https://auth.niffler.qa.guru`.
Переопределение через `BASE_URL` и `AUTH_URL`; параметры браузера и таймаута —
в `settings.py`. Не выводи `.env`, пароли или remote URL с credentials в отчёты.

`existing_user` читает `EXISTING_USERNAME`/`EXISTING_PASSWORD`; отсутствие данных —
ошибка подготовки, а не skip. `new_user` генерирует уникальные данные на каждый
тест; успешная регистрация создаёт постоянного пользователя, подтверждённого
механизма удаления нет. Закрытие браузера не очищает серверные данные.
Точные импорты см. в [каталоге фикстур](../components/fixtures.md),
[данных](../components/models.md) и [helpers](../components/utils.md).
Не предполагай безопасность параллельных прогонов с общим аккаунтом.

## Отчётность

Хук `pytest_runtest_makereport` сохраняет скриншот и HTML в `artifacts/`
и прикладывает их к Allure при падении фазы `call`, если доступен `driver`.
Падение setup/teardown не гарантирует эти вложения. Имена файлов зависят
от имени теста и могут повторяться при перезапуске; перед воспроизведением
сохраняй нужные артефакты предыдущего падения.

GitHub Actions и Jenkins используют `allure-results/`; локальный harness
создаёт отдельные каталоги результатов, см. инструкцию запуска.
TestOps не подключён; Allure-отчёт сам по себе не означает интеграцию с TestOps.
