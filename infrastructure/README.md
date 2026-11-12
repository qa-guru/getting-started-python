# Инфраструктура

Общие инфраструктурные helpers автотестов. Полный каталог переиспользуемых
компонентов — [knowledge/components/README.md](../knowledge/components/README.md),
раздел про этот пакет — [infrastructure.md](../knowledge/components/infrastructure.md).

| Директория | Назначение |
| --- | --- |
| `browser/` | Создание и настройка WebDriver (`factory.create_driver`), тестовые `Settings` (`testing.make_test_settings`) |
| `waits/` | Общие явные ожидания `ElementWaits` для Page Object |
| `reporting/` | Артефакты падения (`artifacts.save_failure_artifacts`), статистика Allure (`stats.collect_stats`), Telegram (`telegram.format_message` / `send_message`) |

Локаторы и действия конкретных страниц здесь не размещаются — они остаются
в Page Object (`pages/`). Тестовые данные и их helpers — в `test_data/`
(`consts/` — фиксированные данные, `utils/` — генерация и загрузка).
