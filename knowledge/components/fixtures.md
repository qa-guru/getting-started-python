# Фикстуры

[Оглавление каталога](README.md)

Фикстуры `settings` и `driver` объявлены в `conftest.py`, фикстуры
тестовых данных подключены через `pytest_plugins` в `conftest.py`.

| Компонент | Путь импорта | Назначение | Пример использования |
| --- | --- | --- | --- |
| `settings` | `conftest.settings` | Session-фикстура `Settings`: собирается из CLI-опций `--browser`/`--bversion` и env через `load_settings` | Аргумент `settings` в тесте; передаётся в Page Object: `LoginPage(driver, settings)` |
| `driver` | `conftest.driver` | Function-фикстура WebDriver: создаётся через `create_driver(settings)`, закрывается `quit()` в `finally` | Аргумент `driver` в тесте; передаётся в Page Object |
| `existing_user` | pytest-плагин `test_data.fixtures` | Session-фикстура существующего пользователя из окружения; аккаунт только читается, без teardown | Аргумент `existing_user` в тесте; данные: `existing_user.username` |
| `new_user` | pytest-плагин `test_data.fixtures` | Фикстура новых уникальных учётных данных на каждый тест | Аргумент `new_user` в тесте; данные: `new_user.username` |

Ограничение очистки: на стенде niffler.qa.guru нет подтверждённого механизма
удаления пользователей, поэтому `new_user` не имеет teardown — созданные
при регистрации пользователи накапливаются на стенде.
