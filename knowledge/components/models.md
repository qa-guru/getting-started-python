# Модели и исключения

[Оглавление каталога](README.md)

| Компонент | Путь импорта | Назначение | Пример использования |
| --- | --- | --- | --- |
| `UserCredentials` | `test_data.users.UserCredentials` | Модель логина и пароля пользователя | `UserCredentials(username=name, password=password)` |
| `MissingTestDataError` | `test_data.users.MissingTestDataError` | Ошибка при отсутствии обязательных тестовых данных | `pytest.raises(MissingTestDataError)` |
| `Settings` | `settings.Settings` | Frozen-dataclass настроек запуска: URL стендов, таймаут, браузер, headless, remote | `Settings(base_url=..., auth_url=..., timeout_s=10, browser="chrome", ...)` |
