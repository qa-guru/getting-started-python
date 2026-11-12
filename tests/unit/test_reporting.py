import json
import urllib.request

import allure
import pytest

import notify_telegram
from infrastructure.reporting.artifacts import save_failure_artifacts
from infrastructure.reporting.stats import collect_stats
from infrastructure.reporting.telegram import (
    TelegramSendError,
    format_message,
    send_message,
)
from test_data.consts.reporting import (
    ARTIFACT_ERROR_TEXT,
    HTTP_STATUS_OK,
    PAGE_SOURCE_HTML,
    RUN_INFO,
    SCREENSHOT_BYTES,
    SEND_ERROR_TEXT,
    STATS_ALL_PASSED,
    STATS_MIXED,
    STATS_MIXED_FAILED,
    STATS_MIXED_TOTAL,
    TELEGRAM_API_URL,
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN,
)


class _StubDriver:
    """Драйвер-подмена с управляемыми ошибками сбора артефактов."""

    def __init__(self, screenshot=SCREENSHOT_BYTES, page_source=PAGE_SOURCE_HTML):
        self._screenshot = screenshot
        self._page_source = page_source

    def get_screenshot_as_png(self):
        if isinstance(self._screenshot, Exception):
            raise self._screenshot
        return self._screenshot

    @property
    def page_source(self):
        if isinstance(self._page_source, Exception):
            raise self._page_source
        return self._page_source


class _FakeResponse:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@allure.epic("Инфраструктура")
@allure.feature("Отчётность")
class TestFailureArtifacts:

    @allure.story("Сохранение артефактов падения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Скриншот и page source сохраняются в каталог артефактов")
    def test_artifacts_saved(self, tmp_path):
        with allure.step("Сохранить артефакты исправного драйвера"):
            save_failure_artifacts(_StubDriver(), tmp_path, "case")

        with allure.step("Проверить записанные файлы"):
            assert (tmp_path / "case.png").read_bytes() == SCREENSHOT_BYTES
            assert (tmp_path / "case.html").read_text(encoding="utf-8") == PAGE_SOURCE_HTML

    @allure.story("Сохранение артефактов падения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Сбой скриншота диагностируется и не мешает сохранить page source")
    def test_screenshot_failure_warns_and_keeps_source(self, tmp_path):
        with allure.step("Подготовить драйвер с ошибкой получения скриншота"):
            drv = _StubDriver(screenshot=RuntimeError(ARTIFACT_ERROR_TEXT))

        with allure.step("Сохранить артефакты и проверить предупреждение"):
            with pytest.warns(UserWarning, match="скриншот"):
                save_failure_artifacts(drv, tmp_path, "case")

        with allure.step("Проверить, что page source всё равно сохранён"):
            assert (tmp_path / "case.html").read_text(encoding="utf-8") == PAGE_SOURCE_HTML

    @allure.story("Сохранение артефактов падения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Сбой page source диагностируется и не мешает сохранить скриншот")
    def test_page_source_failure_warns_and_keeps_screenshot(self, tmp_path):
        with allure.step("Подготовить драйвер с ошибкой получения page source"):
            drv = _StubDriver(page_source=RuntimeError(ARTIFACT_ERROR_TEXT))

        with allure.step("Сохранить артефакты и проверить предупреждение"):
            with pytest.warns(UserWarning, match="page source"):
                save_failure_artifacts(drv, tmp_path, "case")

        with allure.step("Проверить, что скриншот всё равно сохранён"):
            assert (tmp_path / "case.png").read_bytes() == SCREENSHOT_BYTES

    @allure.story("Сохранение артефактов падения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Сбой создания каталога диагностируется и не подменяет падение теста")
    def test_artifacts_dir_failure_is_diagnosed(self, tmp_path):
        with allure.step("Подготовить путь, где каталог артефактов нельзя создать"):
            blocker = tmp_path / "blocker"
            blocker.write_text("file", encoding="utf-8")
            artifacts_dir = blocker / "artifacts"

        with allure.step("Проверить, что сбор артефактов диагностируется без исключения"):
            with pytest.warns(UserWarning):
                save_failure_artifacts(_StubDriver(), artifacts_dir, "case")


