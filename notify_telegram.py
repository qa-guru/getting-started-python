"""Send a Telegram notification with test-run summary.

Reads counters from allure-results/*-result.json, formats a Markdown
message and posts it via the Bot API. Silently exits 0 when
TELEGRAM_TOKEN / TELEGRAM_CHAT_ID are not configured, so pipelines
without secrets keep working.

Configuration via environment variables:
    TELEGRAM_TOKEN   — bot token from @BotFather (required)
    TELEGRAM_CHAT_ID — target chat/channel id (required)
    RESULT_DIR       — path to allure-results (default: allure-results)
    REPO             — owner/repo or project name
    BRANCH           — git branch
    COMMIT           — git commit sha (shortened to 7 chars)
    TRIGGER          — e.g. "push by octocat" or "PR #12"
    RUN_URL          — link to the CI run/build
    REPORT_URL       — link to the Allure report
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def collect_stats(result_dir: Path) -> dict:
    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0}
    for path in result_dir.glob("*-result.json"):
        try:
            status = json.loads(path.read_text()).get("status")
        except (json.JSONDecodeError, OSError):
            continue
        if status in stats:
            stats[status] += 1
    return stats


def main() -> int:
    token = os.environ.get("TELEGRAM_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("TELEGRAM_TOKEN/TELEGRAM_CHAT_ID not set — skipping notification")
        return 0

    stats = collect_stats(Path(os.environ.get("RESULT_DIR", "allure-results")))
    failed = stats["failed"] + stats["broken"]
    total = sum(stats.values())

    icon = "🟢" if failed == 0 else "🔴"
    result = "PASSED" if failed == 0 else "FAILED"
    commit = os.environ.get("COMMIT", "")[:7]

    lines = [
        f"{icon} *{result}* — UI tests",
        f"Repo: `{os.environ.get('REPO', '?')}`",
        f"Branch: `{os.environ.get('BRANCH', '?')}`  Commit: `{commit}`",
        f"Trigger: {os.environ.get('TRIGGER', '?')}",
        "",
        f"Total: {total}  |  ✅ {stats['passed']}  ❌ {failed}  ⏭ {stats['skipped']}",
    ]
    links = []
    if os.environ.get("REPORT_URL"):
        links.append(f"[Allure report]({os.environ['REPORT_URL']})")
    if os.environ.get("RUN_URL"):
        links.append(f"[CI run]({os.environ['RUN_URL']})")
    if links:
        lines += ["", "  |  ".join(links)]

    payload = {
        "chat_id": chat_id,
        "text": "\n".join(lines),
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
            print(f"Telegram notification sent: HTTP {resp.status}")
    except Exception as exc:  # notification must never fail the build
        print(f"Telegram notification failed: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
