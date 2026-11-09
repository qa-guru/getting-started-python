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

## Jenkins setup

Пайплайн описан в `Jenkinsfile` (declarative): проверка Docker → установка Python-зависимостей и pytest в официальном контейнере Playwright → публикация Allure на исходном Jenkins-агенте.

### Требования к ноде

- Jenkinsfile выбирает агент с label `python`. На нём нужны Docker CLI и доступ к работающему Docker daemon. Если Docker недоступен на учебном Jenkins, администратор должен предоставить подходящий агент; при необходимости замени label в Jenkinsfile.
- Установка зависимостей и тесты выполняются в `mcr.microsoft.com/playwright/python:v1.64.1-noble` (Ubuntu/glibc). Версия образа должна совпадать с `playwright` в `requirements.txt`.
- Браузеры Chromium, Firefox, WebKit и системные зависимости уже включены в образ; отдельный `playwright install` не нужен.
- Исходный агент может использовать musl: Python из него для тестов не используется. Для генерации Allure-отчёта на исходном агенте нужны Java и настроенный Allure CLI.
- Контейнер запускается через `docker run` в `ci/run-playwright.sh`; плагин Docker Pipeline не требуется. Для контейнерного агента используются его тома (`--volumes-from`), если агент виден тому же Docker daemon, иначе — bind mount workspace. Workspace должен быть общим с Docker-контейнером, чтобы Allure-результаты и скриншоты были доступны на исходном агенте.

### Плагины

- **Pipeline** (workflow-aggregator)
- **Allure Jenkins Plugin** (Manage Jenkins → Plugins → Allure) — на jenkins.qa.guru уже установлен (есть джобы `*-allure2`/`*-allure3`)
- **Pipeline: Stage View** — опционально, для удобного отображения

### Настройка Allure CLI

1. **Manage Jenkins → Global Tool Configuration → Allure Commandline → Add Allure Commandline** — на jenkins.qa.guru уже настроена.
2. Если настраиваешь свой Jenkins: имя — любое (например `allure`), включи **Install automatically** → **Install from Maven Central**, версия `2.46.1`; либо установи Allure на агент вручную и укажи `ALLURE_HOME`.

### Создание job

1. **New Item → Pipeline** → имя (например `niffler-ui-tests`).
2. В разделе **Pipeline**: Definition = **Pipeline script from SCM**.
3. SCM = **Git**, Repository URL — `https://github.com/L4m4w/getting-started-python.git` (или свой форк), Branch — `*/master`, Script Path — `Jenkinsfile`.
4. Сохранить → **Build with Parameters**: выбор `BROWSER` (chromium/firefox/webkit), `BASE_URL`, `AUTH_URL`.

### Поведение

- Падение тестов → билд `UNSTABLE` (через `catchError`), но Allure-отчёт и артефакты публикуются всегда (`post always`).
- Архивируются `allure-results/**` всегда и `artifacts/**` (скриншоты/page source) при падении.
- История билдов: 20, конкурентные запуски запрещены, таймаут — 20 минут.

Токены и id чатов хранятся только в GitHub Secrets / Jenkins Credentials — не в коде.
