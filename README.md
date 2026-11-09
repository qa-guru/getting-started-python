# Niffler UI Autotests

[![UI Tests](https://github.com/L4m4w/getting-started-python/actions/workflows/tests.yml/badge.svg)](https://github.com/L4m4w/getting-started-python/actions/workflows/tests.yml)

UI-фреймворк автотестирования для [niffler.qa.guru](https://niffler.qa.guru): Python + pytest + Selenium, Page Object, Allure-отчёты.

## Установка

```bash
pip install -r requirements.txt
brew install allure   # для генерации отчётов (требуется Java)
```

Установленные браузер и драйвер не требуются настраивать вручную: Selenium Manager сам подберёт драйвер под установленный Chrome/Firefox.

## Запуск тестов (локально)

```bash
pytest                          # все тесты, chrome, headless
pytest --browser=firefox        # другой браузер: chrome | firefox (chromium = алиас chrome)
pytest --bversion=131           # версия браузера (capability browserVersion, для remote)
HEADLESS=false pytest           # с открытым окном браузера
BASE_URL=https://niffler.qa.guru pytest   # переопределить стенд
AUTH_URL=https://auth.niffler.qa.guru pytest  # переопределить auth-сервис
```

## Запуск через Remote WebDriver (Selenium Grid / Selenoid)

```bash
SELENIUM_REMOTE_URL=https://selenoid.qa.guru/wd/hub pytest --browser=chrome
# с basic-auth, если грид требует логин/пароль:
SELENIUM_REMOTE_URL=https://user:pass@selenoid.qa.guru/wd/hub pytest --browser=chrome
# либо явно включить remote-режим:
SELENIUM_REMOTE=true SELENIUM_REMOTE_URL=http://grid:4444/wd/hub pytest
```

Если `SELENIUM_REMOTE=true`, а `SELENIUM_REMOTE_URL` не задан — прогон падает с понятной ошибкой до старта браузера. В remote-режиме `--bversion` передаётся как capability `browserVersion`.

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
conftest.py                 # фикстуры Selenium WebDriver, CLI-опции, attachments на падении
pages/                      # Page Object: BasePage, LoginPage, MainPage, RegisterPage
test_niffler_login.py       # тесты авторизации
test_niffler_registration.py  # тесты регистрации и логаута
```

## CI

- GitHub Actions: `.github/workflows/tests.yml` — прогон на push в `master`, PR и вручную (выбор браузера). Allure-отчёт сохраняется как artifact и публикуется в GitHub Pages (ветка `gh-pages`): https://L4m4w.github.io/getting-started-python/
- Jenkins: `Jenkinsfile`

Для публикации отчёта в форке включи GitHub Pages: **Settings → Pages → Source: Deploy from a branch → gh-pages**. Если репозиторий форкнут — замени `L4m4w/getting-started-python` в бейдже и ссылке на свой `<owner>/<repo>`.

## Jenkins setup

Пайплайн описан в `Jenkinsfile` (declarative): venv → `pip install -r requirements.txt` → pytest → публикация Allure-отчёта.

### Требования к ноде

- На https://jenkins.qa.guru/ используется агент `python-python314-jenkins-agent-1` (Python 3.14, Linux x86_64, musl). Selenium — pure-Python пакет и ставится на musl без проблем (в отличие от Playwright).
- Сейчас пайплайн запускает браузер **локально на агенте** — на нём должен быть установлен Chrome или Firefox (драйвер подберёт Selenium Manager). Если браузера нет, вариант — удалённый запуск: задай в job env `SELENIUM_REMOTE_URL` (например `https://user:pass@selenoid.qa.guru/wd/hub`) — remote-режим включится автоматически. Креды в URL храни через Jenkins Credentials (`withCredentials`), не в коде.
- На своём Jenkins замени label на нужный (`agent any` или свой label), но убедись, что агент — Linux с Python ≥ 3.11.

### Плагины

- **Pipeline** (workflow-aggregator)
- **Allure Jenkins Plugin** (Manage Jenkins → Plugins → Allure) — на jenkins.qa.guru уже установлен
- **Pipeline: Stage View** — опционально, для удобного отображения

### Настройка Allure CLI

1. **Manage Jenkins → Global Tool Configuration → Allure Commandline → Add Allure Commandline** — на jenkins.qa.guru уже настроена.
2. Если настраиваешь свой Jenkins: имя — любое (например `allure`), включи **Install automatically** → **Install from Maven Central**, версия `2.46.1`; либо установи Allure на агент вручную и укажи `ALLURE_HOME`.

### Создание job

1. **New Item → Pipeline** → имя (например `niffler-ui-tests`).
2. В разделе **Pipeline**: Definition = **Pipeline script from SCM**.
3. SCM = **Git**, Repository URL — `https://github.com/L4m4w/getting-started-python.git` (или свой форк), Branch — `*/master`, Script Path — `Jenkinsfile`.
4. Сохранить → **Build with Parameters**: выбор `BROWSER` (chrome/firefox), `BASE_URL`, `AUTH_URL`.

### Поведение

- Падение тестов → билд `UNSTABLE` (через `catchError`), но Allure-отчёт и артефакты публикуются всегда (`post always`).
- Архивируются `allure-results/**` всегда и `artifacts/**` (скриншоты/page source) при падении.
- История билдов: 20, конкурентные запуски запрещены, таймаут — 20 минут.

Токены, адреса с кредами и id чатов хранятся только в GitHub Secrets / Jenkins Credentials — не в коде.