@allure.epic("Инфраструктура")
@allure.feature("Отчётность")
class TestRunStats:

    @allure.story("Статистика прогона")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Статистика считает статусы и пропускает нечитаемые файлы")
    def test_collect_stats_counts_and_skips_broken(self, tmp_path):
        with allure.step("Подготовить файлы результатов Allure"):
            (tmp_path / "a-result.json").write_text(
                json.dumps({"status": "passed"}), encoding="utf-8"
            )
            (tmp_path / "b-result.json").write_text(
                json.dumps({"status": "failed"}), encoding="utf-8"
            )
            (tmp_path / "c-result.json").write_text("not json", encoding="utf-8")
            (tmp_path / "d-result.json").write_text(
                json.dumps({"status": "unknown"}), encoding="utf-8"
            )

        with allure.step("Собрать статистику"):
            stats = collect_stats(tmp_path)

        with allure.step("Проверить счётчики"):
            assert stats == {"passed": 1, "failed": 1, "broken": 0, "skipped": 0}


@allure.epic("Инфраструктура")
@allure.feature("Уведомления")
class TestTelegram:

    @allure.story("Текст уведомления")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Сообщение о падении содержит статус, счётчики и ссылки")
    def test_format_message_failed_run(self):
        with allure.step("Сформировать сообщение по статистике с падениями"):
            text = format_message(STATS_MIXED, **RUN_INFO)

        with allure.step("Проверить статус, счётчики и ссылки"):
            assert "FAILED" in text
            assert f"Total: {STATS_MIXED_TOTAL}" in text
            assert f"❌ {STATS_MIXED_FAILED}" in text
            assert RUN_INFO["report_url"] in text
            assert RUN_INFO["run_url"] in text

    @allure.story("Текст уведомления")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Сообщение об успешном прогоне содержит статус PASSED")
    def test_format_message_passed_run(self):
        with allure.step("Сформировать сообщение по успешной статистике"):
            text = format_message(STATS_ALL_PASSED, **RUN_INFO)

        with allure.step("Проверить статус"):
            assert "PASSED" in text

    @allure.story("Отправка уведомления")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Отправка использует подменённый транспорт и возвращает HTTP-статус")
    def test_send_message_uses_transport(self, monkeypatch):
        with allure.step("Подменить транспорт Telegram Bot API"):
            captured = {}

            def fake_urlopen(req, timeout):
                captured["url"] = req.full_url
                captured["body"] = json.loads(req.data.decode())
                return _FakeResponse(HTTP_STATUS_OK)

            monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

        with allure.step("Отправить сообщение через подмену"):
            status = send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, "text")

        with allure.step("Проверить адрес, полезную нагрузку и ответ"):
            assert status == HTTP_STATUS_OK
            assert captured["url"] == TELEGRAM_API_URL
            assert captured["body"]["chat_id"] == TELEGRAM_CHAT_ID

    @allure.story("Отправка уведомления")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ошибка отправки диагностируется без раскрытия токена")
    def test_send_error_masks_token(self, monkeypatch):
        with allure.step("Подменить транспорт ошибкой, содержащей адрес с токеном"):
            def fake_urlopen(req, timeout):
                raise RuntimeError(f"cannot open {req.full_url}")

            monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

        with allure.step("Проверить, что ошибка отправки маскирует токен"):
            with pytest.raises(TelegramSendError) as excinfo:
                send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, "text")
            assert TELEGRAM_TOKEN not in str(excinfo.value)

    @allure.story("CLI уведомлений")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Без секретов CLI пропускает отправку и возвращает 0")
    def test_cli_skips_without_secrets(self, monkeypatch):
        with allure.step("Убрать секреты Telegram из окружения"):
            monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
            monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

        with allure.step("Проверить код завершения CLI"):
            assert notify_telegram.main() == 0

    @allure.story("CLI уведомлений")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Сбой отправки не ломает сборку и не раскрывает токен")
    def test_cli_send_failure_keeps_exit_zero(self, monkeypatch, capsys):
        with allure.step("Подготовить окружение и подмену отправки с ошибкой"):
            monkeypatch.setenv("TELEGRAM_TOKEN", TELEGRAM_TOKEN)
            monkeypatch.setenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
            monkeypatch.setattr(
                notify_telegram, "send_message",
                lambda *_: (_ for _ in ()).throw(TelegramSendError(SEND_ERROR_TEXT)),
            )

        with allure.step("Запустить CLI и проверить результат"):
            assert notify_telegram.main() == 0

        with allure.step("Проверить диагностику без секретов в выводе"):
            out = capsys.readouterr().out
            assert SEND_ERROR_TEXT in out
            assert TELEGRAM_TOKEN not in out
