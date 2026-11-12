---
name: run-tests
description: Запустить и проверить существующие тесты Niffler, выбрав unit или UI scope и сообщив результаты конкретного прогона.
---

# Проверка тестов Niffler

Прочитай [AGENTS.md](../../../AGENTS.md) и
[инструкцию запуска](../../../knowledge/testing/run-tests.md).
Проверь текущие изменения через `sh tools/git.sh status` и `diff`.
Выбери минимальную область запроса; `sh tools/run-tests.sh list` показывает
актуальные node ID. Для нового окружения выполни `sh tools/versions.sh`,
для изменённого кода — `sh tools/compile-tests.sh`.

Используй `sh tools/run-tests.sh group unit` для инфраструктурных unit-тестов,
`one 'tests/.../test_*.py::Class::method'` для одного сценария.
UI scope требует `--allow-sut` и разрешения на соответствующий стенд/операции;
учитывай уже выданное разрешение, не запрашивай его повторно. Регистрация
создаёт постоянные данные. Для настройки браузера передавай `--browser` /
`--bversion`; env и remote-настройки остаются в Settings.

При ошибке обратись к [диагностике](../../../knowledge/testing/debugging.md).
Сообщи команду, scope, версии, exit code, passed/failed/errors/skipped и
путь к текущим Allure/JUnit. Collection не является выполнением тестов.
Не меняй тесты ради зелёного результата в задаче только на запуск.
