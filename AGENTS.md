# Project Rules

UI-автотесты для niffler.qa.guru: Python 3.13 + pytest + Selenium,
Page Object, Allure.

## Запуск
- `pytest` — все тесты (chrome, headless по умолчанию)
- `pytest --browser=firefox`, `HEADLESS=false pytest`
- `BASE_URL=... AUTH_URL=... pytest` — переопределить стенд
- `pytest --alluredir=allure-results` → `allure generate allure-results -o allure-report --clean`

## Конвенции
- Тесты лежат в `tests/<область>/test_*.py`; Page Object в `pages/`,
  базовый класс `pages/base_page.py`
- В тестах нет прямых вызовов `driver` — только через page objects
- На методах page objects — `@allure.step`; проверки в тестах —
  `with allure.step(...)`
- Разметка тестов: `@allure.epic/.feature/.story/.severity/.title`
- Скриншот + page source на падении пишет conftest-хук в `artifacts/`
- Секреты — только env / GitHub Secrets / Jenkins Credentials,
  никогда в коде

## CI
- GitHub Actions: `.github/workflows/tests.yml` — паттерн
  "тесты с continue-on-error → отчёт и Telegram с if: always() →
  exit 1 в конце". Не нарушай этот порядок.
- Jenkins: `Jenkinsfile` — Allure-плагин + Telegram через credentials
- Уведомления: `notify_telegram.py` — всегда exit 0, без секретов skip
