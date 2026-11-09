# План: UI-фреймворк автотестов для Niffler

Репозиторий: `L4m4w/getting-started-python` (форк `qa-guru/getting-started-python`)
Стенд: https://niffler.qa.guru · Стек: Python 3.13 + pytest + Selenium + Allure

## Статусы фаз

| Фаза | Содержание | Статус |
|---|---|---|
| 1 | conftest.py: фикстура драйвера, `--browser`/`--bversion`, `BASE_URL`/`AUTH_URL` через env, скриншот + page source на падении (`artifacts/`) | ✅ done |
| 2 | Page Object (`pages/`: BasePage, LoginPage, MainPage, RegisterPage), тесты без прямых вызовов driver | ✅ done |
| 3 | Тесты: авторизация / регистрация / логаут — организованы по `tests/<область>/` | ✅ done |
| 4 | Allure: `@allure.step`, epic/feature/story/severity, attachments, README-команды | ✅ done |
| 5 | GitHub Actions `.github/workflows/tests.yml`: прогон, Allure-отчёт, gh-pages, тренды, artifacts | ✅ done |
| 6 | `Jenkinsfile`: pinned-агент `python-python314-jenkins-agent-1`, Allure-плагин, Selenoid через credentials-параметр | ✅ done |
| 7 | Telegram: `notify_telegram.py` (exit 0 всегда, skip без секретов), шаги в GHA и Jenkins | ✅ done |
| 8 | Mini-review: чистый checkout, секреты, матрица статусов CI | ✅ done — см. `docs/retrospective.md` |

## Проверено

- Локально: `pytest` 7/7, `allure generate` → `allure-report/index.html`
- GHA: workflow валиден (actionlint), реальный прогон на форке, отчёт в Pages
- Jenkins: реальные билды на `jenkins.qa.guru` (номера и итерации — в git log)

## Ограничения и принятые решения

- **Стек — Selenium, не Playwright**: на musl-based Jenkins-агенте нет
  playwright-wheels (ни из корпоративного индекса, ни с pypi.org).
  Миграция зафиксирована коммитом `682490b`.
- **Jenkins-агент pinned**: `python-python314-jenkins-agent-1` — на нём
  проверен прогон (`fabedc2`).
- **Selenoid**: remote-режим включается через `SELENIUM_REMOTE_URL`;
  creds — Jenkins UsernamePassword credential, выбираемый
  credentials-параметром (user-scoped, `d171ba0`); локально — через
  `.env` + python-dotenv.
- **Локализация стенда**: текст ошибки логина зависит от locale
  браузера (ru локально, en в Selenoid) — assert принимает оба
  варианта (`e0d9a17`).
- **GitHub Pages**: включается руками — Settings → Pages → Deploy from
  a branch → `gh-pages`.
- **Секреты**: `TELEGRAM_TOKEN`/`TELEGRAM_CHAT_ID` в GitHub Secrets /
  Jenkins Credentials; в коде — только env.
- **Ветка**: `master` (не `main`) — триггеры, бейдж и URL бейджа
  привязаны к ней (`cbe43db`).

## Известные долги

- `github_should_find_selene.py` в корне — демо-файл вне структуры
  `tests/`; оставлен или удалить — решить владельцу.
- История трендов Allure в gh-pages подтягивается при деплое — при
  первом прогоне ветки история пуста.
