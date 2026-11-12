"""Сбор статистики прогона из результатов Allure."""
import json
from pathlib import Path


def collect_stats(result_dir: Path) -> dict:
    """Посчитать статусы по файлам *-result.json в result_dir.

    Возвращает счётчики passed/failed/broken/skipped; нечитаемые
    файлы пропускаются.
    """
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0}
    for path in result_dir.glob("*-result.json"):
        try:
            status = json.loads(path.read_text()).get("status")
        except (json.JSONDecodeError, OSError):
            continue
        if status in stats:
            stats[status] += 1
    return stats
