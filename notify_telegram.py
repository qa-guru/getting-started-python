"""Send a Telegram notification with test-run summary.

CLI entry point for GitHub Actions and Jenkins. Statistics collection
and message logic live in infrastructure/reporting/. Silently exits 0
when TELEGRAM_TOKEN / TELEGRAM_CHAT_ID are not configured, so pipelines
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

import os
import sys
from pathlib import Path

from infrastructure.reporting.stats import collect_stats
from infrastructure.reporting.telegram import format_message, send_message


def main() -> int:
    token = os.environ.get("TELEGRAM_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("TELEGRAM_TOKEN/TELEGRAM_CHAT_ID not set — skipping notification")
        return 0

    stats = collect_stats(Path(os.environ.get("RESULT_DIR", "allure-results")))
    text = format_message(
        stats,
        repo=os.environ.get("REPO", "?"),
        branch=os.environ.get("BRANCH", "?"),
        commit=os.environ.get("COMMIT", "")[:7],
        trigger=os.environ.get("TRIGGER", "?"),
        report_url=os.environ.get("REPORT_URL", ""),
        run_url=os.environ.get("RUN_URL", ""),
    )
    try:
        status = send_message(token, chat_id, text)
        print(f"Telegram notification sent: HTTP {status}")
    except Exception as exc:  # notification must never fail the build
        print(f"Telegram notification failed: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
