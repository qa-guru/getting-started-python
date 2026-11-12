"""Фиксированные данные для unit-тестов отчётности и уведомлений.

Наборы данных неизменяемы (MappingProxyType), чтобы тесты не разделяли
изменяемое состояние. Ненастоящие креды нужны только для подмены
транспорта; реальные секреты берутся из окружения.
"""
from types import MappingProxyType

# Подменные креды и ожидаемый адрес Bot API для проверок без сети.
TELEGRAM_TOKEN = "test-telegram-token"
TELEGRAM_CHAT_ID = "123456"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

HTTP_STATUS_OK = 200

# Сведения о запуске для проверки текста уведомления.
RUN_INFO = MappingProxyType({
    "repo": "owner/repo",
    "branch": "master",
    "commit": "abc1234",
    "trigger": "push",
    "report_url": "https://example.org/report",
    "run_url": "https://example.org/run/1",
})

# Наборы статистики прогона и ожидаемые итоги.
STATS_ALL_PASSED = MappingProxyType(
    {"passed": 7, "failed": 0, "broken": 0, "skipped": 0}
)
STATS_MIXED = MappingProxyType(
    {"passed": 5, "failed": 1, "broken": 1, "skipped": 2}
)
STATS_MIXED_TOTAL = 9
STATS_MIXED_FAILED = 2

# Полезные нагрузки артефактов и тексты ошибок подменённых обработчиков.
SCREENSHOT_BYTES = b"fake-png"
PAGE_SOURCE_HTML = "<html><body>page</body></html>"
ARTIFACT_ERROR_TEXT = "artifact backend unavailable"
SEND_ERROR_TEXT = "network unreachable"
