# Вспомогательные функции

[Оглавление каталога](README.md)

Новые вспомогательные функции работы с тестовыми данными размещаются
в `test_data/utils/`. Инфраструктурные helpers описаны в [отдельном разделе](infrastructure.md).
Здесь указаны текущие пути существующих функций.

| Компонент | Путь импорта | Назначение | Пример использования |
| --- | --- | --- | --- |
| `unique_username` | `test_data.utils.users.unique_username` | Генерация уникального имени пользователя | `username = unique_username()` |
| `unique_password` | `test_data.utils.users.unique_password` | Генерация пароля для тестового пользователя | `password = unique_password()` |
| `unique_user` | `test_data.utils.users.unique_user` | Генерация учётных данных нового пользователя без регистрации на стенде | `user = unique_user()` |
| `load_existing_user` | `test_data.utils.users.load_existing_user` | Загрузка учётных данных из окружения или переданного mapping | `user = load_existing_user()` |

Параметры генерации (префикс имени и длины значений) вынесены
в `test_data/consts/users.py`.

Имена также доступны через реэкспорт `test_data` (`from test_data import unique_user`).
