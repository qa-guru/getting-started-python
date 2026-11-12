"""Сохранение артефактов падения тестов и вложения в Allure."""
import warnings
from pathlib import Path

import allure
from selenium.webdriver.remote.webdriver import WebDriver


def save_failure_artifacts(driver: WebDriver, artifacts_dir: Path, name: str) -> None:
    """Сохранить скриншот и page source упавшего теста.

    Файлы пишутся в artifacts_dir под именем name, те же данные
    прикладываются к отчёту Allure. Ошибки сбора артефактов
    диагностируются и не скрывают исходную причину падения.
    """
    try:
        artifacts_dir.mkdir(exist_ok=True)
    except Exception as e:
        warnings.warn(f"Не удалось создать каталог артефактов {artifacts_dir}: {e}")
    try:
        screenshot = driver.get_screenshot_as_png()
        (artifacts_dir / f"{name}.png").write_bytes(screenshot)
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        warnings.warn(f"Не удалось сохранить скриншот для {name}: {e}")
    try:
        source = driver.page_source
        (artifacts_dir / f"{name}.html").write_text(source, encoding="utf-8")
        allure.attach(source, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception as e:
        warnings.warn(f"Не удалось сохранить page source для {name}: {e}")
