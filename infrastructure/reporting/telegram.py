"""Форматирование и отправка Telegram-уведомлений о прогоне тестов."""
import json
import urllib.request


class TelegramSendError(RuntimeError):
    """Ошибка отправки уведомления; текст не содержит секретов."""


def format_message(
    stats: dict,
    repo: str,
    branch: str,
    commit: str,
    trigger: str,
    report_url: str = "",
    run_url: str = "",
) -> str:
    """Собрать Markdown-текст уведомления по статистике и сведениям о запуске."""
    failed = stats["failed"] + stats["broken"]
    total = sum(stats.values())

    icon = "🟢" if failed == 0 else "🔴"
    result = "PASSED" if failed == 0 else "FAILED"

    lines = [
        f"{icon} *{result}* — UI tests",
        f"Repo: `{repo}`",
        f"Branch: `{branch}`  Commit: `{commit}`",
        f"Trigger: {trigger}",
        "",
        f"Total: {total}  |  ✅ {stats['passed']}  ❌ {failed}  ⏭ {stats['skipped']}",
    ]
    links = []
    if report_url:
        links.append(f"[Allure report]({report_url})")
    if run_url:
        links.append(f"[CI run]({run_url})")
    if links:
        lines += ["", "  |  ".join(links)]
    return "\n".join(lines)


def send_message(token: str, chat_id: str, text: str) -> int:
    """Отправить сообщение через Telegram Bot API; вернуть HTTP-статус.

    При ошибке транспорта бросает TelegramSendError: токен в тексте
    ошибки замаскирован и не попадёт в логи сборки.
    """
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except Exception as e:
        safe = str(e).replace(token, "***") if token else str(e)
        raise TelegramSendError(f"Telegram API request failed: {safe}") from e
