# Niffler UI Autotests

[![UI Tests](https://github.com/L4m4w/getting-started-python/actions/workflows/tests.yml/badge.svg)](https://github.com/L4m4w/getting-started-python/actions/workflows/tests.yml)

UI-фреймворк автотестирования для [niffler.qa.guru](https://niffler.qa.guru): Python + pytest + Playwright, Page Object, Allure-отчёты.

## Установка

```bash
pip install -r requirements.txt
playwright install chromium
brew install allure   # для генерации отчётов (требуется Java)
```

## Запуск тестов

```bash
pytest                          # все тесты, chromium, headless
pytest --browser=firefox        # другой движок: chromium | firefox | webkit
pytest --bversion=131           # метка версии браузера (информационная)
HEADLESS=false pytest           # с открытым окном браузера
BASE_URL=https://niffler.qa.guru pytest   # переопределить стенд
AUTH_URL=https://auth.niffler.qa.guru pytest  # переопределить auth-сервис
```

При падении теста скриншот и page source сохраняются в `artifacts/` и прикладываются к Allure-отчёту.

## Allure-отчёт

```bash
pytest --alluredir=allure-results   # прогон с записью результатов
allure serve allure-results         # отчёт в браузере (временный)
allure generate allure-results -o allure-report --clean   # статический отчёт
allure open allure-report
```

## Структура

```
conftest.py                 # фикстуры Playwright, CLI-опции, attachments на падении
pages/                      # Page Object: BasePage, LoginPage, MainPage, RegisterPage
test_niffler_login.py       # тесты авторизации
test_niffler_registration.py  # тесты регистрации и логаута
```

## CI

- GitHub Actions: `.github/workflows/tests.yml` — прогон на push в `master`, PR и вручную (выбор браузера). Allure-отчёт сохраняется как artifact и публикуется в GitHub Pages (ветка `gh-pages`): https://L4m4w.github.io/getting-started-python/
- Jenkins: `Jenkinsfile`

Для публикации отчёта в форке включи GitHub Pages: **Settings → Pages → Source: Deploy from a branch → gh-pages**. Если репозиторий форкнут — замени `L4m4w/getting-started-python` в бейдже и ссылке на свой `<owner>/<repo>`.

Токены и id чатов хранятся только в GitHub Secrets / Jenkins Credentials — не в коде.
