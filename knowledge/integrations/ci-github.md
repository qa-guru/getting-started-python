# GitHub Actions: чтение и запуск

Источник конфигурации — `.github/workflows/tests.yml`.
`tools/gh.sh` использует установленный `gh`, существующую авторизацию gh
или `GH_TOKEN`, и явный `GITHUB_REPOSITORY=owner/repo`.
Не сохраняй токен в документацию, не запускай интерактивный login от имени агента.

```sh
GITHUB_REPOSITORY=L4m4w/getting-started-python sh tools/gh.sh runs
GITHUB_REPOSITORY=L4m4w/getting-started-python sh tools/gh.sh view 123
GITHUB_REPOSITORY=L4m4w/getting-started-python sh tools/gh.sh view-log 123
```

При расследовании CI-only ошибки сначала прочитай лог нужного запуска.
Наличие workflow не доказывает успешный прогон или работоспособность секретов.

Следующие команды выполняются только при имеющемся разрешении на CI-запуск:

```sh
GITHUB_REPOSITORY=L4m4w/getting-started-python sh tools/gh.sh --allow-ci-write rerun 123
GITHUB_REPOSITORY=L4m4w/getting-started-python sh tools/gh.sh --allow-ci-write dispatch firefox
```

Dispatch запускает `tests.yml`, передаёт существующий input `browser`
(`chrome` по умолчанию). Rerun повторяет исходный запуск целиком и может снова
создать тестовых пользователей. Оба действия используют сеть и CI-ресурсы;
флаг не заменяет разрешение. Локальная проверка harness не запускает эти команды.

Jenkins остаётся отдельной интеграцией из `Jenkinsfile` и README.
Allure TestOps и `allurectl` этим harness не подключаются.
